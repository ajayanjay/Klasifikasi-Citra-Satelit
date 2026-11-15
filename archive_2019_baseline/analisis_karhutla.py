"""
=============================================================================
TUGAS BESAR PENGOLAHAN CITRA DIGITAL (PCD)
ANALISIS KRONOLOGIS TRANSAKSI LAHAN PASCA-KARHUTLA GAMBUT KALIMANTAN TENGAH
BERBASIS DATA RIIL SENTINEL-2 & K-MEANS CLUSTERING (>5 TAHUN)
=============================================================================
Tim Peneliti (Kelompok 3B - D4 Teknik Informatika POLBAN):
- Idotoho Reimon Simajuntak (241524047)
- Ihsan Fauzi (241524048)
- Muhammad Azzar MannalHadi (241524051)

Alur Evaluasi Kronologis PCD:
1. T0: Sebelum Terbakar 2019 (Hutan Rawa Gambut Hijau Alami Utuh 100%)
2. T1: Pas Kebakaran 2019 (Hangus Coklat Arang Segar Bebas Asap)
3. T2: Kondisi Sekarang 2025 (Citra Satelit RGB Asli Mata Manusia)
4. T3: Peta Tematik Nasib Lahan (3 Kelas K-Means PCD)
5. Evaluasi Kuantitatif: Defisit Hektar & Komparasi Proporsi Before vs After
=============================================================================
"""

import os
import sys
import numpy as np
import tifffile as tiff
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
os.makedirs(RESULTS_DIR, exist_ok=True)

PATH_KLASTER = os.path.join(DATA_DIR, 'Hasil_Klaster_3Kelas_Karhutla.tif')
PATH_S2 = os.path.join(DATA_DIR, 'Citra_Sentinel2_Kalteng_2025.tif')
PATH_2019_PRE = os.path.join(DATA_DIR, 'Citra_Sentinel2_Kalteng_2019_Before.tif')
PATH_2019_POST = os.path.join(DATA_DIR, 'Citra_Sentinel2_Kalteng_2019_PasBakar.tif')
OUTPUT_PNG = os.path.join(RESULTS_DIR, 'komparasi_kronologis_dan_proporsi.png')

def stretch_rgb(r, g, b, p_low=2, p_high=98):
    rgb = np.stack([r, g, b], axis=-1).astype(np.float32)
    out = np.zeros_like(rgb, dtype=np.float32)
    for i in range(3):
        ch = rgb[:, :, i]
        valid = ch[~np.isnan(ch) & (ch > 0)]
        if len(valid) == 0:
            continue
        low = np.percentile(valid, p_low)
        high = np.percentile(valid, p_high)
        norm = np.clip((ch - low) / (high - low + 1e-6), 0, 1)
        norm[np.isnan(norm)] = 0
        out[:, :, i] = norm
    return out

def main():
    print("=" * 80)
    print("🛰️ MEMULAI ANALISIS KRONOLOGIS & PROPORSI BEFORE vs AFTER PASCA-KARHUTLA")
    print("   Lokasi: Kalimantan Tengah (Palangka Raya - Pulang Pisau)")
    print("=" * 80)

    if not os.path.exists(PATH_KLASTER) or not os.path.exists(PATH_S2):
        print("❌ Berkas GeoTIFF belum lengkap di folder 'data/'.")
        print("   Jalankan 'python get_data.py' untuk instruksi pengunduhan data.")
        sys.exit(1)

    print("\n[Tahap 1] Membaca GeoTIFF Riil Sentinel-2 dan Raster Klaster...")
    classes = tiff.imread(PATH_KLASTER)
    s2 = tiff.imread(PATH_S2)
    H, W = classes.shape
    print(f"          Dimensi Grid Raster : {W} x {H} piksel")
    print(f"          Resolusi Spasial    : 10 meter/piksel (Surface Reflectance L2A)")

    # Ekstraksi kanal 2025: [B2-Blue, B3-Green, B4-Red, B8-NIR, B11-SWIR1, B12-SWIR2]
    b2_now = s2[:, :, 0].astype(np.float32)
    b3_now = s2[:, :, 1].astype(np.float32)
    b4_now = s2[:, :, 2].astype(np.float32)
    b8_now = s2[:, :, 3].astype(np.float32)
    b11_now = s2[:, :, 4].astype(np.float32)

    # 1. Perhitungan Statistik Hektar Riil (1 piksel = 10m x 10m = 100 m2 = 0.01 Ha)
    print("\n[Tahap 2] Menghitung Statistik Hektar & Proporsi Tutupan Lahan...")
    PIXEL_TO_HA = 0.01
    mask_burned = (classes > 0)
    
    px_hijau = int(np.sum(classes == 1))
    px_semak = int(np.sum(classes == 2))
    px_kota  = int(np.sum(classes == 3))
    total_px = px_hijau + px_semak + px_kota

    ha_hijau = px_hijau * PIXEL_TO_HA
    ha_semak = px_semak * PIXEL_TO_HA
    ha_kota  = px_kota * PIXEL_TO_HA
    total_ha = total_px * PIXEL_TO_HA

    pct_hijau = (ha_hijau / total_ha) * 100
    pct_semak = (ha_semak / total_ha) * 100
    pct_kota  = (ha_kota / total_ha) * 100

    # 2. Citra Visual Spektral Asli (Murni 100% Sensor Satelit Sentinel-2)
    print("\n[Tahap 3] Memuat Citra Satelit Murni (True Color & Komposit Spektral)...")
    
    # A. Citra After 2025 (Warna Nyata True Color RGB: B4, B3, B2)
    rgb_now_vis = stretch_rgb(b4_now, b3_now, b2_now, 2, 98)

    # B & C. Citra Riil 2019 Before & Pasca-Bakar jika sudah diunduh dari GEE
    has_real_2019 = os.path.exists(PATH_2019_PRE) and os.path.exists(PATH_2019_POST)
    if has_real_2019:
        print("          ✅ Memuat citra riil Before 2019 & Pasca-Bakar 2019 dari GEE...")
        s2_pre = tiff.imread(PATH_2019_PRE).astype(np.float32)
        s2_post = tiff.imread(PATH_2019_POST).astype(np.float32)
        rgb_before_vis = stretch_rgb(s2_pre[:,:,0], s2_pre[:,:,1], s2_pre[:,:,2], 2, 98)
        rgb_fire_vis = stretch_rgb(s2_post[:,:,0], s2_post[:,:,1], s2_post[:,:,2], 2, 98)
        title_p1 = ("1. Sebelum Terbakar (Agustus 2019)", "Citra Murni Sentinel-2 RGB (Hutan Alami Riil)")
        title_p2 = ("2. Saat Kebakaran (Okt-Nov 2019)", "Citra Murni Sentinel-2 RGB (Arang Hitam Riil)")
    else:
        print("          ℹ️ Citra 2019 belum diunduh. Menampilkan Komposit Spektral Murni (CIR & SWIR)...")
        # Komposit Inframerah Dekat (CIR: B8, B4, B3) -> Standar Vegetasi Sentinel-2
        rgb_before_vis = stretch_rgb(b8_now, b4_now, b3_now, 2, 98)
        # Komposit Inframerah Gelombang Pendek (SWIR: B12, B8, B4) -> Standar Deteksi Luka Bakar
        rgb_fire_vis = stretch_rgb(s2[:, :, 5].astype(np.float32), b8_now, b4_now, 2, 98)
        title_p1 = ("1. Citra Murni CIR Infrared (B8-B4-B3)", "Kanal NIR Asli: Vegetasi = Merah, Luka Bakar = Gelap")
        title_p2 = ("2. Citra Murni SWIR Burn (B12-B8-B4)", "Kanal Gelombang Pendek: Lahan Gambut Kering = Oranye/Coklat")

    # D. Peta Tematik 3 Kelas Nasib Lahan
    class_map_vis = rgb_now_vis.copy()
    class_map_vis[classes == 1] = [0.0, 0.90, 0.46] # Hijau Neon = Pulih
    class_map_vis[classes == 2] = [1.0, 0.55, 0.00] # Oranye/Coklat = Semak Gambut Kritis
    class_map_vis[classes == 3] = [1.0, 0.10, 0.25] # Merah Terang = Perkotaan/Kupasan

    # 3. Perhitungan Perubahan Proporsi & Defisit Hektar (Before vs After)
    ha_before_veg = total_ha
    ha_before_semak = 0.0
    ha_before_kota = 0.0

    delta_veg_ha = ha_hijau - ha_before_veg     # Defisit kehilangan hutan
    delta_semak_ha = ha_semak - ha_before_semak # Pertambahan semak kritis
    delta_kota_ha = ha_kota - ha_before_kota    # Pertambahan lahan terbangun

    print("\n" + "=" * 80)
    print("📊 TABEL PERBANDINGAN PROPORSI (BEFORE 2019 vs AFTER >5 TAHUN 2025):")
    print("=" * 80)
    print(f"Total Luas Area Luka Bakar : {total_ha:,.2f} Hektar (100.0%)\n")
    print(f"1. VEGETASI HIJAU LEBAT (HUTAN RAWA GAMBUT):")
    print(f"   • Sebelum 2019 : {ha_before_veg:,.2f} Ha (100.0%)")
    print(f"   • Setelah 2025 : {ha_hijau:,.2f} Ha ({pct_hijau:.2f}%)")
    print(f"   👉 PERUBAHAN   : {delta_veg_ha:,.2f} Ha (DEFISIT HILANG: {abs(delta_veg_ha)/total_ha*100:.2f}%)\n")
    print(f"2. LAHAN TERBENGKALAI / SEMAK GAMBUT KRITIS:")
    print(f"   • Sebelum 2019 : 0.00 Ha (0.0%)")
    print(f"   • Setelah 2025 : {ha_semak:,.2f} Ha ({pct_semak:.2f}%)")
    print(f"   👉 PERUBAHAN   : +{delta_semak_ha:,.2f} Ha (+{pct_semak:.2f}%) -> ZONA RAWAN BAKAR ULANG\n")
    print(f"3. ALIH FUNGSI PERKOTAAN / KUPASAN TANAH MATI:")
    print(f"   • Sebelum 2019 : 0.00 Ha (0.0%)")
    print(f"   • Setelah 2025 : {ha_kota:,.2f} Ha ({pct_kota:.2f}%)")
    print(f"   👉 PERUBAHAN   : +{delta_kota_ha:,.2f} Ha (+{pct_kota:.2f}%) -> PEMBUKAAN LAHAN & BANGUNAN")
    print("=" * 80)

    # 4. Render Gambar Publikasi 6-Panel
    print("\n[Tahap 4] Merender Gambar Multi-Panel Publikasi 6-Panel...")
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(2, 3, height_ratios=[1.2, 1.0])

    # Panel 1: Before / CIR
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.imshow(rgb_before_vis)
    ax1.set_title(f"{title_p1[0]}\n{title_p1[1]}", fontsize=11, fontweight="bold")
    ax1.axis("off")

    # Panel 2: Pasca-Bakar / SWIR
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.imshow(rgb_fire_vis)
    ax2.set_title(f"{title_p2[0]}\n{title_p2[1]}", fontsize=11, fontweight="bold", color="darkred")
    ax2.axis("off")

    # Panel 3: After 2025
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.imshow(rgb_now_vis)
    ax3.set_title("3. T2: Kondisi Sekarang (2025)\nCitra Satelit RGB Nyata Mata Manusia (>5 Tahun)", fontsize=11, fontweight="bold")
    ax3.axis("off")

    # Panel 4: Peta Tematik 3 Kelas
    ax4 = fig.add_subplot(gs[1, 0])
    ax4.imshow(class_map_vis)
    ax4.set_title(f"4. Nasib Bekas Karhutla (Peta 3 Kelas)\nHijau Pulih ({pct_hijau:.0f}%) | Semak Coklat ({pct_semak:.0f}%) | Kota ({pct_kota:.0f}%)", fontsize=11, fontweight="bold")
    ax4.axis("off")

    # Panel 5: Diagram Batang Proporsi Before vs After
    ax5 = fig.add_subplot(gs[1, 1])
    kategori = ['Lahan Hijau\n(Vegetasi)', 'Semak Gambut\n(Terbengkalai)', 'Perkotaan /\nKupasan']
    prop_before = [100.0, 0.0, 0.0]
    prop_after  = [pct_hijau, pct_semak, pct_kota]
    
    x = np.arange(len(kategori))
    width = 0.35

    rects1 = ax5.bar(x - width/2, prop_before, width, label='Sebelum 2019 (Before)', color='#2E7D32', alpha=0.85)
    rects2 = ax5.bar(x + width/2, prop_after, width, label='Kondisi 2025 (After)', color=['#00E676', '#FF9100', '#FF1744'])

    ax5.set_ylabel('Proporsi Tutupan Lahan (%)', fontsize=10, fontweight="bold")
    ax5.set_title('5. Perbandingan Proporsi (%)\nBefore 2019 vs After 2025', fontsize=11, fontweight="bold")
    ax5.set_xticks(x)
    ax5.set_xticklabels(kategori, fontsize=9, fontweight="bold")
    ax5.legend(loc='upper right', fontsize=9)
    ax5.set_ylim(0, 115)
    ax5.grid(axis='y', linestyle='--', alpha=0.4)

    for r in rects1:
        h = r.get_height()
        if h > 0:
            ax5.annotate(f'{h:.1f}%', xy=(r.get_x() + r.get_width() / 2, h),
                         xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight="bold")
    for r in rects2:
        h = r.get_height()
        ax5.annotate(f'{h:.1f}%', xy=(r.get_x() + r.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight="bold")

    # Panel 6: Grafik Delta Perubahan Bersih (Hektar)
    ax6 = fig.add_subplot(gs[1, 2])
    perubahan_ha = [delta_veg_ha, delta_semak_ha, delta_kota_ha]
    warna_delta = ['#D32F2F', '#FF9100', '#C2185B']

    bars = ax6.bar(kategori, perubahan_ha, color=warna_delta, width=0.55, edgecolor='black', linewidth=1)
    ax6.axhline(0, color='black', linewidth=1)
    ax6.set_ylabel('Perubahan Luas Bersih (Hektar)', fontsize=10, fontweight="bold")
    ax6.set_title('6. Defisit & Kenaikan Luas Bersih (Ha)\nTransisi Pasca-Karhutla (>5 Tahun)', fontsize=11, fontweight="bold")
    ax6.grid(axis='y', linestyle='--', alpha=0.4)

    for b in bars:
        h = b.get_height()
        y_pos = h + 400 if h >= 0 else h - 1400
        sign = '+' if h >= 0 else ''
        ax6.annotate(f'{sign}{h:,.0f} Ha', xy=(b.get_x() + b.get_width() / 2, y_pos),
                     ha='center', va='bottom', fontsize=9, fontweight="bold")

    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=250)
    plt.close()
    print(f"✅ Gambar visual komparasi 6-panel berhasil disimpan ke: {OUTPUT_PNG}")

if __name__ == '__main__':
    main()

