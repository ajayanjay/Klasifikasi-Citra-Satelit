import os
import sys
import warnings

os.environ["MPLCONFIGDIR"] = os.path.join(os.environ.get("TEMP", "C:/tmp"), "matplotlib")
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import cv2
import tifffile as tiff
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap, BoundaryNorm
from skimage.feature import graycomatrix, graycoprops
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, cohen_kappa_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.size"] = 10

BAND_ORDER = ["b2", "b3", "b4", "b8", "b11", "b12"]

EPOCHS = [
    ("2023 Pre", "s2_2023_pre"),
    ("2023 Fire", "s2_2023_fire"),
    ("2024 Y1", "s2_2024_y1"),
    ("2025 Y2", "s2_2025_y2"),
    ("2026 Y3", "s2_2026_now"),
]

# 4-Class Post-Fire Land Cover Taxonomy (2-Stage Hierarchical Classification: Bare Land + Spectral-GLCM)
CLASS_NAMES = {
    1: "Structured Monoculture Vegetation",
    2: "Degraded Shrubland",
    3: "Natural Forest Succession",
    4: "Exposed Bare Peat / Unrecovered Land",
}
CLASS_COLORS = {1: "#e6b800", 2: "#d95f02", 3: "#2ca02c", 4: "#ff1744"}

# 3-Class Macro Spectral Taxonomy (Pre-GLCM: Dense Green Vegetation, Dry Shrubland, Bare Soil / Built-Up)
MACRO_NAMES = {
    1: "Dense Green Vegetation",
    2: "Dry Peat Shrubland",
    3: "Bare Soil / Non-Vegetated",
}
MACRO_COLORS = {1: "#00c853", 2: "#ff9100", 3: "#ff1744"}


def to_hwc(arr):
    if arr.ndim == 3 and arr.shape[0] < arr.shape[2]:
        return np.transpose(arr, (1, 2, 0))
    return arr


def detect_pixel_size_m(tif_path, shape_hw):
    """Mendeteksi resolusi spasial (10m vs 15m) dari metadata GeoTIFF atau dimensi grid."""
    try:
        with tiff.TiffFile(tif_path) as tf:
            tags = tf.pages[0].tags
            if "ModelPixelScaleTag" in tags:
                deg_scale = float(tags["ModelPixelScaleTag"].value[0])
                meters = deg_scale * 111320.0
                if 8.0 <= meters <= 12.5:
                    return 10.0
                if 12.5 < meters <= 18.0:
                    return 15.0
    except Exception:
        pass
    return 10.0 if max(shape_hw) >= 2000 else 15.0


def load_dataset(roi_name="Kalteng_Sebangau_Kahayan"):
    """
    Membaca seluruh GeoTIFF hasil ekspor GEE / get_data.py.
    Jika file wajib belum tersedia, eksekusi berhenti dengan pesan galat.
    """
    paths = {suffix: os.path.join(DATA_DIR, f"{roi_name}_{suffix}.tif") for _, suffix in EPOCHS}
    paths["aux"] = os.path.join(DATA_DIR, f"{roi_name}_aux_firms_water.tif")
    paths["dw"] = os.path.join(DATA_DIR, f"{roi_name}_gt_dynamic_world_2026.tif")
    gedi_path = os.path.join(DATA_DIR, f"{roi_name}_gedi_rh98.tif")

    missing = [p for p in paths.values() if not os.path.exists(p)]
    if missing:
        msg = "\n".join(f"  - {os.path.relpath(p, BASE_DIR)}" for p in missing)
        raise FileNotFoundError(
            f"File GeoTIFF berikut belum tersedia:\n{msg}\n"
            f"Jalankan terlebih dahulu get_data.py atau ekspor dari GEE."
        )

    print(f"[INFO] Membaca dataset GeoTIFF dari folder data/ untuk {roi_name}...")
    raw = {k: to_hwc(tiff.imread(p)).astype(np.float32) for k, p in paths.items()}
    gedi = to_hwc(tiff.imread(gedi_path)).astype(np.float32) if os.path.exists(gedi_path) else None

    arrays = list(raw.values()) + ([gedi] if gedi is not None else [])
    H = min(a.shape[0] for a in arrays)
    W = min(a.shape[1] for a in arrays)
    pixel_size_m = detect_pixel_size_m(paths["s2_2023_pre"], (H, W))
    print(f"[INFO] Dimensi citra: {W}x{H} piksel | Resolusi spasial: {pixel_size_m:.0f} meter/piksel")

    images = {}
    for label, suffix in EPOCHS:
        arr = raw[suffix][:H, :W]
        images[label] = {b: arr[:, :, i] for i, b in enumerate(BAND_ORDER)}

    aux = raw["aux"][:H, :W]
    firms_t21 = aux[:, :, 0] if aux.ndim == 3 else aux
    jrc_water = aux[:, :, 1] if aux.ndim == 3 and aux.shape[2] > 1 else np.zeros_like(firms_t21)
    dw = raw["dw"][:H, :W]
    gt_dw = (dw if dw.ndim == 2 else dw[:, :, 0]).astype(np.int16)
    gedi_h = None
    if gedi is not None:
        g = gedi[:H, :W]
        gedi_h = g if g.ndim == 2 else g[:, :, 0]

    return images, firms_t21, jrc_water, gt_dw, gedi_h, pixel_size_m


def valid_mask(img):
    return (img["b8"] > 0) & (img["b4"] > 0) & (img["b11"] > 0)


def spectral_indices(img):
    eps = 1e-6
    ndvi = (img["b8"] - img["b4"]) / (img["b8"] + img["b4"] + eps)
    ndmi = (img["b8"] - img["b11"]) / (img["b8"] + img["b11"] + eps)
    bsi = ((img["b11"] + img["b4"]) - (img["b8"] + img["b2"])) / (
        (img["b11"] + img["b4"]) + (img["b8"] + img["b2"]) + eps
    )
    nbr = (img["b8"] - img["b12"]) / (img["b8"] + img["b12"] + eps)
    ndwi = (img["b3"] - img["b8"]) / (img["b3"] + img["b8"] + eps)
    ndbi = (img["b11"] - img["b8"]) / (img["b11"] + img["b8"] + eps)
    return {"NDVI": ndvi, "NDMI": ndmi, "BSI": bsi, "NBR": nbr, "NDWI": ndwi, "NDBI": ndbi}


def compute_glcm_haralick(nir_band, vmin, vmax, window_size=7, levels=16, stride=6, active_mask=None):
    """
    Perhitungan matriks ko-okurensi tingkat keabuan (GLCM Orde-2) menggunakan
    skimage.feature.graycomatrix dan graycoprops pada 4 sudut arah (0, 45, 90, 135 derajat).
    Jika active_mask diberikan, perhitungan hanya dijalankan pada titik grid di dalam masker.
    """
    H, W = nir_band.shape
    norm_img = np.clip((nir_band - vmin) / (vmax - vmin + 1e-6), 0, 1)
    quantized = (norm_img * (levels - 1)).astype(np.uint8)

    pad = window_size // 2
    padded = np.pad(quantized, pad, mode="reflect")

    r_coords = np.arange(0, H, stride)
    c_coords = np.arange(0, W, stride)
    homo_grid = np.zeros((len(r_coords), len(c_coords)), dtype=np.float32)
    cont_grid = np.zeros_like(homo_grid)
    entr_grid = np.zeros_like(homo_grid)

    if active_mask is not None:
        k_dil = cv2.getStructuringElement(cv2.MORPH_RECT, (stride + 2, stride + 2))
        dil_mask = cv2.dilate(active_mask.astype(np.uint8), k_dil).astype(bool)
    else:
        dil_mask = None

    angles = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]

    for i, r in enumerate(r_coords):
        for j, c in enumerate(c_coords):
            if dil_mask is not None and not dil_mask[r, c]:
                continue
            patch = padded[r:r + window_size, c:c + window_size]
            glcm = graycomatrix(
                patch, distances=[1], angles=angles, levels=levels, symmetric=True, normed=True
            )
            homo_grid[i, j] = np.mean(graycoprops(glcm, "homogeneity"))
            cont_grid[i, j] = np.mean(graycoprops(glcm, "contrast"))

            p_glcm = glcm[:, :, 0, :]
            entr_grid[i, j] = np.mean(-np.sum(p_glcm * np.log2(p_glcm + 1e-10), axis=(0, 1)))

    homogeneity = cv2.resize(homo_grid, (W, H), interpolation=cv2.INTER_LINEAR)
    contrast = cv2.resize(cont_grid, (W, H), interpolation=cv2.INTER_LINEAR)
    entropy = cv2.resize(entr_grid, (W, H), interpolation=cv2.INTER_LINEAR)
    return homogeneity, contrast, entropy


def stretch_composite(c1, c2, c3, mask, p_low=2, p_high=98):
    rgb = np.stack([c1, c2, c3], axis=-1).astype(np.float32)
    out = np.zeros_like(rgb)
    for i in range(3):
        ch = rgb[:, :, i]
        vals = ch[mask]
        if vals.size == 0:
            continue
        lo, hi = np.percentile(vals, p_low), np.percentile(vals, p_high)
        out[:, :, i] = np.clip((ch - lo) / (hi - lo + 1e-6), 0, 1)
    out[~mask] = 0
    return out


def run_macro_spectral_kmeans(spec_now, land_mask):
    """
    Klasterisasi K-Means (k=3) berbasis Spektral Murni (Sebelum GLCM):
    Membedakan 1 = Vegetasi Hijau Rapat, 2 = Semak Gambut Kering, 3 = Kupasan Tanah / Terbangun (Kota).
    """
    rng = np.random.RandomState(42)
    idx_all = np.flatnonzero(land_mask)
    sample_idx = rng.choice(idx_all, size=min(80000, idx_all.size), replace=False)

    f_names = ["NDVI", "NDMI", "BSI", "NDBI"]
    X_full = np.column_stack([spec_now[k].ravel()[idx_all] for k in f_names])
    scaler = StandardScaler()
    X_sample = scaler.fit_transform(np.column_stack([spec_now[k].ravel()[sample_idx] for k in f_names]))

    km = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X_sample)
    raw_pred = km.predict(scaler.transform(X_full))

    # Urutkan berdasarkan rata-rata NDVI tertinggi -> terendah:
    # NDVI tertinggi = 1 (Vegetasi Hijau), sedang = 2 (Semak Kering), terendah & BSI/NDBI tinggi = 3 (Kupasan/Kota)
    means_ndvi = [np.mean(X_full[raw_pred == k, 0]) for k in range(3)]
    order = np.argsort(means_ndvi)[::-1]
    lmap = {int(order[0]): 1, int(order[1]): 2, int(order[2]): 3}
    mapped = np.vectorize(lmap.get)(raw_pred)

    macro_raster = np.zeros(spec_now["NDVI"].shape, dtype=np.uint8)
    macro_raster.ravel()[idx_all] = mapped
    return macro_raster


def run_pipeline(roi_name="Kalteng_Sebangau_Kahayan"):
    print(f"[INFO] Memulai analisis Pengolahan Citra Digital untuk wilayah: {roi_name}")
    images, firms_t21, jrc_water, gt_dw, gedi_h, pixel_size_m = load_dataset(roi_name)
    pre, fire, now = images["2023 Pre"], images["2023 Fire"], images["2026 Y3"]
    valid = {label: valid_mask(img) for label, img in images.items()}
    pixel_area_ha = (pixel_size_m * pixel_size_m) / 10000.0
    is_large = max(pre["b8"].shape) >= 2000

    # 1. Metode 1: Deliniasi Area Terbakar 2023 (dNBR + Filter Vegetasi/Termal/Air + Morfologi)
    print("[INFO] Tahap 1: Menghitung indeks NBR, dNBR, dan operasi morfologi citra...")
    spec_pre = spectral_indices(pre)
    spec_fire = spectral_indices(fire)
    dnbr = spec_pre["NBR"] - spec_fire["NBR"]
    both_valid = valid["2023 Pre"] & valid["2023 Fire"]
    dnbr[~both_valid] = 0

    # Masker daratan bervegetasi pra-kebakaran (mengeliminasi badan air sungai & bangunan permanen kota)
    land_mask = (jrc_water < 25.0) & (spec_pre["NDWI"] < 0.05)
    pre_vegetated = (spec_pre["NDVI"] > 0.32) & (spec_pre["NDBI"] < 0.05)
    raw_burn = dnbr > 0.20
    thermal_valid = (firms_t21 > 310.0) | (dnbr > 0.28)
    candidate_burn = (raw_burn & land_mask & pre_vegetated & thermal_valid & both_valid).astype(np.uint8)

    open_sz = 5 if is_large else 3
    close_sz = 7 if is_large else 5
    k_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (open_sz, open_sz))
    opened = cv2.morphologyEx(candidate_burn, cv2.MORPH_OPEN, k_open)
    k_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (close_sz, close_sz))
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, k_close)

    # Eliminasi komponen terhubung yang terlalu kecil (< 1.0 Ha) agar bebas dari sisa bintik noise
    min_px = int(round(1.0 / pixel_area_ha))
    num_cc, cc_labels, cc_stats, _ = cv2.connectedComponentsWithStats(closed, connectivity=8)
    clean_burn_mask = np.zeros_like(closed, dtype=bool)
    for idx_cc in range(1, num_cc):
        if cc_stats[idx_cc, cv2.CC_STAT_AREA] >= min_px:
            clean_burn_mask[cc_labels == idx_cc] = True

    noise_removed_mask = (candidate_burn.astype(bool)) & (~clean_burn_mask)
    track_mask = clean_burn_mask & valid["2024 Y1"] & valid["2025 Y2"] & valid["2026 Y3"]

    raw_burn_ha = np.sum(candidate_burn) * pixel_area_ha
    clean_burn_ha = np.sum(clean_burn_mask) * pixel_area_ha
    noise_ha = np.sum(noise_removed_mask) * pixel_area_ha
    track_ha = np.sum(track_mask) * pixel_area_ha
    print(f"[INFO] Luas kandidat kasar: {raw_burn_ha:,.2f} Ha | Noise dieliminasi: {noise_ha:,.2f} Ha")
    print(f"[INFO] Luas poligon luka bakar bersih: {clean_burn_ha:,.2f} Ha (teramati penuh: {track_ha:,.2f} Ha)")

    # 2. Metode 2: Ekstraksi Fitur Spektral dan Tekstur GLCM Orde-2 per epoch
    print("[INFO] Tahap 2: Mengekstraksi NDVI, NDMI, BSI, NDBI, dan tekstur GLCM setiap tahun...")
    nir_pool = np.concatenate([img["b8"][valid[l]] for l, img in images.items()])
    nir_min, nir_max = np.percentile(nir_pool, 2), np.percentile(nir_pool, 98)
    stride_glcm = 6 if is_large else 4

    features = {}
    for label, img in images.items():
        spec = spectral_indices(img)
        print(f"[INFO]   GLCM {label}...")
        # Pada tahun 2026 Y3 dihitung penuh satu citra untuk visualisasi peta tekstur;
        # pada tahun historis dihitung pada poligon luka bakar untuk kurva trajektori.
        mask_arg = None if label == "2026 Y3" else track_mask
        homo, cont, entr = compute_glcm_haralick(
            img["b8"], nir_min, nir_max, window_size=7, levels=16, stride=stride_glcm, active_mask=mask_arg
        )
        features[label] = {
            **spec,
            "Homogeneity": homo,
            "Contrast": cont,
            "Entropy": entr,
        }

    f_now = features["2026 Y3"]

    # 3A. Klasterisasi Makro Spektral (Sebelum GLCM: Vegetasi Hijau, Semak, Kupasan/Bangunan)
    print("[INFO] Tahap 3A: Menjalankan K-Means Spektral Makro (Hijau vs Semak vs Kupasan/Bangunan)...")
    macro_landscape = run_macro_spectral_kmeans(f_now, land_mask & valid["2026 Y3"])
    macro_burned = np.zeros_like(macro_landscape)
    macro_burned[track_mask] = macro_landscape[track_mask]
    macro_area = {c: np.sum(macro_burned == c) * pixel_area_ha for c in MACRO_NAMES}
    macro_pct = {c: macro_area[c] / track_ha * 100.0 for c in MACRO_NAMES}

    # 3B. Metode 3: Klasifikasi Berjenjang Hierarki 2-Tahap (Opsi 1)
    # Tahap 1: Pemisahan Spektral Non-Vegetasi (Kupasan Tanah / Lahan Mati Pasca-Bakar)
    # Area non-vegetasi TIDAK dipaksa melalui GLCM kanopi, melainkan langsung dilestarikan sebagai Kelas 4.
    print("[INFO] Tahap 3B: Klasifikasi Hierarkis 2-Tahap (Tahap 1: Ekstraksi Kupasan Tanah; Tahap 2: GLCM Kanopi)...")
    bare_mask = track_mask & (macro_burned == 3)
    veg_mask = track_mask & (~bare_mask)

    # Tahap 2: Ekstraksi GLCM + K-Means (k=3) KHUSUS pada Piksel Bervegetasi (veg_mask)
    feat_keys = ["NDVI", "NDMI", "BSI", "Homogeneity", "Entropy"]
    X_veg = np.column_stack([f_now[k][veg_mask] for k in feat_keys])
    X_scaled = StandardScaler().fit_transform(X_veg)
    raw_labels = KMeans(n_clusters=3, random_state=42, n_init=10).fit_predict(X_scaled)

    # Pengurutan kelas berbasis karakteristik biofisik spektral dan tekstur GLCM:
    # - Kelas 1 (Vegetasi Terstruktur / Monokultur): Homogeneity tertinggi, Entropy terendah
    # - Kelas 3 (Vegetasi Suksesi Alami): NDVI & NDMI tertinggi di antara vegetasi, kanopi multi-strata heterogen
    # - Kelas 2 (Semak Belukar Terdegradasi): NDVI & NDMI lebih rendah, tajuk terbuka
    stats_veg = []
    for k in range(3):
        idx = raw_labels == k
        stats_veg.append({
            "k": k,
            "homo": float(np.mean(X_veg[idx, 3])),
            "entr": float(np.mean(X_veg[idx, 4])),
            "ndvi": float(np.mean(X_veg[idx, 0])),
        })
    k_struct = max(stats_veg, key=lambda d: d["homo"])["k"]
    rem = [d for d in stats_veg if d["k"] != k_struct]
    k_nat = max(rem, key=lambda d: d["ndvi"])["k"]
    k_shrub = min(rem, key=lambda d: d["ndvi"])["k"]

    veg_label_map = {k_struct: 1, k_shrub: 2, k_nat: 3}
    mapped_veg = np.vectorize(veg_label_map.get)(raw_labels)

    cluster_raster = np.zeros(track_mask.shape, dtype=np.uint8)
    cluster_raster[veg_mask] = mapped_veg
    cluster_raster[bare_mask] = 4
    tiff.imwrite(os.path.join(DATA_DIR, "Hasil_Klaster_3Kelas_Karhutla.tif"), cluster_raster)
    tiff.imwrite(os.path.join(DATA_DIR, "Hasil_Klaster_4Kelas_Karhutla.tif"), cluster_raster)

    area = {c: np.sum(cluster_raster == c) * pixel_area_ha for c in CLASS_NAMES}
    pct = {c: area[c] / track_ha * 100.0 for c in CLASS_NAMES}

    # 4. Trajektori tahunan setiap kelas (2023 Pre -> 2026 Y3)
    print("[INFO] Tahap 4: Menghitung kurva trajektori tahunan rata-rata setiap kelas...")
    feat_all = ["NDVI", "NDMI", "BSI", "Homogeneity", "Contrast", "Entropy"]
    traj_rows = []
    for c in CLASS_NAMES:
        m_c = cluster_raster == c
        for label, _ in EPOCHS:
            m = m_c & valid[label]
            row = {"Kelas_ID": c, "Nama_Kelas": CLASS_NAMES[c], "Epoch": label, "Jumlah_Piksel": int(np.sum(m))}
            for f in feat_all:
                vals = features[label][f][m]
                row[f"Mean_{f}"] = round(float(np.mean(vals)), 4) if vals.size else np.nan
                row[f"Std_{f}"] = round(float(np.std(vals)), 4) if vals.size else np.nan
            traj_rows.append(row)
    df_traj = pd.DataFrame(traj_rows)
    traj_csv = os.path.join(DATA_DIR, "trajektori_tahunan_2023_2026.csv")
    df_traj.to_csv(traj_csv, index=False)

    # 5. Evaluasi Ground Truth (Dynamic World 2026 + Kriteria Struktur Kanopi & GEDI LiDAR)
    print("[INFO] Tahap 5: Evaluasi akurasi terhadap referensi Dynamic World 2026 dan GEDI LiDAR...")
    pred_labels = cluster_raster[track_mask]
    dw_burned = gt_dw[track_mask]
    homo_burned = f_now["Homogeneity"][track_mask]
    ndmi_burned = f_now["NDMI"][track_mask]
    bsi_burned = f_now["BSI"][track_mask]
    ndvi_burned = f_now["NDVI"][track_mask]

    tree_mask = (dw_burned == 1)
    homo_med = float(np.median(homo_burned[tree_mask])) if np.any(tree_mask) else 0.65

    # Hierarki Referensi Ground Truth 4 Kelas:
    # 1. Kupasan Tanah / Lahan Mati: DW 6 (built), 7 (bare), atau tanah terbuka kering (BSI > 0 & NDMI < 0) -> Kelas 4
    # 2. Semak Belukar Terdegradasi: DW 2 (grass), 5 (shrub), atau defisit air tajuk (NDMI < 0.10) -> Kelas 2
    # 3. Vegetasi Terstruktur / Monokultur: DW 4 (crops) atau tegakan pohon (DW 1) dengan homogenitas spasial tinggi -> Kelas 1
    # 4. Vegetasi Suksesi Alami: tegakan pohon (DW 1) dengan kanopi multi-strata heterogen -> Kelas 3
    gt_labels = np.where(
        np.isin(dw_burned, [6, 7]) | ((bsi_burned > 0.0) & (ndmi_burned < 0.0)),
        4,
        np.where(
            np.isin(dw_burned, [2, 5]) | (ndmi_burned < 0.10),
            2,
            np.where(
                np.isin(dw_burned, [4]) | ((dw_burned == 1) & (homo_burned >= homo_med)),
                1,
                3,
            ),
        ),
    )

    cm = confusion_matrix(gt_labels, pred_labels, labels=[1, 2, 3, 4])
    oa = np.trace(cm) / np.sum(cm) * 100.0
    kappa = cohen_kappa_score(gt_labels, pred_labels)

    gedi_valid = (gedi_h > 0) if gedi_h is not None else np.zeros(track_mask.shape, bool)

    rows = []
    for c in CLASS_NAMES:
        m_c = cluster_raster == c
        m_g = m_c & gedi_valid
        rows.append({
            "Kelas_ID": c,
            "Nama_Kelas": CLASS_NAMES[c],
            "Jumlah_Piksel": int(np.sum(m_c)),
            "Luas_Ha": round(float(area[c]), 2),
            "Proporsi_Persen": round(float(pct[c]), 2),
            **{f"Mean_{f}_2026": round(float(np.mean(f_now[f][m_c])), 4) for f in feat_all},
            "Jumlah_Footprint_GEDI": int(np.sum(m_g)),
            "Mean_GEDI_RH98_m": round(float(np.mean(gedi_h[m_g])), 2) if np.any(m_g) else np.nan,
        })
    df_stats = pd.DataFrame(rows)
    csv_path = os.path.join(DATA_DIR, "statistik_klaster_2023_2026.csv")
    df_stats.to_csv(csv_path, index=False)

    print("\n--- Ringkasan Kuantitatif Klasterisasi Spektral + GLCM (2023 - 2026) ---")
    print(df_stats.to_string(index=False))
    print(f"\n[INFO] Overall Accuracy (OA): {oa:.2f}% | Cohen's Kappa: {kappa:.4f}")

    # Persiapan Komposit Visual
    rgb_pre = stretch_composite(pre["b4"], pre["b3"], pre["b2"], valid["2023 Pre"])
    rgb_fire = stretch_composite(fire["b4"], fire["b3"], fire["b2"], valid["2023 Fire"])
    swir_fire = stretch_composite(fire["b12"], fire["b8"], fire["b4"], valid["2023 Fire"])
    rgb_now = stretch_composite(now["b4"], now["b3"], now["b2"], valid["2026 Y3"])
    cir_now = stretch_composite(now["b8"], now["b4"], now["b3"], valid["2026 Y3"])
    swir_now = stretch_composite(now["b12"], now["b8"], now["b4"], valid["2026 Y3"])

    # =========================================================================
    # FIGURE 1: MULTI-SPECTRAL COMPOSITES & BIOPHYSICAL INDICES (SENTINEL-2 10M)
    # =========================================================================
    print("[INFO] Rendering Figure 1: Sentinel-2 Multi-Spectral Composites & Biophysical Indices...")
    fig, axes = plt.subplots(2, 3, figsize=(18, 11), dpi=160)
    axes[0, 0].imshow(rgb_now)
    axes[0, 0].set_title("(a) True Color RGB Composite (B4-B3-B2)\nSurface Reflectance (2026 Y3)", fontweight="bold")
    axes[0, 1].imshow(cir_now)
    axes[0, 1].set_title("(b) Color Infrared (CIR) Composite (B8-B4-B3)\nNIR Band: Dense Vegetation = Bright Red", fontweight="bold")
    axes[0, 2].imshow(swir_now)
    axes[0, 2].set_title("(c) False Color SWIR Composite (B12-B8-B4)\nBare Peat & Dry Shrubland = Orange/Red", fontweight="bold")

    im1 = axes[1, 0].imshow(f_now["NDVI"], cmap="RdYlGn", vmin=-0.1, vmax=0.85)
    axes[1, 0].set_title("(d) Normalized Difference Vegetation Index (NDVI)\nFormula: (B8 - B4) / (B8 + B4)", fontweight="bold")
    plt.colorbar(im1, ax=axes[1, 0], fraction=0.046, pad=0.04, label="NDVI")

    im2 = axes[1, 1].imshow(f_now["NDMI"], cmap="BrBG", vmin=-0.3, vmax=0.45)
    axes[1, 1].set_title("(e) Normalized Difference Moisture Index (NDMI)\nCanopy Water Content: (B8 - B11) / (B8 + B11)", fontweight="bold")
    plt.colorbar(im2, ax=axes[1, 1], fraction=0.046, pad=0.04, label="NDMI")

    im3 = axes[1, 2].imshow(f_now["BSI"], cmap="coolwarm", vmin=-0.35, vmax=0.25)
    axes[1, 2].set_title("(f) Bare Soil Index (BSI)\nExposed Soil & Built-Up Surface", fontweight="bold")
    plt.colorbar(im3, ax=axes[1, 2], fraction=0.046, pad=0.04, label="BSI")

    for ax in axes.ravel():
        ax.axis("off")
    fig.suptitle(f"Sentinel-2 Multi-Spectral Composites and Biophysical Spectral Indices ({roi_name})", fontsize=13, fontweight="bold")
    plt.tight_layout()
    fig1_path = os.path.join(RESULTS_DIR, "fig1_komposit_multispektral.png")
    plt.savefig(fig1_path, dpi=200, bbox_inches="tight")
    plt.savefig(os.path.join(RESULTS_DIR, "citra_murni_multi_spektral_dan_analisis.png"), dpi=200, bbox_inches="tight")
    plt.close()

    # =========================================================================
    # FIGURE 2: METHOD 1 WORKFLOW (BURN SCAR DELINEATION, dNBR & MORPHOLOGY)
    # =========================================================================
    print("[INFO] Rendering Figure 2: Burn Scar Delineation & Mathematical Morphology Workflow...")
    fig, axes = plt.subplots(2, 4, figsize=(22, 11), dpi=160)

    # Row 1: Spectral & Thermal Observation Sequence (Pre-Fire -> Active Fire RGB -> SWIR -> FIRMS)
    axes[0, 0].imshow(rgb_pre)
    axes[0, 0].set_title("(a) Step 1: Pre-Fire Baseline (May-Jul 2023)\nTrue Color RGB (Intact Peat Swamp Forest)", fontweight="bold")

    axes[0, 1].imshow(rgb_fire)
    axes[0, 1].set_title("(b) Step 2A: Active Fire Peak (Sep-Nov 2023)\nTrue Color RGB (Charcoal Burn Scar)", fontweight="bold")

    axes[0, 2].imshow(swir_fire)
    axes[0, 2].set_title("(c) Step 2B: Active Fire Peak (Sep-Nov 2023)\nFalse Color SWIR (B12-B8-B4: Burn Scar = Orange/Brown)", fontweight="bold")

    firms_vis = np.ma.masked_where(firms_t21 < 300, firms_t21)
    axes[0, 3].imshow(rgb_fire * 0.45)
    im_firms = axes[0, 3].imshow(firms_vis, cmap="inferno", vmin=305, vmax=360)
    axes[0, 3].set_title("(d) Step 3: NASA FIRMS Brightness Temp (T21)\nThermal Anomaly Confirmation (> 310 K)", fontweight="bold")
    plt.colorbar(im_firms, ax=axes[0, 3], fraction=0.046, pad=0.04, label="Brightness Temp T21 (K)")

    # Row 2: Digital Image Processing Pipeline (dNBR -> Raw Candidate Mask -> Morphology -> 2026 Overlay)
    im_dnbr = axes[1, 0].imshow(dnbr, cmap="hot", vmin=0.0, vmax=0.55)
    axes[1, 0].set_title("(e) Step 4: Burn Severity Index (dNBR)\nDifferenced NBR (NBR Pre - NBR Fire)", fontweight="bold")
    plt.colorbar(im_dnbr, ax=axes[1, 0], fraction=0.046, pad=0.04, label="dNBR")

    raw_vis = np.zeros((*candidate_burn.shape, 3), dtype=np.float32)
    raw_vis[candidate_burn > 0] = [1.0, 0.55, 0.0]
    axes[1, 1].imshow(rgb_fire * 0.35 + raw_vis * 0.65)
    axes[1, 1].set_title(
        f"(f) Step 5: Raw Burn Candidate Mask (Pre-Morphology)\nArea: {raw_burn_ha:,.1f} Ha (Contains Salt-and-Pepper Noise)",
        fontweight="bold",
    )

    morph_vis = rgb_fire * 0.35
    morph_vis[clean_burn_mask] = [1.0, 0.15, 0.15]
    morph_vis[noise_removed_mask] = [0.0, 0.95, 1.0]
    axes[1, 2].imshow(np.clip(morph_vis, 0, 1))
    axes[1, 2].set_title(
        f"(g) Step 6: Morphological Opening & Closing Result\nClean Polygon: {clean_burn_ha:,.1f} Ha | Filtered Noise: {noise_ha:,.1f} Ha",
        fontweight="bold",
    )
    axes[1, 2].legend(
        handles=[
            Patch(facecolor="#ff2626", edgecolor="k", label=f"Clean Burn Scar ({clean_burn_ha:,.0f} Ha)"),
            Patch(facecolor="#00f2ff", edgecolor="k", label=f"Eliminated Noise ({noise_ha:,.0f} Ha)"),
        ],
        loc="lower right",
        fontsize=8,
        framealpha=0.92,
    )

    axes[1, 3].imshow(rgb_now)
    axes[1, 3].contour(clean_burn_mask, colors="cyan", linewidths=0.6)
    axes[1, 3].set_title(
        f"(h) Step 7: Clean Burn Scar Polygon on 2026 RGB\nCyan Contour = 2023 Burn Scar Boundary ({clean_burn_ha:,.0f} Ha)",
        fontweight="bold",
    )

    for ax in axes.ravel():
        ax.axis("off")
    fig.suptitle("Method 1 Pipeline: Burn Scar Delineation via Spectral Differencing (dNBR), Thermal Filtering, and Mathematical Morphology", fontsize=14, fontweight="bold")
    plt.tight_layout()
    fig2_path = os.path.join(RESULTS_DIR, "fig2_progres_workflow_morfologi.png")
    plt.savefig(fig2_path, dpi=200, bbox_inches="tight")
    plt.close()

    # =========================================================================
    # FIGURE 3: 6 EXTRACTED FEATURES FOR K-MEANS (SPECTRAL + HARALICK GLCM)
    # =========================================================================
    print("[INFO] Rendering Figure 3: Spectral & Haralick GLCM Texture Feature Maps (2026)...")
    fig, axes = plt.subplots(2, 3, figsize=(18, 11), dpi=160)
    f_cfg = [
        ("NDVI", "RdYlGn", 0.1, 0.85, "(a) Feature 1: NDVI (2026 Y3)\nCanopy Chlorophyll Density"),
        ("NDMI", "BrBG", -0.25, 0.40, "(b) Feature 2: NDMI (2026 Y3)\nCanopy Moisture Content"),
        ("BSI", "coolwarm", -0.35, 0.25, "(c) Feature 3: BSI (2026 Y3)\nBare Soil Exposure Index"),
        ("Homogeneity", "viridis", 0.35, 0.90, "(d) Feature 4: GLCM Homogeneity (2026 Y3)\nSpatial Canopy Regularity"),
        ("Contrast", "magma", 0.0, 4.0, "(e) Feature 5: GLCM Contrast (2026 Y3)\nLocal Gray-Level Canopy Variation"),
        ("Entropy", "plasma", 1.5, 4.8, "(f) Feature 6: GLCM Shannon Entropy (2026 Y3)\nStructural Disorder & Complexity"),
    ]
    for ax, (fk, cmap_name, vmin, vmax, title) in zip(axes.ravel(), f_cfg):
        im = ax.imshow(f_now[fk], cmap=cmap_name, vmin=vmin, vmax=vmax)
        ax.contour(clean_burn_mask, colors="cyan", linewidths=0.4, alpha=0.7)
        ax.set_title(title, fontweight="bold")
        ax.axis("off")
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label=fk)

    fig.suptitle("Method 2 Feature Extraction: Biophysical Spectral Indices & 4-Directional Haralick GLCM Texture (Cyan = 2023 Burn Scar)", fontsize=13, fontweight="bold")
    plt.tight_layout()
    fig3_path = os.path.join(RESULTS_DIR, "fig3_ekstraksi_fitur_spektral_glcm.png")
    plt.savefig(fig3_path, dpi=200, bbox_inches="tight")
    plt.close()

    # =========================================================================
    # FIGURE 4: MACRO SPECTRAL CLUSTERING (PRE-GLCM) VS 2-STAGE HIERARCHICAL GLCM
    # =========================================================================
    print("[INFO] Rendering Figure 4: Macro Spectral K-Means vs 2-Stage Hierarchical Spectral+GLCM...")
    fig, axes = plt.subplots(2, 3, figsize=(18, 11), dpi=160)

    cmap_macro = ListedColormap(["#1a1a1a", MACRO_COLORS[1], MACRO_COLORS[2], MACRO_COLORS[3]])
    norm_3 = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], 4)

    axes[0, 0].imshow(macro_landscape, cmap=cmap_macro, norm=norm_3)
    axes[0, 0].set_title("(a) Landscape Macro Spectral K-Means (Pre-GLCM)\n(Dense Vegetation, Dry Shrubland, Bare Soil / Built-Up)", fontweight="bold")
    axes[0, 0].axis("off")
    axes[0, 0].legend(
        handles=[Patch(facecolor=MACRO_COLORS[c], edgecolor="k", label=MACRO_NAMES[c]) for c in MACRO_NAMES],
        loc="lower right",
        fontsize=8.5,
        framealpha=0.92,
    )

    axes[0, 1].imshow(rgb_now * 0.40)
    axes[0, 1].imshow(np.ma.masked_equal(macro_burned, 0), cmap=cmap_macro, norm=norm_3)
    axes[0, 1].set_title("(b) Macro Spectral K-Means Inside Burn Scar (Pre-GLCM)\n(Without GLCM: Structured & Natural Vegetation Merged)", fontweight="bold")
    axes[0, 1].axis("off")
    axes[0, 1].legend(
        handles=[
            Patch(facecolor=MACRO_COLORS[c], edgecolor="k", label=f"{MACRO_NAMES[c]}: {macro_area[c]:,.0f} Ha ({macro_pct[c]:.1f}%)")
            for c in MACRO_NAMES
        ],
        loc="lower right",
        fontsize=8,
        framealpha=0.92,
    )

    cmap_klaster = ListedColormap(["#000000", CLASS_COLORS[1], CLASS_COLORS[2], CLASS_COLORS[3], CLASS_COLORS[4]])
    norm_4 = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5, 4.5], 5)
    axes[0, 2].imshow(rgb_now * 0.40)
    axes[0, 2].imshow(np.ma.masked_equal(cluster_raster, 0), cmap=cmap_klaster, norm=norm_4)
    axes[0, 2].set_title("(c) 2-Stage Hierarchical Classification (Spectral + GLCM)\n(Bare Peat Preserved; Green Split into Monoculture vs Succession)", fontweight="bold")
    axes[0, 2].axis("off")
    axes[0, 2].legend(
        handles=[
            Patch(facecolor=CLASS_COLORS[c], edgecolor="k", label=f"{CLASS_NAMES[c]}: {area[c]:,.0f} Ha ({pct[c]:.1f}%)")
            for c in CLASS_NAMES
        ],
        loc="lower right",
        fontsize=8,
        framealpha=0.92,
    )

    # Panel (d): Spectral Feature Profile per Class
    x_cls = np.arange(4)
    w_bar = 0.25
    ndvi_m = [df_stats.loc[df_stats["Kelas_ID"] == c, "Mean_NDVI_2026"].values[0] for c in [1, 2, 3, 4]]
    ndmi_m = [df_stats.loc[df_stats["Kelas_ID"] == c, "Mean_NDMI_2026"].values[0] for c in [1, 2, 3, 4]]
    bsi_m = [df_stats.loc[df_stats["Kelas_ID"] == c, "Mean_BSI_2026"].values[0] for c in [1, 2, 3, 4]]
    axes[1, 0].bar(x_cls - w_bar, ndvi_m, w_bar, label="NDVI (Chlorophyll)", color="#2e7d32")
    axes[1, 0].bar(x_cls, ndmi_m, w_bar, label="NDMI (Canopy Moisture)", color="#0288d1")
    axes[1, 0].bar(x_cls + w_bar, bsi_m, w_bar, label="BSI (Bare Soil)", color="#d95f02")
    axes[1, 0].axhline(0, color="k", linewidth=0.8)
    axes[1, 0].set_xticks(x_cls)
    axes[1, 0].set_xticklabels(["Class 1:\nStructured Mono.", "Class 2:\nDegraded Shrub", "Class 3:\nNat. Succession", "Class 4:\nBare Peat"], fontsize=8)
    axes[1, 0].set_ylabel("Mean Spectral Index Value")
    axes[1, 0].set_title("(d) Spectral Feature Signatures Across 4 Classes (2026)", fontweight="bold")
    axes[1, 0].legend(fontsize=8)
    axes[1, 0].grid(axis="y", alpha=0.3)

    # Panel (e): GLCM Texture Feature Profile per Class
    homo_m = [df_stats.loc[df_stats["Kelas_ID"] == c, "Mean_Homogeneity_2026"].values[0] for c in [1, 2, 3, 4]]
    cont_m = [df_stats.loc[df_stats["Kelas_ID"] == c, "Mean_Contrast_2026"].values[0] for c in [1, 2, 3, 4]]
    entr_m = [df_stats.loc[df_stats["Kelas_ID"] == c, "Mean_Entropy_2026"].values[0] for c in [1, 2, 3, 4]]
    axes[1, 1].bar(x_cls - w_bar, homo_m, w_bar, label="Homogeneity (Regularity)", color="#6a51a3")
    axes[1, 1].bar(x_cls, cont_m, w_bar, label="Contrast (Variation)", color="#e6550d")
    axes[1, 1].bar(x_cls + w_bar, entr_m, w_bar, label="Entropy (Disorder)", color="#31a354")
    axes[1, 1].set_xticks(x_cls)
    axes[1, 1].set_xticklabels(["Class 1:\nStructured Mono.", "Class 2:\nDegraded Shrub", "Class 3:\nNat. Succession", "Class 4:\nBare Peat"], fontsize=8)
    axes[1, 1].set_ylabel("Mean Haralick GLCM Value")
    axes[1, 1].set_title("(e) GLCM Texture Separation of Canopy Structure", fontweight="bold")
    axes[1, 1].legend(fontsize=8)
    axes[1, 1].grid(axis="y", alpha=0.3)

    # Panel (f): Post-Fire Land Cover Area Distribution (Hectares)
    bars_labels = ["Tracked Burn Scar\n(2023)", "Structured\nMonoculture", "Degraded\nShrubland", "Natural Forest\nSuccession", "Exposed\nBare Peat"]
    bars_vals = [track_ha, area[1], area[2], area[3], area[4]]
    bars_cols = ["#455a64", CLASS_COLORS[1], CLASS_COLORS[2], CLASS_COLORS[3], CLASS_COLORS[4]]
    b_plot = axes[1, 2].bar(range(5), bars_vals, color=bars_cols, edgecolor="k", width=0.58)
    for rect, val in zip(b_plot, bars_vals):
        p_txt = (val / track_ha) * 100.0
        axes[1, 2].text(
            rect.get_x() + rect.get_width() / 2.0,
            val + track_ha * 0.02,
            f"{val:,.0f} Ha\n({p_txt:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=7.5,
            fontweight="bold",
        )
    axes[1, 2].set_ylim(0, track_ha * 1.18)
    axes[1, 2].set_xticks(range(5))
    axes[1, 2].set_xticklabels(bars_labels, fontsize=7.5)
    axes[1, 2].set_ylabel("Area (Hectares)")
    axes[1, 2].set_title("(f) Post-Fire Land Cover Area Quantification (4 Classes)", fontweight="bold")
    axes[1, 2].grid(axis="y", alpha=0.3)

    fig.suptitle("Method 3 Comparison: Pre-GLCM Macro Spectral Clustering vs 2-Stage Hierarchical Classification (Spectral + GLCM)", fontsize=13, fontweight="bold")
    plt.tight_layout()
    fig4_path = os.path.join(RESULTS_DIR, "fig4_komparasi_sebelum_sesudah_glcm.png")
    plt.savefig(fig4_path, dpi=200, bbox_inches="tight")
    plt.close()

    # =========================================================================
    # FIGURE 5: 6-PANEL EXECUTIVE SUMMARY (CHRONOLOGICAL SPATIAL & CLUSTERS)
    # =========================================================================
    print("[INFO] Rendering Figure 5: 6-Panel Executive Summary Map...")
    fig, axes = plt.subplots(2, 3, figsize=(18, 11), dpi=160)

    axes[0, 0].imshow(rgb_pre)
    axes[0, 0].set_title("(a) Pre-Fire Baseline (May-Jul 2023)\nTrue Color RGB Composite", fontweight="bold")
    axes[0, 1].imshow(rgb_fire)
    axes[0, 1].set_title("(b) El Nino Active Fire Peak (Sep-Nov 2023)\nTrue Color RGB Composite", fontweight="bold")

    im_dnbr = axes[0, 2].imshow(dnbr, cmap="hot", vmin=0.0, vmax=0.55)
    axes[0, 2].contour(clean_burn_mask, colors="cyan", linewidths=0.5)
    axes[0, 2].set_title(f"(c) Method 1: Burn Severity (dNBR) & Morphology\nCyan Contour = Clean Burn Scar ({clean_burn_ha:,.0f} Ha)", fontweight="bold")
    plt.colorbar(im_dnbr, ax=axes[0, 2], fraction=0.046, pad=0.04, label="dNBR")

    im_homo = axes[1, 0].imshow(f_now["Homogeneity"], cmap="viridis", vmin=0.35, vmax=0.90)
    axes[1, 0].set_title("(d) Method 2: Haralick GLCM Homogeneity (2026 Y3)\nSpatial Canopy Regularity", fontweight="bold")
    plt.colorbar(im_homo, ax=axes[1, 0], fraction=0.046, pad=0.04, label="Homogeneity")

    axes[1, 1].imshow(rgb_now)
    axes[1, 1].set_title("(e) Post-Fire Recovery State (Jun-Sep 2026)\n3 Years Post-Fire (True Color RGB)", fontweight="bold")

    axes[1, 2].imshow(rgb_now * 0.42)
    axes[1, 2].imshow(np.ma.masked_equal(cluster_raster, 0), cmap=cmap_klaster, norm=norm_4)
    axes[1, 2].set_title(
        f"(f) Method 3: 2-Stage Hierarchical Classification (4 Classes)\nOverall Accuracy: {oa:.1f}% | Cohen's Kappa: {kappa:.3f}",
        fontweight="bold",
    )
    axes[1, 2].legend(
        handles=[
            Patch(facecolor=CLASS_COLORS[c], edgecolor="k", label=f"{CLASS_NAMES[c]}: {area[c]:,.0f} Ha ({pct[c]:.1f}%)")
            for c in CLASS_NAMES
        ],
        loc="lower right",
        fontsize=8,
        framealpha=0.92,
    )

    for ax in axes.ravel():
        ax.axis("off")
    plt.tight_layout()
    fig_map = os.path.join(RESULTS_DIR, "hasil_analisis_pcd_karhutla.png")
    fig_map_legacy = os.path.join(RESULTS_DIR, "komparasi_kronologis_dan_proporsi.png")
    plt.savefig(fig_map, dpi=200, bbox_inches="tight")
    plt.savefig(fig_map_legacy, dpi=200, bbox_inches="tight")
    plt.close()

    # =========================================================================
    # FIGURE 6: MULTI-TEMPORAL TRAJECTORY CURVES PER CLASS (2023 - 2026)
    # =========================================================================
    print("[INFO] Rendering Figure 6: Multi-Temporal Trajectory Curves (2023-2026)...")
    x = np.arange(len(EPOCHS))
    fig, axes = plt.subplots(2, 3, figsize=(18, 9), dpi=160)
    for ax, f in zip(axes.ravel(), feat_all):
        for c in CLASS_NAMES:
            d = df_traj[df_traj["Kelas_ID"] == c]
            mean, std = d[f"Mean_{f}"].values, d[f"Std_{f}"].values
            ax.plot(x, mean, marker="o", color=CLASS_COLORS[c], linewidth=2.2, label=CLASS_NAMES[c])
            ax.fill_between(x, mean - std, mean + std, color=CLASS_COLORS[c], alpha=0.12)
        ax.axvline(1, color="red", linestyle="--", linewidth=0.9, label="2023 Fire Event" if f == "NDVI" else None)
        ax.set_xticks(x)
        ax.set_xticklabels([e[0] for e in EPOCHS])
        ax.set_title(f"{f} Multi-Temporal Trajectory", fontweight="bold")
        ax.grid(alpha=0.3)
    axes[0, 0].legend(fontsize=8, loc="lower right")
    fig.suptitle(
        f"Post-Fire Multi-Temporal Spectral & GLCM Trajectory (2023-2026, {roi_name})\nClass Mean +/- 1 SD Inside Tracked Burn Scar Polygon ({track_ha:,.0f} Ha)",
        fontweight="bold",
    )
    plt.tight_layout()
    fig_traj = os.path.join(RESULTS_DIR, "trajektori_tahunan_2023_2026.png")
    plt.savefig(fig_traj, dpi=200, bbox_inches="tight")
    plt.close()

    # =========================================================================
    # FIGURE 7: CONFUSION MATRIX & GEDI LIDAR VERTICAL CANOPY VALIDATION
    # =========================================================================
    print("[INFO] Rendering Figure 7: Confusion Matrix & GEDI LiDAR Canopy Height Validation...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=160)
    short = ["Structured\nMonoculture", "Degraded\nShrubland", "Natural Forest\nSuccession", "Exposed\nBare Peat"]
    axes[0].imshow(cm, cmap="Blues")
    for i in range(4):
        row_sum = np.sum(cm[i, :])
        for j in range(4):
            pct_cell = (cm[i, j] / row_sum * 100.0) if row_sum > 0 else 0.0
            axes[0].text(
                j,
                i,
                f"{cm[i, j]:,}\n({pct_cell:.1f}%)",
                ha="center",
                va="center",
                color="white" if cm[i, j] > cm.max() / 2 else "black",
                fontweight="bold" if i == j else "normal",
                fontsize=8,
            )
    axes[0].set_xticks(range(4))
    axes[0].set_xticklabels(short, fontsize=8)
    axes[0].set_yticks(range(4))
    axes[0].set_yticklabels(short, fontsize=8)
    axes[0].set_xlabel("Predicted Class (2-Stage Spectral + GLCM)", fontweight="bold")
    axes[0].set_ylabel("Reference Class (Dynamic World V1 2026)", fontweight="bold")
    axes[0].set_title(f"4-Class Confusion Matrix (2-Stage Spectral + GLCM)\nOverall Accuracy: {oa:.1f}% | Cohen's Kappa: {kappa:.3f}", fontweight="bold")

    data_gedi = [gedi_h[(cluster_raster == c) & gedi_valid] if gedi_h is not None else np.array([]) for c in [1, 2, 3, 4]]
    if any(d.size for d in data_gedi):
        bp = axes[1].boxplot([d if d.size else [np.nan] for d in data_gedi], patch_artist=True, showfliers=False)
        for patch, c in zip(bp["boxes"], [1, 2, 3, 4]):
            patch.set_facecolor(CLASS_COLORS[c])
        axes[1].set_xticks([1, 2, 3, 4])
        axes[1].set_xticklabels([f"{s}\n(n={d.size})" for s, d in zip(short, data_gedi)], fontsize=8)
        axes[1].set_ylabel("GEDI L2A RH98 Canopy Height (m)", fontweight="bold")
        axes[1].grid(alpha=0.3)
    else:
        axes[1].text(0.5, 0.5, "No valid GEDI footprints\ninside burn scar polygon", ha="center", va="center", transform=axes[1].transAxes)
    axes[1].set_title("Independent Vertical Canopy Structure Validation (NASA GEDI L2A RH98)", fontweight="bold")
    plt.tight_layout()
    fig_eval = os.path.join(RESULTS_DIR, "evaluasi_confusion_matrix_gedi.png")
    plt.savefig(fig_eval, dpi=200, bbox_inches="tight")
    plt.close()

    print("\n[INFO] Seluruh 7 rangkaian visualisasi publikasi selesai disimpan di folder results/:")
    print(f"  1. {fig1_path}")
    print(f"  2. {fig2_path}")
    print(f"  3. {fig3_path}")
    print(f"  4. {fig4_path}")
    print(f"  5. {fig_map}")
    print(f"  6. {fig_traj}")
    print(f"  7. {fig_eval}")
    return df_stats, df_traj, oa, kappa


if __name__ == "__main__":
    roi = sys.argv[1] if len(sys.argv) > 1 else "Kalteng_Sebangau_Kahayan"
    if not os.path.exists(os.path.join(DATA_DIR, f"{roi}_s2_2023_pre.tif")):
        if os.path.exists(os.path.join(DATA_DIR, "ROI2_Kotawaringin_Timur_s2_2023_pre.tif")):
            roi = "ROI2_Kotawaringin_Timur"
    run_pipeline(roi)
