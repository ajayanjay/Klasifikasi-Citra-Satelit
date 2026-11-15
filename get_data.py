import os
import sys
import requests
import ee

GEE_PROJECT_ID = os.environ.get("GEE_PROJECT", "pcd-pra-tubes-511102")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

ROIS = {
    "ROI1_Pulang_Pisau": {
        "desc": "Kawasan Gambut Eks-PLG (Pulang Pisau)",
        "coords": [114.28, -2.75, 114.42, -2.62],
    },
    "ROI2_Kotawaringin_Timur": {
        "desc": "Kawasan Ekspansi Monokultur (Kotawaringin Timur / Sampit)",
        "coords": [112.78, -2.32, 112.92, -2.19],
    },
    "ROI3_Seruyan": {
        "desc": "Zona Transisi Perkebunan dan Hutan Rawa (Seruyan)",
        "coords": [112.38, -2.66, 112.52, -2.53],
    }
}


def init_earth_engine():
    print("[INFO] Menghubungkan ke Google Earth Engine API...")
    try:
        ee.Initialize(project=GEE_PROJECT_ID)
        print(f"[INFO] Terhubung ke project: {GEE_PROJECT_ID}")
    except Exception:
        print("[WARN] Sesi belum terautentikasi. Membuka proses otorisasi...")
        try:
            ee.Authenticate()
            ee.Initialize(project=GEE_PROJECT_ID)
            print(f"[INFO] Autentikasi berhasil pada project: {GEE_PROJECT_ID}")
        except Exception as err:
            print(f"[ERROR] Gagal melakukan autentikasi GEE: {err}")
            sys.exit(1)


def mask_s2_clouds(image):
    qa = image.select("QA60")
    cloud_bit = 1 << 10
    cirrus_bit = 1 << 11
    mask = qa.bitwiseAnd(cloud_bit).eq(0).And(qa.bitwiseAnd(cirrus_bit).eq(0))

    scl = image.select("SCL")
    valid_scl = scl.neq(3).And(scl.neq(8)).And(scl.neq(9)).And(scl.neq(10))
    return image.updateMask(mask).updateMask(valid_scl)


def get_s2_composite(s2_col, geom, start_date, end_date, max_cloud=40):
    bands = ["B2", "B3", "B4", "B8", "B11", "B12"]
    return (
        s2_col.filterDate(start_date, end_date)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", max_cloud))
        .map(mask_s2_clouds)
        .select(bands)
        .median()
        .unmask(0)
        .clip(geom)
        .multiply(0.0001)
        .toFloat()
    )


def download_tif(ee_image, region, filename, scale=15):
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        print(f"[INFO] File sudah tersedia, melewati: {filename}")
        return filepath

    print(f"[INFO] Mengunduh {filename} (resolusi {scale}m)...")
    try:
        url = ee_image.getDownloadURL({
            "name": filename.replace(".tif", ""),
            "scale": scale,
            "crs": "EPSG:4326",
            "region": region,
            "format": "GEO_TIFF"
        })
        resp = requests.get(url, stream=True, timeout=180)
        resp.raise_for_status()

        with open(filepath, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        print(f"[INFO] Tersimpan: {filepath} ({size_mb:.2f} MB)")
        return filepath
    except Exception as err:
        print(f"[ERROR] Gagal mengunduh {filename}: {err}")
        return None


def fetch_roi_data(roi_name, roi_cfg, scale=15):
    print(f"\n--- Memproses {roi_name}: {roi_cfg['desc']} ---")
    min_lon, min_lat, max_lon, max_lat = roi_cfg["coords"]
    geom = ee.Geometry.Rectangle([min_lon, min_lat, max_lon, max_lat])

    s2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterBounds(geom)

    # Deret Waktu Tahunan (2023 Pre -> 2023 Fire -> 2024 Y1 -> 2025 Y2 -> 2026 Y3)
    # max_cloud dinaikkan ke 85% agar median filter memiliki sampel bebas awan yang cukup
    pre_2023 = get_s2_composite(s2, geom, "2023-04-01", "2023-07-31", max_cloud=85)
    fire_2023 = get_s2_composite(s2, geom, "2023-08-15", "2023-11-30", max_cloud=85)
    y1_2024 = get_s2_composite(s2, geom, "2024-05-01", "2024-10-15", max_cloud=85)
    y2_2025 = get_s2_composite(s2, geom, "2025-05-01", "2025-10-15", max_cloud=85)
    now_2026 = get_s2_composite(s2, geom, "2026-05-01", "2026-10-15", max_cloud=85)

    firms = (
        ee.ImageCollection("FIRMS")
        .filterBounds(geom)
        .filterDate("2023-08-01", "2023-11-30")
        .select("T21")
        .max()
        .unmask(0)
        .clip(geom)
        .toFloat()
    )

    jrc = (
        ee.Image("JRC/GSW1_4/GlobalSurfaceWater")
        .select("occurrence")
        .unmask(0)
        .clip(geom)
        .toFloat()
    )

    aux_img = firms.addBands(jrc).rename(["firms_t21", "jrc_water"])

    dw_col = (
        ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1")
        .filterBounds(geom)
        .filterDate("2026-06-01", "2026-09-30")
        .select("label")
    )
    dw_mode = dw_col.reduce(ee.Reducer.mode()).rename("dw_label").clip(geom).toInt16()

    # Tinggi kanopi GEDI L2A (RH98) hasil observasi LiDAR. Footprint GEDI bersifat
    # sampel jarang, sehingga piksel tanpa observasi diberi nilai -1 (no data).
    def mask_gedi(img):
        valid = img.select("quality_flag").eq(1).And(img.select("degrade_flag").eq(0))
        return img.updateMask(valid).select("rh98")

    gedi = (
        ee.ImageCollection("LARSE/GEDI/GEDI02_A_002_MONTHLY")
        .filterBounds(geom)
        .filterDate("2024-06-01", "2026-09-30")
        .map(mask_gedi)
        .median()
        .unmask(-1)
        .rename("gedi_rh98")
        .clip(geom)
        .toFloat()
    )

    download_tif(pre_2023, geom, f"{roi_name}_s2_2023_pre.tif", scale=scale)
    download_tif(fire_2023, geom, f"{roi_name}_s2_2023_fire.tif", scale=scale)
    download_tif(y1_2024, geom, f"{roi_name}_s2_2024_y1.tif", scale=scale)
    download_tif(y2_2025, geom, f"{roi_name}_s2_2025_y2.tif", scale=scale)
    download_tif(now_2026, geom, f"{roi_name}_s2_2026_now.tif", scale=scale)
    download_tif(aux_img, geom, f"{roi_name}_aux_firms_water.tif", scale=scale)
    download_tif(dw_mode, geom, f"{roi_name}_gt_dynamic_world_2026.tif", scale=scale)
    download_tif(gedi, geom, f"{roi_name}_gedi_rh98.tif", scale=scale)


def main():
    init_earth_engine()
    print("\nPilihan Unduhan Dataset Multi-Tahun (2023 - 2026):")
    print("1. Semua ROI (Pulang Pisau, Kotawaringin Timur, Seruyan)")
    print("2. ROI 2 (Kotawaringin Timur)")
    print("3. ROI 1 (Pulang Pisau)")
    print("4. ROI 3 (Seruyan)")

    if len(sys.argv) > 1:
        choice = sys.argv[1].strip()
    else:
        choice = input("Pilih nomor [1-4] (default 2): ").strip() or "2"

    if choice == "1":
        for k, v in ROIS.items():
            fetch_roi_data(k, v, scale=15)
    elif choice == "2":
        fetch_roi_data("ROI2_Kotawaringin_Timur", ROIS["ROI2_Kotawaringin_Timur"], scale=15)
    elif choice == "3":
        fetch_roi_data("ROI1_Pulang_Pisau", ROIS["ROI1_Pulang_Pisau"], scale=15)
    elif choice == "4":
        fetch_roi_data("ROI3_Seruyan", ROIS["ROI3_Seruyan"], scale=15)
    else:
        print("[ERROR] Pilihan tidak dikenal.")
        return

    print("\n[INFO] Seluruh proses pengunduhan deret waktu selesai. File tersimpan di folder data/.")


if __name__ == "__main__":
    main()
