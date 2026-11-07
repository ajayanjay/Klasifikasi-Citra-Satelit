# Panduan Replikasi Paper: Deteksi dan Klasifikasi Tipe Bangunan pada Citra Satelit Menggunakan Metode K-Nearest Neighbor (k-NN)

Dokumentasi ini dibuat untuk praktikum **Pengolahan Citra Digital (PCD), Semester 5, Program Studi Teknik Informatika (Diploma)** dalam rangka mereplikasi metodologi dari penelitian/skripsi:
* **Judul**: *Deteksi dan Klasifikasi Tipe Bangunan pada Citra Satelit Menggunakan Metode K-Nearest Neighbor*
* **Penulis Asli**: Adam Jaelani (NIM: 14650050), UIN Maulana Malik Ibrahim Malang (2020).

---

## 🔬 Analisis Kritis PCD: Mengapa Terjadi Perbedaan Resolusi Spasial?

> [!NOTE]
> Temuan ini sangat penting untuk dibahas pada laporan atau presentasi tugas Pengolahan Citra Digital (PCD):

1. **Pada Paper / Skripsi Asli**:
   * Penulis melakukan *screenshot/crop* gambar dari software **Google Earth Desktop** pada ketinggian 700–800 meter.
   * Citra tersebut beresolusi **ultra-tinggi ($\approx 0.2$ meter per piksel)**.
   * Oleh karena itu, satu rumah kecil di paper tersusun atas **1.600 - 2.100 piksel** (Lihat Tabel 3.4 skripsi). Jarak antar atap/gang tampak jelas terpisah.
2. **Pada Citra Publik Google Earth Engine (`Sentinel-2`)**:
   * Citra satelit Sentinel-2 memiliki resolusi **10 meter per piksel**.
   * Satu rumah tipe 36 atau 45 (ukuran $6\text{ m} \times 6\text{ m} = 36\text{ m}^2$) berukuran **kurang dari 1 piksel** ($1\text{ piksel} = 100\text{ m}^2$).
   * Akibatnya terjadi fenomena **piksel campuran (*mixed pixels*)**, di mana satu blok perumahan menyatu menjadi satu gumpalan poligon besar saat disegmentasi.

---

## 🎛️ Dua Mode Operasi pada Script

Untuk mengatasi hal tersebut, script ini menyediakan dua mode pada variabel `CONFIG.mode`:

1. **`mode: 'HIGH_RES_INDIVIDUAL'` (DEFAULT & REKOMENDASI)**:
   * Menggunakan poligon jejak atap individual bersumber dari satelit Google resolusi sub-meter (`GOOGLE/Research/open-buildings/v3/polygons`).
   * **Mengekstraksi 4 Ciri Geometris Paper**: Luas ($A$), Keliling ($P$), *Metric* ($M$), dan *Eccentricity* ($e$) untuk setiap rumah.
   * **Mengklasifikasikan tiap rumah dengan k-NN ($k=5$)**:
     * 🔴 **Merah (Tipe A)**: Bangunan Besar (Luas $> 300\text{ m}^2$)
     * 🟡 **Kuning (Tipe B)**: Bangunan Sedang (Luas $120 - 300\text{ m}^2$)
     * 🔵 **Cyan (Tipe C)**: Bangunan Kecil (Luas $< 120\text{ m}^2$)
   * **Hasil**: Setiap rumah memiliki poligon presisi yang pas di atapnya dengan warna sesuai klasifikasi tipe.

2. **`mode: 'PIXEL_SEGMENTATION'`**:
   * Menjalankan rantai segmentasi piksel murni ($RGB \to CIELab \to K\text{-Means} \to \text{Morfologi}$) pada raster Sentinel-2.
   * Sangat berguna sebagai bahan pembanding di bab pembahasan laporan mengenai limitasi resolusi spasial citra satelit optik 10 meter.

---

## 📁 Berkas yang Tersedia di `gee_scripts/`

| Nama Berkas | Lingkungan / Format | Deskripsi |
| :--- | :--- | :--- |
| **`building_detection_knn.js`** | **GEE Code Editor (Web)** | **(Rekomendasi Utama)** Script JavaScript siap pakai untuk langsung di-copy-paste ke [Google Earth Engine Code Editor](https://code.earthengine.google.com/). Dilengkapi dengan UI Legenda interaktif, Map Click Inspector, dan multi-layer visualizer. |
| **`building_detection_knn.py`** | **Python (Jupyter / Colab)** | Script Python alternatif menggunakan library `ee` dan `geemap` untuk mahasiswa yang ingin menjalankan simulasi di Google Colab atau notebook lokal. |
| **`README.md`** | Markdown | Panduan lengkap cara kerja, pemetaan rumus, konfigurasi parameter, dan langkah pengujian. |

---

## 🚀 Cara Menjalankan Script di GEE Code Editor (Step-by-Step)

1. Buka browser dan kunjungi **[Google Earth Engine Code Editor](https://code.earthengine.google.com/)**.
2. Pastikan Anda sudah login dengan akun Google yang terdaftar di Google Earth Engine.
3. Buka file **`gee_scripts/building_detection_knn.js`** di text editor Anda (VS Code, Notepad, dll).
4. **Copy (Salin)** seluruh isi kode dari berkas tersebut.
5. **Paste (Tempel)** kode ke dalam panel editor tengah di GEE Code Editor.
6. Klik tombol **Run** (berwarna merah di bagian atas editor).
7. Perhatikan hasilnya:
   * **Peta (Map Area)**: Peta akan otomatis memusatkan tampilan ke area perumahan Sawojajar, Malang (atau Polban Bandung).
   * **Panel Legenda & Inspector (Kiri Bawah)**: Menampilkan legenda warna bangunan (Tipe A: Merah, Tipe B: Kuning, Tipe C: Cyan).
   * **Tab Console (Kanan Atas)**: Menampilkan ringkasan jumlah bangunan per tipe, total objek yang terdeteksi, serta sampel vektor fitur 4D.

---

## 🔍 Interaksi dan Pengujian pada Tampilan Peta

1. **Memeriksa Layer Citra**:
   * Arahkan kursor ke menu **Layers** di pojok kanan atas peta.
   * Anda dapat mencentang / menghilangkan centang untuk melihat tahapan pemrosesan citra:
     1. `1. Citra Asli (RGB Sentinel-2)`: Komposit spektral RGB murni.
     2. `2. Komponen Warna CIE L*a*b*`: Visualisasi false-color ruang warna CIELab.
     3. `3. Segmentasi K-Means (k=3)`: Pembagian citra menjadi 3 kluster warna (lahan, vegetasi, atap).
     4. `4. Mask Bangunan Mentah (Raw)`: Mask biner hasil seleksi kluster atap sebelum morfologi.
     5. `5. Mask Bangunan Bersih (Morfologi)`: Hasil setelah operasi *Opening*, *Closing (Filling Holes)*, dan *Bwareaopen*.
     6. `6a, 6b, 6c. Klasifikasi Tipe A, B, C`: Poligon vektor bangunan berwarna sesuai tipe hasil prediksi k-NN ($k=5$).
     7. `7. Pembanding: Google Open Buildings AI`: Dataset ground truth jejak bangunan resolusi tinggi dari Google.
     8. `8. Batas ROI Kajian`: Garis batas poligon wilayah uji.

2. **Interactive Inspector (Fitur Geometris Objek)**:
   * Klik poligon bangunan mana pun yang berwarna di peta.
   * Panel di pojok kiri bawah akan langsung menampilkan data ekstraksi ciri objek tersebut secara real-time:
     * **Prediksi**: Tipe A / B / C
     * **Luas ($A$)**: dalam satuan $\text{m}^2$
     * **Keliling ($P$)**: dalam satuan meter
     * **Metric ($M$)**: indeks kebulatan/kompak ($0 \le M \le 1$)
     * **Eccentricity ($e$)**: rasio kelonjongan struktur atap ($0 \le e \le 1$)

---

## 🧠 Pemetaan Metodologi Paper ke Script GEE

| Tahapan di Paper / Skripsi | Formula Matematika di Paper | Implementasi di Script GEE (`building_detection_knn.js`) |
| :--- | :--- | :--- |
| **1. Akuisisi Citra** | Google Earth ketinggian 700–800 m | Komposit median Sentinel-2 SR bebas awan resolusi 10m dengan basemap Google Satellite resolusi sub-meter |
| **2. Ruang Warna CIE L\*a\*b\*** | $\begin{bmatrix}X\\Y\\Z\end{bmatrix} = \mathbf{M} \begin{bmatrix}R\\G\\B\end{bmatrix}$, <br>$L^* = 116 f(Y/Y_n) - 16$,<br>$a^* = 500 [f(X/X_n) - f(Y/Y_n)]$,<br>$b^* = 200 [f(Y/Y_n) - f(Z/Z_n)]$ | Fungsi `rgbToCieLab(imgRGB)` dengan matriks D65 dan fungsi non-linier $f(t)$ piecewise |
| **3. Segmentasi Warna** | $k$-Means Clustering ($k=3$) pada kanal $a^*$ dan $b^*$ | `ee.Clusterer.wekaKMeans(3).train(trainingPixels)` pada band `['a', 'b']` |
| **4. Morfologi Biner** | *Opening* ($A \circ B$), *Closing* / *Filling Holes*, *Bwareaopen* | `focal_min` lalu `focal_max` (Opening), `focal_max` lalu `focal_min` (Closing), dan `connectedPixelCount` untuk `bwareaopen` |
| **5. Ekstraksi Fitur 4D** | $\mathbf{x}_i = [A, P, M, e]^T$<br>$M = \frac{4 \pi A}{P^2}$, $e = \sqrt{1 - (b/a)^2}$ | `geom.area()`, `geom.perimeter()`, $M$, dan $e$ dari perbandingan rasio bounding box poligon |
| **6. Klasifikasi $k$-NN** | Algoritma $k$-Nearest Neighbor ($k=5$) dengan jarak Euclidean | `ee.Classifier.smileKNN({k: 5})` dilatih dengan referensi 15 sampel dari Tabel 3.4 Skripsi |

---

## ⚙️ Kustomisasi Konfigurasi (Variabel `CONFIG`)

Pada bagian awal file `building_detection_knn.js`, Anda dapat mengubah variabel `CONFIG`:

```javascript
var CONFIG = {
  // 1. Pilih Lokasi Wilayah Studi:
  //    'MALANG_SAWOJAJAR' : Lokasi skripsi asli di Sawojajar, Kota Malang
  //    'BANDUNG_POLBAN'   : Kampus Polban & Perumahan Ciwaruga/Gegerkalong Bandung
  //    'CUSTOM'           : Menggunakan polygon yang Anda gambar sendiri di peta
  studyArea: 'MALANG_SAWOJAJAR',

  // 2. Rentang Waktu Citra (Pilih rentang kemarau untuk tutupan awan minimal):
  startDate: '2023-06-01',
  endDate: '2023-09-30',

  // 3. Hyperparameter Model:
  kMeansClusters: 3,     // 3 kluster warna (lahan, tanaman, bangunan)
  knnNeighbors: 5,       // Parameter k=5 terbaik pada evaluasi cross-validation skripsi
  minPixelNoise: 2,      // Batas minimum piksel bwareaopen
};
```

### Menggunakan Poligon Sendiri (Custom Geometry)
Jika Anda ingin menguji area perumahan lain di kota Anda:
1. Ubah `studyArea: 'CUSTOM'`.
2. Gunakan **Drawing Tools** (ikon kotak / segi banyak di pojok kiri atas peta GEE).
3. Gambar kotak atau poligon di atas area perumahan yang ingin diuji.
4. Pastikan nama layer gambarnya adalah `geometry`.
5. Klik **Run**, sistem akan langsung memproses wilayah baru tersebut!

---

## 📊 Kategori Tipe Bangunan Hasil Klasifikasi

Berdasarkan dataset penelitian pada Tabel 3.4 dan Bab IV:
1. **Tipe A (Bangunan Besar / Warna Merah)**:
   * Karakteristik: Luas tapak besar ($> 350 \text{ m}^2$), keliling besar, rasio kelonjongan tinggi (*eccentricity* mendekati 0.95–0.97).
   * Contoh fisik: Fasilitas umum, aula kampus, gudang logistik, atau kompleks hunian besar memanjang.
2. **Tipe B (Bangunan Sedang / Warna Kuning-Emas)**:
   * Karakteristik: Luas sedang ($130 - 350 \text{ m}^2$), rasio bentuk lebih seimbang (*metric* $0.5 - 0.7$).
   * Contoh fisik: Rumah tinggal perumahan tipe standar (tipe 54, 70, dsb).
3. **Tipe C (Bangunan Kecil / Warna Cyan)**:
   * Karakteristik: Luas kompak ($< 130 \text{ m}^2$), tapak relatif persegi/kompak.
   * Contoh fisik: Rumah tinggal tipe 21/36 atau paviliun/bangunan sekunder.
