"""
=============================================================================
MODUL GET DATA DAN VALIDASI CITRA SATELIT SENTINEL-2 (KARHUTLA GAMBUT KALTENG)
=============================================================================
Mata Kuliah : Pengolahan Citra Digital (PCD)
Institusi   : D4 Teknik Informatika - Politeknik Negeri Bandung (POLBAN)
Tim         : Kelompok 3B
              - Idotoho Reimon Simajuntak (241524047)
              - Ihsan Fauzi (241524048)
              - Muhammad Azzar MannalHadi (241524051)

Fungsi Script:
1. Memeriksa ketersediaan berkas GeoTIFF di folder 'data/'
2. Memberikan panduan cara export citra mentah dari Google Earth Engine (GEE)
3. Melakukan inspeksi otomatis: resolusi spasial, jumlah band, tipe data, dan statistik dasar
=============================================================================
"""

import os
import sys
import numpy as np

try:
    import tifffile as tiff
except ImportError:
    print("❌ Paket 'tifffile' belum terpasang. Jalankan: pip install tifffile imagecodecs")
    sys.exit(1)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

FILE_KLASTER = os.path.join(DATA_DIR, 'Hasil_Klaster_3Kelas_Karhutla.tif')
FILE_S2_2025 = os.path.join(DATA_DIR, 'Citra_Sentinel2_Kalteng_2025.tif')
FILE_S2_2019_PRE = os.path.join(DATA_DIR, 'Citra_Sentinel2_Kalteng_2019_Before.tif')
FILE_S2_2019_POST = os.path.join(DATA_DIR, 'Citra_Sentinel2_Kalteng_2019_PasBakar.tif')

def print_panduan_gee():
    print("""
=============================================================================
ℹ️ PANDUAN MENGAMBIL DATA ('GET DATA') DARI GOOGLE EARTH ENGINE (GEE)
=============================================================================
1. Buka Google Earth Engine Code Editor: https://code.earthengine.google.com/
2. Buat script baru dan salin seluruh isi berkas 'script_gee.js'.
3. Klik tombol 'Run'.
4. Di sebelah kanan atas editor GEE, buka tab 'Tasks'.
5. Terdapat 4 tugas ekspor GeoTIFF:
   - 'Citra_Sentinel2_Kalteng_2019_Before'   -> Citra asli satelit Sebelum Kebakaran 2019 (True Color RGB)
   - 'Citra_Sentinel2_Kalteng_2019_PasBakar' -> Citra asli satelit Pas Kebakaran 2019 (True Color RGB Arang)
   - 'Citra_Sentinel2_Kalteng_2025'          -> Citra multi-band 2025 (B2, B3, B4, B8, B11, B12)
   - 'Hasil_Klaster_3Kelas_Karhutla'        -> Peta raster hasil klaster K-Means PCD
6. Klik tombol 'Run' pada task yang ingin Anda ekspor ke Google Drive.
7. Setelah selesai (centang biru), unduh file .tif dari Google Drive ke folder 'data/' di repositori ini.
=============================================================================
""")

def validasi_berkas():
    print("=" * 75)
    print("🔍 MEMERIKSA STATUS BERKAS DATASET DI FOLDER 'data/'...")
    print("=" * 75)

    os.makedirs(DATA_DIR, exist_ok=True)

    # 1. Periksa File Klaster
    if os.path.exists(FILE_KLASTER):
        size_kb = os.path.getsize(FILE_KLASTER) / 1024
        print(f"✅ [DITEMUKAN] {os.path.basename(FILE_KLASTER)} ({size_kb:,.1f} KB)")
        try:
            klaster_data = tiff.imread(FILE_KLASTER)
            h, w = klaster_data.shape
            unique, counts = np.unique(klaster_data, return_counts=True)
            print(f"   • Dimensi Grid          : {w} x {h} piksel")
            print(f"   • Tipe Data             : {klaster_data.dtype}")
            total_burned = np.sum(klaster_data > 0)
            print(f"   • Total Piksel Terbakar : {total_burned:,} piksel ({total_burned*0.01:,.2f} Ha)")
            for u, c in zip(unique, counts):
                label = 'Background / Tidak Terbakar' if u == 0 else f'Kelas {u}'
                if u == 1: label += ' (Hijau Pulih / Suksesi)'
                elif u == 2: label += ' (Semak Terbengkalai / Rawan Bakar Ulang)'
                elif u == 3: label += ' (Lahan Terbuka / Perkotaan / Kupasan)'
                print(f"     - Nilai {u}: {c:,} piksel ({c/total_burned*100 if total_burned and u>0 else 0:.2f}%) -> {label}")
        except Exception as e:
            print(f"   ⚠️ Gagal membaca konten TIFF: {e}")
    else:
        print(f"❌ [TIDAK DITEMUKAN] {os.path.basename(FILE_KLASTER)}")

    print("-" * 75)

    # 2. Periksa File Sentinel-2 2025
    if os.path.exists(FILE_S2_2025):
        size_mb = os.path.getsize(FILE_S2_2025) / (1024 * 1024)
        print(f"✅ [DITEMUKAN] {os.path.basename(FILE_S2_2025)} ({size_mb:,.1f} MB)")
        try:
            s2_data = tiff.imread(FILE_S2_2025)
            print(f"   • Bentuk Array          : {s2_data.shape} (Tinggi, Lebar, Kanal)")
            print(f"   • Tipe Data             : {s2_data.dtype}")
            print(f"   • Susunan Band          : [B2-Blue, B3-Green, B4-Red, B8-NIR, B11-SWIR1, B12-SWIR2]")
            print(f"   • Resolusi Spasial      : 10 meter/piksel (Surface Reflectance L2A)")
        except Exception as e:
            print(f"   ⚠️ Gagal membaca konten TIFF: {e}")
    else:
        print(f"⚠️ [BELUM TERSEDIA] {os.path.basename(FILE_S2_2025)}")

    print("-" * 75)

    # 3. Periksa Citra Riil 2019 Before & Pasca-Bakar
    found_2019 = True
    for fpath in [FILE_S2_2019_PRE, FILE_S2_2019_POST]:
        if os.path.exists(fpath):
            size_mb = os.path.getsize(fpath) / (1024 * 1024)
            print(f"✅ [DITEMUKAN] {os.path.basename(fpath)} ({size_mb:,.1f} MB)")
        else:
            print(f"ℹ️ [OPSIONAL / DAPAT DIUNDUH DARI GEE] {os.path.basename(fpath)}")
            found_2019 = False

    print("=" * 75)
    if found_2019:
        print("🎉 SEMPURNA! Citra kronologis riil 2019 & 2025 lengkap tersedia!")
    else:
        print("💡 TIP: Untuk menampilkan citra satelit murni Before 2019 & Pasca-Bakar 2019 di Python,")
        print("   jalankan task export 'Citra_Sentinel2_Kalteng_2019_Before' & 'Citra_Sentinel2_Kalteng_2019_PasBakar' di GEE!")
        print_panduan_gee()
    print("=" * 75)

if __name__ == '__main__':
    validasi_berkas()

