# Analisis Trajektori dan Klasifikasi Tutupan Lahan Pasca-Karhutla Gambut Berbasis Sentinel-2 dan PCD

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Sentinel-2 L2A](https://img.shields.io/badge/Satellite-Sentinel--2%20L2A%20(10m)-emerald.svg)](https://sentinels.copernicus.eu/)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red.svg)](https://streamlit.io/)
[![Google Earth Engine](https://img.shields.io/badge/Platform-Google%20Earth%20Engine-orange.svg)](https://earthengine.google.com/)
[![Institution POLBAN](https://img.shields.io/badge/Institution-POLBAN%20D4%20TI-purple.svg)](https://www.polban.ac.id/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Tim Peneliti (Kelompok 3B)
Proyek Tugas Besar Mata Kuliah **Pengolahan Citra Digital (PCD)**  
**Program Studi D4 Teknik Informatika - Jurusan Teknik Komputer dan Informatika**  
**Politeknik Negeri Bandung (POLBAN)**

| No | Nama Mahasiswa | NIM | Peran Utama |
|:--:|:---|:---:|:---|
| 1 | **Idotoho Reimon Simajuntak** | `241524047` | Ekstraksi Ciri Spektral (NDVI, NDMI, BSI) dan Klasterisasi K-Means |
| 2 | **Ihsan Fauzi** | `241524048` | Arsitektur GEE Script, Filtering Awan/Aerosol, Pipeline Python dan Dashboard Streamlit |
| 3 | **Muhammad Azzar MannalHadi** | `241524051` | Morfologi Citra (Opening/Closing), Tekstur GLCM Orde-2 dan Evaluasi GEDI LiDAR |

---

## 1. Latar Belakang dan Urgensi Masalah

Bencana Kebakaran Hutan dan Lahan (**Karhutla**) pada ekosistem rawa gambut tropis di Kalimantan Tengah (koridor Sebangau - Kahayan) menimbulkan dampak kerusakan lingkungan jangka panjang. Hutan rawa gambut primer membutuhkan waktu 20 hingga 30 tahun untuk membentuk kembali struktur kanopi klimaks secara suksesi alami.

Penelitian ini memantau trajektori pemulihan vegetasi sepanjang 3 tahun pasca-kebakaran El Nino 2023 (rentang waktu 2023 hingga 2026) melalui data penginderaan jauh Sentinel-2 resolusi spasial 10 meter. Pendekatan yang digunakan adalah **murni Pengolahan Citra Digital (PCD)** tanpa model supervised machine learning/deep learning (bebas black-box seperti CNN, Random Forest, atau SVM), dengan tahapan:
1. **Method 1 (Burn Scar Delineation & Mathematical Morphology):** *Burn Severity Index* ($\Delta\text{NBR}$), penyaringan *NASA FIRMS Brightness Temperature (T21 > 310 K)*, serta pembentukan *Raw Burn Candidate Mask* yang dimurnikan melalui *Morphological Opening* ($5\times 5$), *Morphological Closing* ($7\times 7$), dan *Connected Component Filtering* menjadi *Clean Burn Scar Polygon*.
2. **Method 2 (Multi-Temporal Spectral & Haralick GLCM Feature Extraction):** Ekstraksi indeks spektral biofisik (*NDVI*, *NDMI*, *BSI*) dan tekstur *Gray-Level Co-occurrence Matrix (GLCM)* Orde-2 Haralick 4 arah (*Homogeneity*, *Contrast*, *Shannon Entropy*) pada kanal NIR sepanjang deret waktu 5 epoch (`2023 Pre`, `2023 Fire`, `2024 Y1`, `2025 Y2`, `2026 Y3`).
3. **Method 3 (2-Stage Hierarchical Classification):** 
   - **Stage 1:** Isolasi spektral area non-vegetasi sebagai **Class 4: Exposed Bare Peat / Unrecovered Land (Merah)** tanpa dipaksa masuk ke komputasi tekstur kanopi GLCM.
   - **Stage 2:** Klasterisasi K-Means ($k=3$) khusus pada piksel bervegetasi untuk memisahkan **Class 1: Structured Monoculture Vegetation (Kuning)** vs **Class 2: Degraded Shrubland (Oranye)** vs **Class 3: Natural Forest Succession (Hijau)**.
4. **Independent Validation:** Evaluasi *4-Class Confusion Matrix* terhadap *Google Dynamic World V1 2026* dan validasi profil kanopi vertikal menggunakan *NASA GEDI L2A RH98 Canopy Height*.

---

## 2. Temuan Kuantitatif Utama (Kondisi 2026 pada Luka Bakar 2023)

Berdasarkan komputasi piksel riil pada lanskap master 30 x 30 km (luas *Clean Burn Scar Polygon* teramati penuh = **5.888,20 Ha**):

| ID | Post-Fire Land Cover Class (Domain Taxonomy) | Area (Ha) | Proportion (%) | Mean NDVI | Mean NDMI | Mean BSI | GLCM Homogeneity | GLCM Entropy | GEDI RH98 (m) |
|:--:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | **Structured Monoculture Vegetation** | **1.344,57** | **22,83%** | 0,6278 | 0,1145 | -0,0766 | **0,7971** | **2,3653** | 5,15 m |
| **2** | **Degraded Shrubland** | **1.270,06** | **21,57%** | 0,6194 | 0,1231 | -0,0785 | 0,6265 | 3,7987 | 5,92 m |
| **3** | **Natural Forest Succession** | **1.211,82** | **20,58%** | **0,7317** | **0,2541** | -0,2096 | 0,6495 | 3,5812 | 6,39 m |
| **4** | **Exposed Bare Peat / Unrecovered Land** | **2.061,75** | **35,01%** | 0,4724 | -0,0603 | **+0,0790** | 0,7202 | 3,0102 | 7,12 m* |
| **-** | **Total Tracked Burn Scar Polygon (2023)** | **5.888,20** | **100,00%** | - | - | - | - | - | - |

- **Evaluasi Confusion Matrix (Dynamic World V1 2026):** Overall Accuracy (OA) = **58,37%** | Cohen's Kappa = **0,4448**.
- **Structured Monoculture Conversion:** Sebesar **1.344,57 Ha (22,83%)** bekas luka bakar bertransisi menjadi *Structured Monoculture Vegetation* dengan *GLCM Homogeneity* sangat tinggi ($0,7971$) dan *GLCM Shannon Entropy* rendah ($2,3653$).
- **Exposed Bare Peat / Unrecovered Land:** Sebesar **2.061,75 Ha (35,01%)** masih berupa *Exposed Bare Peat / Unrecovered Land* dengan nilai *BSI* positif ($+0,0790$) dan defisit kelembaban tajuk ($\text{NDMI} = -0,0603$).

---

## 3. Rangkaian Visualisasi Hasil Penelitian (Folder `results/`)

Repositori ini menghasilkan 7 visualisasi saintifik standar publikasi:

1. **`fig1_komposit_multispektral.png`:** Eksplorasi 6 kanal dan indeks Sentinel-2 (True Color RGB, False Color CIR, Penetrasi SWIR, NDVI, NDMI, BSI).
2. **`fig2_progres_workflow_morfologi.png`:** Rangkaian 8 panel workflow deliniasi (Pra RGB, Puncak RGB arang hitam, False Color SWIR, Suhu termal FIRMS, dNBR, Kandidat kasar vs noise, Morfologi opening-closing, dan Poligon bersih pada kondisi 2026).
3. **`fig3_ekstraksi_fitur_spektral_glcm.png`:** Peta spasial 6 fitur input K-Means (NDVI, NDMI, BSI, GLCM Homogeneity, Contrast, dan Entropy).
4. **`fig4_komparasi_sebelum_sesudah_glcm.png`:** Integrasi sebelum vs sesudah GLCM hierarkis (mempertahankan kupasan tanah merah dan mengurai vegetasi hijau menjadi monokultur dan suksesi alami).
5. **`hasil_analisis_pcd_karhutla.png`:** Peta spasial kronologis utama 6 panel (2023 Pra s/d 2026 Y3).
6. **`trajektori_tahunan_2023_2026.png`:** Kurva dinamika 4 kelas sepanjang 5 epoch observasi temporal.
7. **`evaluasi_confusion_matrix_gedi.png`:** Confusion Matrix 4x4 dan validasi profil kanopi NASA GEDI LiDAR.

---

## 4. Dashboard Interaktif Streamlit (`app.py`)

Aplikasi web interaktif telah disediakan untuk mempermudah eksplorasi visual, inspeksi kuantitatif, komparasi antar-studi kasus, dan pengunduhan data.

### Cara Menjalankan Dashboard:
```bash
# Pastikan dependensi terpasang
pip install -r requirements.txt

# Jalankan server Streamlit
streamlit run app.py
```

Dashboard dapat diakses melalui browser di `http://localhost:8501` dengan fitur utama:
- **Navigasi Studi Kasus:** Beralih antara Studi Kasus Mutakhir (2023-2026), Studi Kasus Baseline Arsip (2019-2025), dan Komparasi Lintas Periode.
- **6 Tab Interaktif:** Ringkasan metrik, progres deliniasi & morfologi, ekstraksi spektral & GLCM, klasifikasi hierarkis, kurva trajektori deret waktu, dan evaluasi akurasi GEDI LiDAR.
- **Fitur Ekspor Data:** Pengunduhan file CSV statistik klaster dan data trajektori multi-tahun.

---

## 5. Arsip Baseline 2019 (`archive_2019_baseline/`)

Penelitian baseline sebelumnya yang menganalisis dampak Karhutla El Nino 2019 terhadap pemulihan 5 tahun (>5 tahun, 2019 s/d 2025) disimpan secara terpisah di folder `archive_2019_baseline/`:
- **Luas Terbakar Baseline 2019:** 20.188,42 Ha.
- **Metode Baseline:** dNBR + K-Means spektral 3 kelas (Hijau Pulih 17,44%, Semak Terbengkalai 45,91%, Kupasan/Kota 36,65%).
- Seluruh kode, notebook, raster klaster, dan grafik visualisasi baseline 2019 tetap tersimpan utuh dan dapat diinspeksi melalui `app.py`.

---

## 6. Struktur Direktori Repositori

```text
Klasifikasi-Citra-Satelit/
├── .gitignore                                 # Mengabaikan cache lokal dan GeoTIFF mentah (>50MB)
├── README.md                                  # Dokumentasi komprehensif penelitian
├── requirements.txt                           # Daftar dependensi Python (streamlit, cv2, tifffile, dll)
├── app.py                                     # Aplikasi dashboard interaktif Streamlit
├── analisis_karhutla.py                       # Skrip CLI pemrosesan citra digital & plotting grafik
├── analisis_karhutla.ipynb                    # Jupyter Notebook laporan interaktif
├── get_data.py                                # Skrip verifikasi GeoTIFF lokal & parameter akuisisi
├── export_all_data_gee.js                     # Skrip export Google Earth Engine 8 layer GeoTIFF 10m
├── inspeksi_kebakaran_2023_interaktif.js      # Skrip visualisasi interaktif GEE Code Editor
├── data/
│   ├── statistik_klaster_2023_2026.csv        # Tabel statistik kuantitatif 4 kelas
│   ├── trajektori_tahunan_2023_2026.csv       # Tabel trajektori rata-rata 5 epoch
│   └── Hasil_Klaster_3Kelas_Karhutla.tif      # Raster klasifikasi akhir 10 meter
├── results/
│   ├── fig1_komposit_multispektral.png        # Gambar 1 publikasi
│   ├── fig2_progres_workflow_morfologi.png    # Gambar 2 publikasi
│   ├── fig3_ekstraksi_fitur_spektral_glcm.png # Gambar 3 publikasi
│   ├── fig4_komparasi_sebelum_sesudah_glcm.png# Gambar 4 publikasi
│   ├── hasil_analisis_pcd_karhutla.png        # Gambar 5 publikasi
│   ├── trajektori_tahunan_2023_2026.png       # Gambar 6 publikasi
│   └── evaluasi_confusion_matrix_gedi.png     # Gambar 7 publikasi
└── archive_2019_baseline/                     # Arsip studi kasus baseline 2019 - 2025
    ├── README.md                              # Dokumentasi studi kasus 2019
    ├── analisis_karhutla.py                   # Skrip analisis 2019
    ├── analisis_karhutla.ipynb                # Notebook analisis 2019
    ├── data/Hasil_Klaster_3Kelas_Karhutla.tif # Raster klaster 2019
    └── results/                               # Grafik visualisasi 2019
```

---

## 7. Panduan Menjalankan Analisis CLI

```bash
# 1. Jalankan pipeline lengkap analisis citra digital (menghasilkan seluruh visualisasi & CSV)
python analisis_karhutla.py

# 2. Jalankan dashboard visualisasi Streamlit
streamlit run app.py
```
