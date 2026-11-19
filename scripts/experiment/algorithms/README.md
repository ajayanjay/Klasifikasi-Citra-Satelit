# Algoritma Deteksi Bangunan Berbasis PCD & Classical Machine Learning

Daftar implementasi algoritma dari Key Papers (`papers/key/`):

1. **`paper_lab_kmeans.py`**
   - **Paper:** Adam Jaelani (2020), *Deteksi dan Klasifikasi Tipe Bangunan pada Citra Satelit Menggunakan Metode K-Nearest Neighbor*.
   - **Metode:** PCD murni (CIE L\*a\*b\* color transformation, K-Means clustering pada kanal kromatik $a^*b^*$, hole filling morfologi, filter luas minimum).
   - **Karakter:** Sangat cepat, berfokus pada atap genteng kromatik (merah/oranye/terakota).

2. **`paper_baluyan_svm.py`**
   - **Paper:** Hayk Baluyan, Bikash Joshi, Amer Al Hinai, Wei Lee Woon (2013), *Novel Approach for Rooftop Detection Using Support Vector Machine*, ISRN Machine Vision.
   - **Metode:** Hybrid PCD + Classical ML. Bilateral filtering untuk mempertahankan tepi, segmentasi klaster K-Means ($k=4$), ekstraksi 8 fitur geometris & spektral per kandidat (Area, Perimeter, Visible Vegetation Index, Solidity, Grayscale Mean, Grayscale Variance, Extent, Eccentricity), klasifikasi SVM kernel RBF, dan Pass 2 (metode histogram intensitas atap untuk merecovery kandidat atap yang terlewat).
   - **Karakter:** Mendeteksi objek atap diskret dengan batas geometris yang rapi, meminimalkan false positive jalan/vegetasi.

3. **`paper_morphological_mabi.py`**
   - **Paper:** Weixuan Ma, Youchuan Wan, Jiayi Li, Sa Zhu, Mingwei Wang (2019), *An Automatic Morphological Attribute Building Index (MABI) Approach for Satellite High Spatial Resolution Imagery*, Remote Sensing (MDPI).
   - **Metode:** PCD Morfologi Matematika Multiskala Tingkat Lanjut. Membangun profil atribut diferensial (DAP) pada 4 orientasi arah linear ($0^\circ, 45^\circ, 90^\circ, 135^\circ$) pada variasi skala spasial. Menghitung $MABI_{bright}$ (white top-hat) dan $MABI_{dark}$ (black top-hat untuk atap gelap), supresi koridor jalan berbasis anisotropi arah, dan verifikasi bayangan (MASI).
   - **Karakter:** Otomatis tanpa training (unsupervised), sangat efektif mengekstraksi blok permukiman padat dan atap seng/metal kontras tinggi.

4. **`paper_turker_svm_pca.py`**
   - **Paper:** M. Turker & D. Koc-San (2010), *Building Detection from Pan-Sharpened IKONOS Imagery Through Support Vector Machines Classification*, ISPRS.
   - **Metode:** Classical ML (Pixel-level SVM). Membangun stack fitur multispektral 7-dimensi: Red, Green, Blue, Visible NDVI/GLI ($(2G-R-B)/(2G+R+B)$), CIE L\*a\*b\* chroma, dan tekstur varians spasial lokal. Diklasifikasikan menggunakan SVM kernel RBF, dilanjutkan post-processing morfologi (opening, closing, hole filling, filter rasio aspek).
   - **Karakter:** Pemetaan cakupan atap piksel demi piksel yang andal dan menekan false alarm vegetasi secara ketat.

---

## Cara Menjalankan Benchmark Dataset

```powershell
# Menjalankan algoritma individual pada dataset/raw:
python scripts\experiment\algorithms\paper_lab_kmeans.py --output output_results\paper_lab_kmeans
python scripts\experiment\algorithms\paper_baluyan_svm.py --output output_results\paper_baluyan_svm
python scripts\experiment\algorithms\paper_morphological_mabi.py --output output_results\paper_morphological_mabi
python scripts\experiment\algorithms\paper_turker_svm_pca.py --output output_results\paper_turker_svm_pca

# Evaluasi kuantitatif terhadap Ground Truth dataset/eval:
python scripts\metric_eval\evaluate_masks.py --predictions output_results\paper_lab_kmeans
python scripts\metric_eval\evaluate_masks.py --predictions output_results\paper_baluyan_svm
python scripts\metric_eval\evaluate_masks.py --predictions output_results\paper_morphological_mabi
python scripts\metric_eval\evaluate_masks.py --predictions output_results\paper_turker_svm_pca
```

---

## Cara Menjalankan Pengujian Permukiman Padat Jakarta

```powershell
python scripts\experiment\test_dense_settlement_jakarta.py
```
Hasil visualisasi, mask, kontur batas bangunan, overlay, perbandingan grid side-by-side, dan tabel CSV disimpan di `output_results/jakarta_dense_settlement_comparison/`.
