## **DETEKSI DAN KLASIFIKASI TIPE BANGUNAN PADA CITRA SATELIT MENGGUNAKAN METODE** _**K NEAREST NEIGHBOR**_ 

**SKRIPSI Oleh: ADAM JAELANI NIM. 14650050** 

**==> picture [115 x 114] intentionally omitted <==**

**JURUSAN TEKNIK INFORMATIKA FAKULTAS SAINS DAN TEKNOLOGI UNIVERSITAS ISLAM NEGERI MAULANA MALIK IBRAHIM MALANG 2020** 

## **DETEKSI DAN KLASIFIKASI TIPE BANGUNAN PADA CITRA SATELIT MENGGUNAKAN METODE** _**K NEAREST NEIGHBOR**_ 

**SKRIPSI** 

**Diajukan Kepada: Fakultas Sains dan Teknologi Universitas Islam Negeri Maulan Malik Ibrahim Malang Untuk Memenuhi Salah Satu Persyaratan Dalam Memperoleh Gelar Sarjana Komputer (S.Kom)** 

**Oleh: ADAM JAELANI NIM. 14650050** 

**JURUSAN TEKNIK INFORMATIKA FAKULTAS SAINS DAN TEKNOLOGI UNIVERSITAS ISLAM NEGERI MAULANA MALIK IBRAHIM MALANG 2020** 

ii 

## **LEMBAR PERSETUJUAN** 

## **DETEKSI DAN KLASIFIKASI TIPE BANGUNAN PADA CITRA SATELIT MENGGUNAKAN METODE** _**K NEAREST NEIGHBOR**_ 

**SKRIPSI Oleh: ADAM JAELANI NIM. 14650050** Telah Diperiksa dan Disetujui untuk Diuji Tanggal:      Mei 2020 Dosen Pembimbing I Dosen Pembimbing II Dr. Fachrul Kurniawan, M.MT Dr. M Faisal, MT NIP. 19771020 200912 1 001 NIP. 19740510 200501 1 007 Mengetahui, Ketua Jurusan Teknik Informatika Fakultas Sains dan Teknologi Universitas Islam Negeri Maulana Malik Ibrahim Malang 

## Dr, Cahyo Crysdian 

NIP. 19740424 200901 1 008 

iii 

## **LEMBAR PENGESAHAN** 

## **DETEKSI DAN KLASIFIKASI TIPE BANGUNAN PADA CITRA SATELIT MENGGUNAKAN METODE** _**K NEAREST NEIGHBOR**_ 

|||**Oleh:**||
|---|---|---|---|
|||**ADAM JAELANI**||
|||**NIM. 14650050**||
||Telah Dipertahankan di Depan Dewan Penguji Skripsi|||
||dan Dinyatakan|Diterima Sebagai Salah Satu Persyaratan||
||Untuk Memperoleh Gelar Sarjan Komputer (S. Kom)|||
|||Tanggal:        Juni 2020||
|**Susunan Dewan Penguji**|||**Tanda Tangan**|
|1.|Penguji Utama         :|Yunifa Miftachul Arif, M.T|(                          )|
|||NIP. 198306162011011004||
|2.|Ketua Penguji          :|Hani Nurhayati, M.T|(                          )|
|||NIP. 197806252008012006||
|3.|Sekertaris Penguji   :|Dr. Fachrul Kurniawan, M.MT|(                          )|
|||NIP. 19771020 2009121001||
|4.|Anggota Penguji     :|Dr. M Faisal, MT|(                          )|
|||NIP. 19740510 2005011007||
|||Mengetahui,||
||Ketua Jurusan Teknik Informatika|||
||Fakultas Sains dan Teknologi|||
||Universitas Islam Negeri Maulana Malik Ibrahim Malang|||



Dr, Cahyo Crysdian 

NIP. 19740424 200901 1 008 

iv 

## **PERNYATAAN KEASLIAN TULISAN** 

Saya yang bertanda tangan dibawah ini: Nama :  Adam Jaelani NIM :  14650050 Jurusan :  Teknik Informatika Fakultas :  Sains dan Teknologi Judul Skripsi : **DETEKSI DAN KLASIFIKASI TIPE BANGUNAN PADA CITRA SATELIT MENGGUNAKAN METODE** _**K NEAREST NEIGHBOR**_ Menyatakan dengan sebenarnya bahwa Skripsi yang saya tulis ini benar benar merupakan hasil karya saya sendiri, bukan merupakan pengambilalihan data, tulisan atau pikiran orang lain yang saya akui sebagai hasil tulisan atau pikiran saya sendiri, kecuali dengan mencantumkan sumber cuplikan pada daftar pustaka. Apabila dikemudian hari terbukti atau dapat dibuktikan Skripsi ini hasil jiplakan maka saya bersedia menerima sanksi atas perbuatan tersebut. 

**==> picture [222 x 197] intentionally omitted <==**

v 

## **MOTTO** 

## **“Not knowing oneself that's the worst”** 

```
“Don’t compare yourself with others, There is
no comparison between the sun & the moon, they
shine when it’s their time”
```

vi 

## **HALAMAN PERSEMBAHAN** 

Puji Syukur kehadirat Allah Subhanahu wa ta’ala atas segala limapahan RahmatNya, Serta Sholawat dan salam semoga selalu tercurah kepada Rasul Muhammad Shallallahu alihi wassalam. 

Ucapan Terimakasih dan Karya ini saya persembahkan kepada: Keduan Orangtuaku tercinta Bapak Sucita dan Ibu Rohimah, atas doa dan kasih sayang yang selalu tercurah, Semoga Allah menganugrahkan umur panjang, kesehatan, ketaatan dan selalu dalam ridhoNya. Never forget two people in mylife: The person who lost every thing just to make me win (My Father). The person who was with me in every pain (My Mother) Ketiga Saudaraku tercinta, kakakku Rahmat Saleh dan Mustofa Hambali dan adikku Aprilia Rahmi semoga selalu dalam lindungan Allah dan dapat menjadi anak anak yang berbakti kepada orang tua. Kakek, Nenek, Paman, Bibi dan semua keluarga besarku semoga dikumpulkan kembali didalam surgaNya. Dosen pembimbing saya Bapak Fachrul Kurniawan, M.MT dan Bapak Dr. M Faisal, M.T. Seluruh dosen dan Stuf Jurusan Teknik Informatika Universitas Islam Negeri Maulana Malik Ibrahim Malang atas semua bimbingan dan ilmu yang diajarkan semoga selalu diberi keberkahan dan RidhoNya. Sahabat sahabat seperjuangan Teknik Informatika B 14, Biner 14, dan semua angkatan Teknik Informatika Uin Malang. Sahabat rantau dan sahabat Forum Silaturahim Mahasiswa Lombok Semua orang yang saya sayangi yang tidak bisa saya sebutkan satu persatu Saya ucapkan terimakasih yang luar biasa, semoga persahabatan dan kekeluargaan ini selalu dalam Ridho Allah Subhanahu wa ta’ala, Aamiin. 

vii 

## **KATA PENGANTAR** 

Segala puji bagi Allah Subhanahu wa ta’ala atas limpahan rahmat, taufiq dan hidayahNya, sehingga penulis dapat menyelesaikan skripsi yang berjudul “Deteksi dan Klasifikasi Tipe Bangunan Pada Citra Satelite Menggunakan Metode _k Nearest Neighbor”_ sebagai syarat untuk memperoleh gelar sarjana Program Studi Teknik Informatika jenjang Strata- 1 Universitas Islam negeri Maulan Malik Ibrahim Malang. Sholawat dan salam senantiasa tercurah kepada Rasul Mulia Muhammad Shalallahu alaihi wassalam, keluarga dan para sahabatnya yang telah membawa umat manusia dari zaman yang gelap gulita jahiliyah menuju ke zaman yang terang benderang, Islam yang diridhoi Allah Subhanahu wa ta’ala. Penulis menyadari bahwa ada banyak keterbatas yang penulis miliki, sehingga ada banyak pihak yang telah memberikan bantun baik secara moril ataupun materil dalam menyelesaikan penelitian ini. Maka dari itu dengan segenap kerendahan hati penulis mengucapkan terimakasih kepada: 1. Prof Dr H Abd. Haris, M.Ag selaku Rektor UIN Maulana Malik Ibrahim Malang. 2. Dr. Sri Harini, M.Si selaku Dekan Fakultas Sains dan Teknologi UIN Maulana Malik Ibrahim Malang. 3. Dr. Cahyo Crysdian selaku Ketua Jurusan Teknik Informatika UIN Maulana Malik Ibrahim Malang. 4. Fachrul Kurniawan, M.MT selaku pembimbing I dan Dr. M Faisla M.T selaku pembimbing II yang senantiasa memberikan bimbingan, arahan dan masukan kepada penulis. 

viii 

5. Seluruh Dosen Jurusan Teknik Informatika Fakultas Sains dan Teknologi UIN Maulana Malik Ibrahim Malang. 6. Segenap Civitas Akademik Jurusan Teknik Informatika Fakultas Sains dan Teknologi UIN Maulana Malik Ibrahim Malang. 7. Kedua Orang tua dan seluruh keluarga besar penulis yang senatiasa memberi dukungan. 8. Rekan rekan seperjuangan Jurusan Teknik Informatika Fakultas Sains dan Teknologi UIN Maulana Malik Ibrahim Malang. Penulis menyadari bahwa dalam karya ini masih banyak kekurangan, oleh karena itu penulis selalu menerima segala keritik dan saran dari pembaca. Semoga karya ini bermanfaat bagi seluruh pihak. Malang,      Juni 2020 Penulis 

ix 

## **DAFTAR ISI** 

|**LEMBAR PENGAJUAN...................................................................................... ii**|
|---|
|**LEMBAR PERSETUJUAN ................................................................................ iii**|
|**LEMBAR PENGESAHAN ................................................................................. iv**|
|**LEMBAR PERNYATAAN .................................................................................. v**|
|**HALAMAN MOTTO .......................................................................................... vi**|
|**HALAMAN PERSEMBAHAN ......................................................................... vii**|
|**KATA PENGANTAR ........................................................................................ viii**|
|**DAFTAR ISI .......................................................................................................... x**|
|**DAFTAR GAMBAR .......................................................................................... xiii**|
|**DAFTAR TABEL ............................................................................................... xv**|
|**ABSTRAK ......................................................................................................... xvii**|
|**ABSTRACT ...................................................................................................... xviii**|
|**..............................................................................................................ملخص البخثxix**|
|**BAB I PENDAHULUAN ...................................................................................... 1**|
|1.1.<br>Latar Belakang ......................................................................................... 1|
|1.2.<br>Pernyataan Masalah .................................................................................. 5|
|1.3.<br>Tujuan Penelitian ...................................................................................... 5|
|1.4.<br>Batasan Penelitian .................................................................................... 6|
|1.5.<br>Manfaat Penelitian .................................................................................... 6|
|**BAB II TINJAUAN PUSTAKA ........................................................................... 7**|
|2.1. Penelitian Terkait ......................................................................................... 7|
|2.2. Landasan Teori ............................................................................................. 9|
|2.2.1.<br>Model Warna (Color Models) ......................................................... 10|
|2.2.1.1. Ruang Warna RGB ...................................................................... 11|
|2.2.1.2. Ruang Warna_L*a*b_.................................................................... 12|
|2.2.2.<br>Segmentasi Gambar ........................................................................ 14|
|2.2.3.<br>Ekstarksi Ciri ................................................................................... 18|
|2.2.3.1. Ekstraksi Ciri Bentuk ................................................................... 18|
|2.2.3.2. Ekstataksi CiriaUkuran ................................................................ 20|
|2.2.3.3. Ekstraksi CiriaGeometri ............................................................... 20|



x 

|2.2.3.4. Ekstraksi Ciri Tekstur .................................................................. 21|
|---|
|2.2.3.5. Ekstraksi Ciri Warna .................................................................... 21|
|2.2.4.<br>Operasi Morfologis ......................................................................... 23|
|2.2.4.1.<br>Translasia ................................................................................. 23|
|2.2.4.2.<br>Dilasi ........................................................................................ 24|
|2.2.4.3.<br>Erosi ......................................................................................... 24|
|2.2.4.4.<br>Opening .................................................................................... 24|
|2.2.5.<br>K Nearest Neighbora ....................................................................... 25|
|2.2.5.1.<br>Cara Kerja Algoritma_k-NN_..................................................... 26|
|2.2.5.2.<br>Perhitungan Jarak ..................................................................... 28|
|2.2.5.3.<br>Kinerja Algoritma_k-NN_........................................................... 30|
|2.2.5.4.<br>Kelebihan dan Kekurangan Algoritma_k-NN_........................... 30|
|_2.2.6._<br>_K Fold Cross Validationa_............................................................... 31|
|**BAB III DESAIN PENELITIAN ....................................................................... 33**|
|3.1.<br>Desain Sistem ......................................................................................... 33|
|3.1.1.<br>Citra Satelit_RGB_............................................................................. 34|
|3.1.2.<br>Segmentasi ...................................................................................... 34|
|3.1.2.1.<br>Proses Segmentasi.................................................................... 35|
|3.1.3.<br>Ekstraksi Ciri ................................................................................... 41|
|3.1.4.<br>Klasifikasia_k-Nearest Neighbora_.................................................... 44|
|3.1.4.1.<br>Flowchart Algoritma_k-Nearest Neighbor_............................... 46|
|3.1.4.2.<br>Menghitung_Euclidean Distance_............................................. 49|
|3.1.4.3.<br>Klasifikasi Data........................................................................ 50|
|3.1.5.<br>Perhitungan Akurasi ........................................................................ 52|
|**BAB IV UJICOBA DAN PEMBAHASAN ....................................................... 54**|
|4.1.<br>Implementasi .......................................................................................... 54|
|4.1.1.<br>Software .......................................................................................... 54|
|4.1.2.<br>Hardware ......................................................................................... 54|
|4.2.<br>Uji Coba Deteksi Bangunan ................................................................... 55|
|4.2.1.<br>Citra Hasil Segmentasi .................................................................... 55|
|4.2.2.<br>Citra Hasil Deteksi Bangunan ......................................................... 57|
|4.3.<br>Proses Klasifikasi Bangunan .................................................................. 60|
|4.3.1.<br>Ektraksi Ciri Objek Deteksi ............................................................ 61|



xi 

|4.3.2.<br>Uji Coba Akurasi Klasifikasi KNN ................................................ 62|4.3.2.<br>Uji Coba Akurasi Klasifikasi KNN ................................................ 62|4.3.2.<br>Uji Coba Akurasi Klasifikasi KNN ................................................ 62|
|---|---|---|
||4.3.2.1.<br>Dataset Uji Coba Klasifikasi KNN .......................................... 62||
||4.3.2.2.<br>Skenario Pengujian 1 ............................................................... 64||
||4.3.2.3.<br>Skenario Pengujian 2:|.............................................................. 68|
||4.3.2.4.<br>Skenario pengujian 3 ............................................................... 72||
|4.4.|Integrasi Dengan Al Quran ..................................................................... 78||
|**BAB V KESIMPULAN DAN SARAN**||**.............................................................. 81**|
|5.1.|Kesimpulan ............................................................................................. 81||
|5.2.|Saran ....................................................................................................... 81||
|**DAFTAR PUSTAKA .......................................................................................... 83**|||
|**LAMPIRAN ......................................................................................................... 85**|||



xii 

## **DAFTAR GAMBAR** 

Gambar 2.1 Koordinat Warna RGB ...................................................................... 11 Gambar 2. 2 _LAB Color_ ........................................................................................ 13 Gambar 2. 3 Histogramadengan 1 lembahadiantara 2 puncak .............................. 15 Gambar 2. 4 Contoh Segmentasiadengan _Histogram_ adan _Region_ ....................... 15 Gambar 2. 5 GambaraSegmentasi Pesawat ........................................................... 17 Gambar 2. 6 Ilustrasi Perhitungan _Eccentricity_ .................................................... 19 Gambar 2. 7 Ilustrasi Perhitungan Matric ............................................................. 19 Gambar 2. 8 Contoh Ciri Ukuran .......................................................................... 20 Gambar 2. 9 Contoh Bentuk Bentuk Geometri ..................................................... 20 Gambar 2. 10 Contoh Tekstu Citra ....................................................................... 21 Gambar 2. 11 _RGB ColoraSpace_ dan _HSVaColor Space_ ..................................... 23 Gambar 2. 12 Contoh Klasifikasi _k- NN_ ............................................................... 26 Gambar 3. 1 Desain Sistem ................................................................................... 33 Gambar 3. 2 Citra Satelit Hasil Croping ............................................................... 34 Gambar 3. 3 Proses Segmentasi ............................................................................ 35 Gambar 3. 4 Inputan Citra _RGB_ ............................................................................ 35 Gambar 3. 5 Proses Konversi Warna .................................................................... 36 Gambar 3. 6 Hasil Konversi _RGB_ ke _LAB_ ............................................................ 37 Gambar 3. 7 Citra RGB ......................................................................................... 38 Gambar 3. 8 Konversi _RGB_ ke _L*a*b_ .................................................................. 38 Gambar 3. 9 Citra Hasil Segmentasi ..................................................................... 39 Gambar 3. 10 Hasil Segmentasi _Cluster_ 1 ............................................................ 39 Gambar 3. 11 Hasil Segmentasi _Cluster_ 2 ............................................................ 39 xiii 

Gambar 3. 12 Hasil Segmentasi _Cluster_ 3 ............................................................ 40 Gambar 3. 13 Cluster Terdapat _Foreground_ Bangunan ........................................ 40 Gambar 3. 14 Hasil Morfologi _Filling Holes_ dan _Bwarea Open_ .......................... 41 Gambar 3. 15 _Flowchart_ Ektraksi Ciri .................................................................. 42 Gambar 3. 16 Labelling Objek .............................................................................. 42 Gambar 3. 17 Rumus _Eccentricity_ ........................................................................ 44 Gambar 3. 18 Rumus _Metric_ ................................................................................. 44 Gambar 3. 19 Flowchat Algoritma _k-NN_ .............................................................. 46 Gambar 4. 1 Blok Deteksi Bangunan .................................................................... 55 Gambar 4. 2 Diagram Blok Klasifikasi sistem...................................................... 60 Gambar 4. 3  Gambar Uji ...................................................................................... 61 Gambar 4. 4 Citra Bangunan ................................................................................. 75 Gambar 4. 5 Interface Sistem ................................................................................ 75 

xiv 

## **DAFTAR TABEL** 

Tabel 2. 1 Ilustrasi _k-Fold Cross Validation_ ......................................................... 31 Tabel 3. 1 Luas, Keliling, _Eccentricity_ , dan _Metrik_ Hasil Ekstraksi ..................... 43 Tabel 3. 2 Contoh Data Training Tipe Bangunan ................................................. 45 Tabel 3. 3 Sampel Data Latih Bangunan .............................................................. 47 Tabel 3. 4 Sampel Data Training Tipe Bangunan ................................................. 48 Tabel 3. 5 Tabel Pehitungan _Euclidean Distance_ ................................................. 49 Tabel 3. 6 Hasil Perhitngan _Euclidean Distance_ .................................................. 50 Tabel 3. 7 _k_ =3 ........................................................................................................ 50 Tabel 3. 8 _k=_ 5 ....................................................................................................... 51 Tabel 3. 9 _k=_ 7 ....................................................................................................... 51 Tabel 3. 10 _k=9_ ..................................................................................................... 52 Tabel 3. 11 _Confusion Matric Model_ .................................................................... 53 Tabel 4. 1 Hasil Segmentasi Citra ......................................................................... 56 Tabel 4. 2 Tabel Hasil Deteksi Bangunan ............................................................. 57 Tabel 4. 3 Akurasi Deteksi Sistem ........................................................................ 59 Tabel 4. 4 Tabel Hasil Ekstraksi Ciri .................................................................... 62 Tabel 4. 5 Tipe Bangunan A ................................................................................. 63 Tabel 4. 6 Tipe Bangunan B ................................................................................. 63 Tabel 4. 7 Tipe Bangunan C ................................................................................. 63 Tabel 4. 8 Hasil Klasifikasi Knn ........................................................................... 65 Tabel 4. 9 Rumus _Confussion Matrix_ .................................................................. 66 Tabel 4. 10 _Confussion matrix k_ =3 ....................................................................... 66 Tabel 4. 11 _Confussion Matrix k_ =5 ....................................................................... 66 

xv 

Tabel 4. 12 _Confussion Matrix k_ =7 ....................................................................... 67 Tabel 4. 13 _Confussion Matrix k=_ 9 ...................................................................... 67 Tabel 4. 14 _Confussion Matrix k=_ 11 .................................................................... 67 Tabel 4. 15 Akurasi Hasil Klasifikasi _k_ ................................................................ 68 Tabel 4. 16 Pengujian _k-fold_ =5 ............................................................................. 69 Tabel 4. 17 Test _fold_ 1........................................................................................... 69 Tabel 4. 18 Test _fold_ 2........................................................................................... 70 Tabel 4. 19 Test _fold_ 3........................................................................................... 70 Tabel 4. 20 Test _fold_ 4........................................................................................... 70 Tabel 4. 21 Test _fold_ 5........................................................................................... 71 Tabel 4. 22 Akurasi _k fold_ ..................................................................................... 71 Tabel 4. 23 Perbandingan akurasi _k NN_ dan _k Fold_ .............................................. 72 Tabel 4. 24 Hasil Deteksi dan Klasifikasi Sistem ................................................. 77 

xvi 

## **ABSTRAK** 

Jaelani, Adam. 2020. **Deteksi dan Klasifikasi Tipe Bangunan Pada Citra Satelite Menggunakan Metode** _**k Nearest Neighbor**_ **.** Skripsi. Jurusan Teknik Informatika Fakultas Sains dan Teknologi Universitas Islam Negeri Maulana Malik Ibrahim Malang. Pembimbing: (I) Fachrul Kurniawan, M. MT. (II) Dr. M Faisal, MT. 

Kata kunci: Citra Satelit, Segmentasi Warna, Deteksi Bangunan, _k Fold Cross Validation, k Nearest Neighbor_ 

Kepadatan bangunan menimbulkan berbagai permasalahan di kota kota besar di Indonesia, menjadikan kota cerdas muncul menjadi solusi untuk mengurangi masalah yang ditibulkan, agar infrastruk kota menjadi cerdas makas konsep identifikasi objek harus digunakan untuk mendeteksi dan menganalisa keberadaan mobil, jalan, dan bangunan. Dengan adanya citra satelit maka proses pengolahan citra digital terkait dengan objek objek permukaan bumi akan sangat membantu dalam menyelesaikan permasalahan geografis, tataruang kota dan lain lain. Metode segmentasi warna digunakan untuk mendeteksi objek bangunan pada citra satelit digital dan metode _k Nearest Neighbor_ digunakan untuk mengklasifikasi objek bangunan berdasarkan hasil ektraksi ciri yang didapatkan. Rata rata akurasi deteksi bangunan dengan segmentasi warna yaitu 90.8%, pengujian nilai akurasi _k Nearest Neighbor_ dengan _k_ =5 mendapatkan akurasi terbaik 93%. Akurasi hasil pengujian ketepatan klasifikasi _k Nearest Neighbor_ dengan _k Fold Cross Validation_ menujukan rata rata akurasi _k Nearest Neighbor_ sebesar 93%. 

xvii 

## **ABSTRACT** 

Jaelani, Adam. 2020. Detection and Classification of Building Types in Satellite Image Using _k Nearest Neighbor_ Method. Thesis. Department of Informatics, Faculty of Science and Technology, Maulana Malik Ibrahim State Islamic University of Malang. Supervisor: (I) Fachrul Kurniawan, M. MT. (II) Dr. M Faisal, MT. 

Keywords: Satellite Imagery, Color Segmentation, Building Detection _, k Fold Cross Validation_ , _k Nearest Neighbor_ 

Building density causes various problems in big cities in Indonesia, making smart cities emerge as a solution to reduce the problems that are caused, so that city infrastructure becomes intelligent, the concept of object identification must be used to detect and analyze the presence of cars, roads and buildings. With the presence of satellite imagery, the process of processing digital images associated with objects on the surface of the earth will be very helpful in solving geographical problems, the layout of cities and others. The color segmentation method is used to detect building objects in digital satellite imagery and the _k Nearest Neighbor_ method is used to classify building objects based on the feature extraction obtained. The average accuracy of building detection with color segmentation is 90.8%, testing the accuracy value of _k Nearest Neighbor_ with _k_ = 5 gets the best accuracy of 93%. The accuracy of the results of the classification of _k Nearest Neighbor_ with _k Fold Cross Validation_ shows the average accuracy of _k Nearest Neighbor_ by 93%. 

xviii 

## **ملخص البخث** 

٠٢٠٢آدم. . تكشيف وتصنيف أنواع املباين يف صورة األقمار الصناعية ابستخدام طريقة جيالين، .k Nearest Neighbor . شعبة اهلندسة املعلوماتية، كلية العلوم والتكنولوجيا، البحث اجلامعي لنج. جامعة موالان مالك إبراهيم اإلسالمية احلكومية م والدكتور حممد فيصل، املاجسترياملشرف: فخر الكورنيوان، املاجستري، 

|الكلمات الرئيسية: صورة القمار الصناعية، تزئة اللوان ، تكشيف البان،k Fold Cross|
|---|
|Validation<br>،<br>k Nearest Neighbor|
|البن<br>ال<br>متل<br>ي<br>سبب مشاكل متلفة ف الدن<br>الكبى ف إندونيسيا، ما يعل الدن الذكية أن ت<br>ظهر|
|كحل للحد الشاكل لن تصبح البنية التحتية للمدينة ذكية ، ويب أن يستخدم مفهوم تديد الكائن|
|لكتشاف وتليل وجود السيارات والطرق والبان. مع وجود صورة القمار الصناعية، ستكون عملية|
|معالة الصورة الرقمية الت<br>تتعلق بلجسام على سطح الرض مفيدة جدًا ف حل الشكلت الغرافي<br>ة،|
|وتطيط الدن وغيها. استخدم طريقة تزئة اللوان للكشف عن كائن البن ف صورة القمار الصناعية|
|الرقمية ، واستخدم طريقة<br> k Nearest Neighbor<br>.لتصنيف كائن البن بناء على استخراج العال|
|دقة<br>الكشف<br>البان التوسط مع تزئة اللوان هي90.8<br>٪<br>، ويتب قيمة دقة<br> k Nearest|
|Neighborمع<br> k= 5<br>أفضل دقة أي93<br>٪. دلت دقة نتائجلختبار التصنيف<br> k Nearest|
|Neighbor<br>مع<br> k Fold Cross Validation دقة<br>متوسطk Nearest Neighbor<br>بنسبة|
|93<br>٪ .|



xix 

## **BAB I** 

## **PENDAHULUAN** 

## **1.1. Latar Belakang** 

Dari hasil sensus penduduk jumlah penduduk di Indonesia pada tahun 2010 adalah sebanyak 237.641.326 jiwa, yang mencakup mereka yang bertempat tinggal di daerah perkotaan sebanyak 118.320.256 jiwa (49.79%) dan di daerah pedesaan sebanyak 119.321.070 jiwa (50.21%) (bps.go.id:2010). Tahun ini, jumlah penduduk Indonesia yang tinggal di perkotaan diperkirakan telah mencapai 54%. Jika saat ini penduduk Indonesia sudah lebih dari 240 juta, artinya paling sedikit ada 129,6 juta orang yang menyesaki perkotaan. Angka ini melambung tinggi disbanding hasil sensus penduduk tahun 2010. Saat itu, sebanyak 49, 8 % dari 237, 6 juta penduduk Indonesia tinggal di kota (Wahyudi, 2012). Semakin hari kita akan melihat semakin tingginya migrasi dari zona desa menuju zona kota. Ketimpangan antara desa dengan kota menjadi penyebab terus meningkatnya Urbanisasi dari tahun ke tahun. Oleh karena itu permasalahan baru akan muncul di kota kota besar di Indonesia seperti: kelangkaan sumberdaya, polusi, kemancetan lalulintas, kesehatan, infrastruktur yang tidak memadai, dan lain lain. 

Menjadikan kota ‘cerdas’ muncul menjadi solusi untuk mengurangi masalah yang ditimbulkan oleh pertumbuhan populasi perkotaan dan urbanisasi yang cepat. Lebih dari setengah penduduk dunia sekarang tinggal didaerah perkotaan. Pergeseran dari zona pedesaan menuju perkotaan diproyeksikan akan berlanjut dalam beberapa dekade mendatang. Akibatnya kota harus tumbuh, tetapi penting harmoni itu ada atau dihasilkan antara aspek spasial, sosial, ekonomi dan lingkungan. Kota disebut kota pintar harus membuat perencanaan kota itu lebih pintar. 

1 

2 

Konsep _Smart City_ untuk negara berkembang terdiri dari delapan parameter, yaitu _Smart Energy_ , _Smart Infrastructure_ , _Smart People_ , _Smart Health, Smart Mobility, Smart Governance, Smart Educatuin,_ dan _Smart Technology_ . Perbedaan antara negara maju dan negara berkembang terletak pada ketersediaan infrastruktur perkotaan, sumber daya manusia yang kompeten, dan teknologi canggih, yang mungkin berbeda dalam beberapa tahun (Kurniawan, Nugroho, & Hariadi, 2018). _Smart Infrastruktur_ sangat membantu dalam meningkatkan perencanaan kota dalam membentuk _Smart City_ , sehingga dapat menerapkan sistem pengalamatan bangunan cerdas di dalam kota. Agar infrastruktur kota menjadi cerdas maka konsep identifikasi objek harus digunakan untuk mendeteksi dan menganalisa keberadaan mobil, jalan, bangunan dan lain lain. Dari konteks ini penulis berfokus pada studi ini tentang topik penelitian deteksi bangunan yang merupakan batuan dasar dalam membangun infrastruktur _Smart City_ yang lengkap. Selain itu banyaknya jenis bangunan dengan berbagai bentuk dan ukuran membutuhkan algoritma yang bisa mengklasifikasikan tipe tipe bangunan sehingga dapat dibedakan antara bangunan satu dengan bangunan yang lain dengan mudah dan akurat. Algoritmaa _k Nearest Neighbor_ merupakanateknik klasifikasiayang sangatapopular yang telah terbukti menjadi algoritma sederhana yang baik. _K Nearest Neighbor_ merupakan salah satu metode yang digunakan dalam pengklasifikasian dengan menggunakan algoritma _Supervised_ . Tujuan dari algoritma ini adalah untuk 

3 

mengklasifikasikan objek baru berdasarkan jarak suatu objek yang akan diklasifikasikan terhadap data contoh. _Classifier_ hanya menggunakan fungsi jarak dari data baru ke data _training_ (Whidhiasih, Wahanani, & Supriyanto, 2013) Pesatnya perkembangan teknologi khususnya dalam bidang pengolahan citra digital yang banyak dimanfaatkan di berbagai bidang untuk menyelesaikan banyak permasalahan. Pengolahan citra satelit merupakan salah satu topik penelitian yang banyak dikaji beberapa tahun belakangan ini, dengan adanya citra satelit maka proses pengolahan citra digital terkait dengan objek objek permukaan bumi akan sangat membantu manusia dalam menyelesaikan permasalahan seperti geografis, kependudukan, keamanan dan lain lain. Salah satu penelitina terkait pengolahan citra satelit digital adalah deteksi bangunan. Deteksi bangunan dari data penginderaan jauh adalah sangat penting untuk industri perumahan, perencanaan kota, keamanan dalam negeri, manajemen bencana dan banyak aplikasi lainnya. Ekstraksi batas batas bangunan secara otomatis juga merupakan langkah penting menuju pembuatan model kota (Liang, Gong, Chen, & Han, 2008) Dalam ayat Al Quran surat Ali Imran ayat 190- 191, dijelaskan bahwa manusia diperintahkan untuk memperhatikan tanda tanda kebesaran Allah sehingga manusia dapat mengambil pelajaran sekaligus manfaat dari apa yang diperhatikannya. 

4 

**==> picture [286 x 176] intentionally omitted <==**

190. _Sesungguhnya dalam penciptaan langit dan bumi, dan silih bergantinya malam dan siang terdapat tanda-tanda bagi orang-orang yang berakal_ 191. _(yaitu) orang-orang yang mengingat Allah sambil berdiri atau duduk atau dalam keadan berbaring dan mereka memikirkan tentang penciptaan langit dan bumi (seraya berkata): "Ya Tuhan kami, tiadalah Engkau menciptakan ini dengan sia-sia, Maha Suci Engkau, maka peliharalah kami dari siksa neraka_ **Tafsir Al Quran Surat Ali Imran Ayat 190-191:** Sesungguhnya dalam penciptaan langit dan bumi yang tanpa ada contoh sebelumnya dan pergantian malam dan siang dan perbedaan waktu keduanya dengan memanjang dan memendek benar benar merupakan petunjuk petunjuk dan bukti bukti yang agung atas keesaan Allah bagi orang orang yang mempunyai akal akal yang selamat (Tafsir al Muyassar). Yaitu orang orang yang mengingat Allah dalam semua kondisi mereka, baik berdiri, duduk dan dalam keadaan mereka berbaring. Mereka mentadaburi dalam penciptaan langit dan bumi seraya berkata, “wahai Tuhan 

5 

kami, Engkau tidaklah menciptakan makhluk ciptaan ini dengan sia sia. Dan Engkau Maha Suci dari hal itu. Maka jauhkanlah dari kami siksaan neraka (Tafsir al Muyassar). **1.2. Pernyataan Masalah** Berdasarkan latar belakang yang telah diuraikan sebelumnya, maka dapat diketahui permasalahan yang dapat difokuskan pada penelitian ini adalah: a. Bagaimana membangun sistem deteksi bangunan berdasarkan segmentasi gambar dan klasifikasi tipe bangunan menggunakan metode _k Nearest Neighbor?_ b. Bagaimana mendapatkan tingkat akurasi metode _k Nearest Neighbor_ untuk klasifikasikan bangunan pada citra satelit? **1.3. Tujuan Penelitian** Berdasarkan identifikasi permasalahan yang telah diuraikan sebelumnya, maka tujuan yang ingin dicapai dalam penelitian ini adalah: a. Penelitian ini untuk membangun sistem deteksi dan klasifikasi tipe bangunan dari citra satelit menggunakan metode segmentasi warna dan klasifikasian tipe bangunan menggunakan metode _k Nearest Neighbor_ . b. Penelitian ini untuk mendapatkan tingkat akurasi dari metode segmentasi gambar dan _k Nearest Neighbor_ dalam mendeteksi dan mengklasifikasikan bangunan pada citra satelit. 

6 

## **1.4. Batasan Penelitian** 

Batasan penelitian ini bertujuan untuk memfokuskan dan 

memudahkan dalam penelitian, maka diperlukan beberapa batasan-batasan 

dalam pengerjaannya, diantaranya sebagai berikut ini: 

a. Citra Satelit yang digunakan diambil dari citra satelit _Google Earth_ . 

b. Citra satelit yang digunakan diambil dari ketinggian 700 – 800 meter. 

**1.5. Manfaat Penelitian** Adapun hasil penelitian ini diharapkan dapat memberikan manfaat sebagai berikut: 

a. Bagi penulis, penelitian ini dapat menambah pengetahuan dan wawasan mengenai permasalahan deteksi bangunan dari citra satelit dan pengklasifikasian tipe bangunan menggunakan metode _k Nearest Neighbor_ . b. Bagi pengguna, hasil dari penelitian ini dapat membantu untuk melakukan deteksi bangunan pada suatu wilayah secara cepat dan mudah sehingga permasalahan akibat kepadatan bangunan dapat diatasi. 

## **BAB II** 

## **TINJAUAN PUSTAKA** 

## **2.1. Penelitian Terkait** 

(Awrangjeb, Ravanbakhsh, & Fraser, 2010) _**Automatic detection of residential buildings using LIDAR data and multispectral imagery**_ . Mengusulkan teknik deteksi bangunan otomatis menggunakan _LIDAR_ data dan _colour orthoimagery_ yang memiliki empat langkah utama. Pertama, _two mask_ , ‘ _primary building mask_ ’ dan  ‘ _secondary building mask_ ’ yang dihasilkan dari _LIDAR_ data. _Mask_ bangunan primer menunjukan daerah kosong dimana tidak ada laser kembali dibawah ambang batas ketinggian tertentu. _Mask_ bangunan sekunder menunjukkan area yang terisi, darimana objek ditinggikan diatas ambang ketinggian yang sama. Kedua, baris segmen dari seluruh area kosong di _mask_ bangunan utama diekstrak. Segmen garis di sekitar pohon dihapus menggunakan _Normalized Different Vegetation Index_ ( _NDVI_ ) nilai diturunkan dari gambar _multispectral_ . Ketiga, posisi awal bangunan dipulihkan berdasarkan segmen garis yang tersisa. Akhirnya, jejak bangunan yang lengkap diperoleh dari posisi awal menggunakan _two mask_ dan _orthoimagery_ didalam _YIQ colour system_ . 

(Akcay & Aksoy, 2010) _**Building detection using directional spatial contraints.**_ Menggambarkan sebuah algoritma untuk mendeteksi bangunan pada citra spasial resolusi tinggi. Setelah _oversegmentation_ awal, selanjutnya menggunakan _directional spatial constraints_ untuk menemukan kandidat daerah bangunan yang dekat dengan bayangan di sepanjang sudut _azimuth_ matahari. Wilayah bangunan dipilih dengan cara pengelompokan daerah kandidat menggunakan _spanning trees minimum_ . Selanjutnya mengevaluasi pendekatan 

7 

8 

yang diusulkan pada _scene_ yang berbeda dengan karakteristik bangunan yang berbeda. Eksperimen menunjukkan bahwa algoritma yang diusulkan mampu mendeteksi bangunan dengan berbagai bentuk dan warna. Selain itu, setelah daerah bangunan terdeteksi, mereka dapat digunakan untuk meningkatkan analisis scene dan klasifikasi daerah perkotaan. 

(Izadi & Saeedi, 2010) _**Automatic building detection in aerial image using**_ 

_**a hierarchical feature based image segmentation.**_ Memperkenalkan deteksi bangunan otomatis dari gambar udara. Metode yang diusulkan menggabungkan fitur _hirarki multilayer_ berbasis teknik segmentasi gambar menggunakan warna. Sejumlah atribut geometri atau regional didefinisikan untuk mengidentifikasi daerah potensial dalam berbagai lapisan gambar tersegmentasi. Mekanisme berbasis _tree_ digunkan untuk memeriksa daerah tersegmentasi menggunakan hubungan sapsial satu sama lain dan karakteristik regional atau geometris. Proses ini memungkinkan terciptanya sekumpulan kandidat daerah yang tervalidasi sebagai atap rumah berdasarkan pada tumpang tindih dan prediksi bayangan setiap daerah sesuai dengan informasi perolehan gambar. Hasil eksperimen menunjukkan akurasi bentuk keseluruhan dan kelengkapan 96%. 

(Setiawan & Damayanti, 2016) _**Klasifikasi Citra Retina Menggunakan K Nearest Neighbor Untuk Mendeteksi Makulopati Diabetik.**_ Melakukan pendeteksian penyakit Makulopati Diabetik dari analisis citra fundus yang merupakan citra hasil foto retina menggunakan kamera fundus. Dataset yang digunakan yaitu _MESSIDOR_ sebanyak 75 citra retina, terdiri dari 3 kelas yaitu Edema Makula ( _EM_ ) tingkat 1, _EM_ tingkat 2 dan _EM_ tingkat 3. Ekstraksi fitur menggunakan _Two Dimensional Linear Discriminant Analysis_ , sedangkan 

klasifikasi menggunakan _k-Nearest Neighbor_ . Dari hasil ujicoba didapatkan prosentase pengenalan maksimal hingga 93,33%. Hal ini dipengaruhi oleh semakin banyaknya data pelatihan maka semakin baik prosentase keakuratan. 

(Subairi, Rahmadwati, & Yudaningtyas, 2018) _**Implementasi Metode K Nearest Neighbor Pada Pengenalan Pola Tekstur Citra Saliva Untuk Deteksi Ovulasi.**_ Mendeteksi masa ovulasi pada wanita berdasarkan citra pola _ferning saliva_ menggunakan metode metode _k-Nearest Neighbor._ Data masukan berupa lima parameter dari fitur tekstur _GLCM_ ( _gray-level co-occurence matrices_ ), yang meliputi _ASM_ ( _Angular Second Moment_ ), contrast, _IDM_ ( _Inverse Different Moment_ ), _entropy_ , dan _correlation_ , yang diambil dari rata-rata dari masing-masing sudut 0°, 45°, 90°, dan 135°. Sedangkan data keluaran adalah salah satu dari tiga klasifikasi dari masa ovulasi, yaitu _infertile_ , _intermediate_ , dan _fertile_ dengan akurasi 93.3%. 

## **2.2. Landasan Teori** 

Pengolahan citra digital _(Digital Image Processing)_ merupakan bidang ilmu yang mempelajari tentang bagaimana suatu citra itu dibentuk, diolah, dan dianalisis sehingga menghasilkan informasi yang dapat dipahami manusia. Citra digital merupakan representasi dari fungsi intensitas cahaya dalam bentuk diskrit pada bidang dua dimensi. Citra tersusun oleh sekumpulan piksel ( _picture element_ ) yang memiliki koordinat _(x, y)_ dan amplitude _f(x, y)._ Koordinat _(x, y)_ menunjukkan letak atau posisi piksel dalam suatu citra, sedangkan amplitude _f(x, y)_ menunjukkan nilai intensitas warna citra. 

10 

Berdasarkan bentuk sinyal penyusunnya, citra dapat digolongkan menajadi dua jenis yaitu citra analog dan citara digital. Citra analog adalah citra yang dibentuk dari sinyal analog yang bersifat kontiyu, sedangkan citra digital adalah citra yang dibentuk dari sinyal digital yang bersifat diskrit. Citra analog dihasilkan dari alat akuisisii citra analog, contohnya adalah mata manusia dan kamera analog. Gambar yang tertangkap oleh mata manusia dan foto atau film yang tertangkap oleh kamera analog merupakan contoh dari citra analog. Citra tersebut memiliki kualitas dengan tingkat kerincian (resolusi) yang sangat baik tetapi memiliki kelemahan diantaranya adalah tidak dapat disimpan, diolah, dan dipublikasikan di dalam komputer. Citra digital merupakan representasi dari fungsi intensitas cahaya dalam bentuk diskrit pada bidang dua dimensi. Citra tersusun oleh sekumpulan piksel _(picture element)_ yang memiliki koordinat _(x, y)_ dan ampiltudo _f(x, y)._ 

**2.2.1. Model Warna (Color Models)** Ruang warna adalah representasi matematis dari serangkaian warna (Gonzalez & Woods, 2002). Tiga model warna yang paling sering digunakan adalah _RGB_ (digunakan di dalam grafik komputer), _YIQ, YUV,_ dan _YCbCr_ (digunakan dalam video system), _CMYK_ (digunakan dalam _color printing_ ). Namu, tidak satupun dari ruang warna ini yang berhubungan dengan pengertian intuitif _hue_ , _saturation, dan brightness._ Ini menghasilkan pengejaran sementara dari model lain seperti _HIS_ dan _HSV_ , untuk menyederhanakan pemrograman, pemrosesan dan manipulasi penggunaan akhir. Semua ruang warna dapat berasal dari informais _RGB_ yang disediakan oleh perangkat seperti kamera dan pemindai. 

11 

## **2.2.1.1. Ruang Warna RGB** 

Model warna red, green, and blue ( _RGB_ ) banyak digunakan di seluruh komputer grafik, merupakan tiga warna aditif primer yaitu kompenen individual ditambahkan secara bersama untuk membentuk warna yang diinginkan dan di wakilkan oleh system kordinat kartesius tiga dimensi, gambar 2.1. Diagonal yang ditunjukkan dari kubus, dengan jumlah yang sama dari setiap komponen utama, mewakili berbagai tingkat abu-abu. Ruang warna RGB adalah pilihan paling umum untuk grafik komputer karena tampilan warna menggunakan merah, hijau, dan biru untuk membuat warna yang diinginkan. Oleh karena itu, pilihan ruang warna RGB menyederhanakan arsitektur dan desain sistem. 

**==> picture [303 x 151] intentionally omitted <==**

Gambar 2.1 Koordinat Warna RGB 

Gambar dalam bentuk _RGB_ bekerja dengan 24 bit dimana warna tiap chanel 

( _R, G, B_ ) mengandung 8 bit. Sistem yang dirancang menggunakan ruang warna 

_RGB_ dapat memanfaatkan sejumlah besar rutin perangkat lunak yang ada, karena ruang warna ini telah ada selama beberapa tahun. 

12 

## **2.2.1.2. Ruang Warna** _**L*a*b**_ 

_CIELAB_ merupakan model tiga dimensi, hanya dapat digambarkan apabila dalam ruang tiga dimensi, dan apabila diambil irisan kompones _a*_ dan _b*_ , maka akan mendapatkan diagram _chromaticity a*b*._ Dengan _CIELAB_ diberikan makna dari setiap dimensi yang dibentuk: 

a) Besaran _CIE L*_ untuk mendeskripsikan kecerahan warna, 0 untuk hitam dan _L*=_ 100 untuk putih b) Dimensi _CIE a*_ mendeskripsikan jenis warna hijau-merah, angka negative _a*:_ warna hijau; _CIE a*_ positif mengidentifikasikan warna merah. c) Dimensi _CIE b*_ untuk jenis warna biru-kuning, angka _negative b*_ mengidentifikasikan warna biru dan sebaliknya _CIE b*_ positif mengidentifikasikan warna kuning. Pengukuran warna dengan metode ini jauh lebih cepat dengan ketepatan yang cukup baik. Pada system ini term penilaian terdiri atas tiga parameter yaitu _L_ , _a_ , dan _b_ . Lokasi warna pada system ini ditentukan dengan koordinat _L*, a*, b*._ Notasi _L*:_ 0 (hitam); 100 (putih) menyatakan cahaya pantul yang menghasilkan warna akromatik putih, abu-abu dan hitam. Notasi _a*:_ warna kromatik campuran merah-hijau dengan niali (+) _a*_ (positif) dari 0 sampai +80 untuk warna merah, dan nilai (-) _a*_ (negative) dari 0 sampai -80 untuk warna hijau. Notasi _b*:_ warna kromatik campuran biru kuning dengan nilai (+) _b*_ (positif) dari 0 sampai +70 untuk warna kuning dan nilai (-) _b*_ (negative) dari 0 sampai -70 untuk warna biru. 

13 

**==> picture [176 x 148] intentionally omitted <==**

Gambar 2. 2 _LAB Color_ 

Ruang warna _XYZ_ , beberapa warna direperesentasikan sebagai nilai yang selalu positif. Perhitungan untuk transformasi warna dari ruang warna RGB ke _XYZ_ (dengan nilai referensi putih), adalah melalui perhitungan matriks tranformasi (Sinaga, 2019). Konversi ruang warna dari _type RGB_ ke _CIELab_ . 

Konversi _RGB-XYZ_ : 

**==> picture [213 x 41] intentionally omitted <==**

**==> picture [212 x 13] intentionally omitted <==**

Konversi _XYZ – L*a*b_ : 

**==> picture [231 x 150] intentionally omitted <==**

14 

## **2.2.2. Segmentasi Gambar** 

Segmentasiamerupakanaprosesamempartisi citraamenjadi beberapaadaerah 

atauaobjek. Segmentasi acitra padaaumumnya berdasarkan pada sifat _Discontinuity_ atau _Similaritya_ piksel. 

 Pendekatana _Discontinuity_ : mempartisi citra bila terdapat perubahan intesitasa secara tibaatiba _(Edge Based)._ 

 Pendekatan S _imilarity_ : mempartisi citra menjadi daerah daerah yang memilikiakesamaanasifatatertentu _(Region Based)_ . _Contoh: Thresholding, Region Growing, Region Splitting and Merging._ 

Citraadigital berisiapiksel piksel, segmentasiamerupakan partisiaatau membagiacitra kedalamabagian yangalebih kecil ( _segmen_ ). Segmentasiadilakukan dengan menggabungkanapiksel piksel yangamirip atau _similar_ (piksel iadan j), 𝑆𝑖𝑗 = 𝑆𝑖𝑗 ≥0. Tujuan segmentasi adalahamenggabungkan piksel yangamirip dengan nilai darianilai 𝑆𝑖𝑗 yang besar, harusapada segmen yangasama, sedangkan piksel yangatidak mirip padaasegmen yang berbedazbeda. Segmentasi dapatajuga dianggap sebagai prosesapembagian citra keadalam kelompok kelompokayang berarti yangasalingaberkaitan. 

Tujuan dari segmentasiaadalah membagi bagi citraadalam bagian atauaregion yang pentingauntuk aplikasiatertentu. Segmentasi dikerjakan denganaberbasis pada: _Greylevel_ . _Colour, Texture, Depth or Motion_ . Segmentasiamerupakan proses awaladari pengolahn citraaselanjutnya, contoh aplikasi segmentasiaantara lain: Indetifikasiaobjek berdasarkan ukuranadan bentuk dan identifikasiaobjek dari _movingapicture_ ( _objek based video compression_ 

15 

_MPEG4_ ). Terdapat beberapa macamasegmentasi, antara laina _greylevel histogram based segmentation thresholding_ dan _grelevel histogram based segmentation clustring_ . Didalamatipe segmentasi, terlebih dahulu didefinisikanacitra _input_ sebagaiacitra _input signal-to-noisearatio_ dalam hal rataarata ( _mean_ ) dari nilaia _greylevel_ piksel objekadan _piksel backgroundaand standard deviasi noise._ 

**==> picture [75 x 27] intentionally omitted <==**

Dapat mudah dipahamiabahwa segmentasi berbasisa _thresholding_ dengan 

memeriksa _histogram_ apada citra dengana _low noise_ dana _background_ , seperti 

gambaraberikut: 

**==> picture [182 x 167] intentionally omitted <==**

Gambar 2. 3 Histogramadengan 1 lembahadiantara 2 puncak 

**==> picture [310 x 105] intentionally omitted <==**

Gambar 2. 4 Contoh Segmentasiadengan _Histogram_ adan _Region_ 

16 

Dalam melakukan pengenalanasebuah objek diaantara banyak objekadalam citra, komputer harusamelakukan proses segmentasiaterlebih dahulu. Berdasarkan caraakerjanya, terdapat dua jenisasegmentasi citraayaitu: 

1. Segmentasi berdasarkan intensitasawarna (derajat keabuan). Berasumsiabahwa objek objekayang akan dipisahkanacendrung memiliki intensitasawarna yang berbedaabeda dan masingamasing objek memiliki warnaayang seragam. Salahasatu teknik berdasarkan intensitasawarna adalah _MeanaClustering_ . Pada _meanaclustering_ dilakukan pembagian citraadengan membagi _histogram_ acitra. Kelemahan segmentasi berdasarkanaintensitas warna (derajat keabuan) antaraalain harus tauadengan tepat berapaajumlah objek yang ada padaacitra serta citraahasil kurang bagusajika pada citra terdapatabeberapa objek denganawarna pada masingamasing objeknya bervariasiaatau pada setiapaobjek memiliki warnaayang sama. 

2. Segmentasi berdasarkanakarakteristik. Yaitu mengelompokkan bagianabagian citra yangamemiliki karakteristik yangasama berupa perubahanawarna antara titik yangaberdekatan, nilai rataarata dari bagianacitra tersebut. Untukamenghitung atau menentukan karakteristikadigunakan perhitunganastatistik, misalnya _varian_ , standaradeviasi, teori probabilitas, trasformasia _fourier_ . Salah satu teknikasegmentasi berdasarkan karakteristikaadalah _Split and Merge_ . Proses tersebutadilakukan secara rekrusifakarena pada setiapasaat dilakukan prosesayang sama tetapiadengan data yang selaluaberubah. 

17 

Sedangkan berdasarkanametodenya, terdapat dua pendekatanautama dalam segmentasiacitra yaitu didasarkanapada tepi _(Edge Based)_ danadidasarkanapada wilayah _(Region Based)_ . Segmentasi berdasarkan tepiamembagi citra berdasarkan diskontinuitasadia antara subawilayah _(Sub Region)_ , sedangkanasegmentasi berdasarkan wilayah bekerjaaberdasarkan keseragaman yangaada pada subawilayah tersebut. Hasil dari segmentasiacitra adalah sekumpulanawilayah yang melingkupiacitra tersebut, atauasekumpulan kontur yangadiekstrak dariacitra (pada deteksi tepi). Tiap pikseladalam suatu wilayahamempunyai kesamaanakarakteristik atau propertiayang dapatadihitung ( _ImageaProperties_ ), seperti: warna ( _Color_ ), intensitas ( _Intensity_ ), tekstur ( _Texture_ ). 

**==> picture [271 x 131] intentionally omitted <==**

Gambar 2. 5 GambaraSegmentasi Pesawat 

Segmentasi wilayah merupakanapendekatan lanjutan dariadeteksi tepi. Dalamadeteksi tepi segmentasiacitra dilakukan melaluiaidentifikasi batasabatas objek _(boundaries of object)_ . Batas merupakan lokasi dimana terjadi perubahan intensitas. Dalam pendekatan didasarkan padaawilayah, maka identifikasi dilakukanamelalui wilayah yangaterdapat dalam objekatersebut. Salah satu cara untukamendefinisikan segmentasiacitra adalah sebagaiaberikut. 

18 

Sekumpulan wilayah {𝑅1, 𝑅2, 𝑅3, … . 𝑅𝑛} merupakanasegmentasi citra _**R**_ keadalam _**n**_ wilayah jika: 

**==> picture [79 x 14] intentionally omitted <==**

**==> picture [109 x 12] intentionally omitted <==**

III. 𝑅𝑖 𝑡𝑒𝑟ℎ𝑢𝑏𝑢𝑛𝑔 𝑖= 1, 2, … 𝑛 

IV. Terdapatasuatu predikat yangamerupakan ukuranahomogenesis 

wilayah: 

a. 𝑃(𝑅𝑖) = 𝑇𝑅𝑈𝐸, 𝑖= 1,2, … 𝑛 

b. 𝑃(𝑅𝑖 ∪𝑅𝑘 = 𝐹𝐴𝐿𝑆𝐸, 𝑖≠𝑘 𝑑𝑎𝑛 𝑅𝑖 𝑎𝑑𝑗𝑎𝑛𝑐𝑒𝑛𝑡 𝑅𝑘 

## **2.2.3. Ekstarksi Ciri** 

Merupakan tahapanamengekstarak ciri atauainformasi dari objekadi dalam 

citra yang inginadikenali atau dibedakanadengan objek lainnya. Ciriayang telah 

diekstarkasiakemudian digunakan sebagaiaparameter atau nilai masukan untuk 

membedakanaantara objek satu denganalainnya pada tahapanaidentifikasi atau klasifikasi. Ciri umumayang diekstrakaantara lain: 

## **2.2.3.1. Ekstraksi Ciri Bentuk** 

Untuk membedakan bentukaobjek satu dengan lainnya, dapat menggunakan 

parameterayang disebutadengan ‘ _eccentricity’_ . _Eccentricity_ merupakananilai perbandingan antara jaraka _foci ellips minor_ dengana _foci ellips mayor_ suatuaobjek. 

_Eccentricity_ memiliki rentanganilai antara 0 hingga 1. Objek yangaberbentuk memanjang atau mendekatiabentuk garisalurus, nilai _Eccentricity_ nyaamendekati angka 1, sedangkanaobjek yang berbentukabulat atau lingkarananilai 

19 

_Eccentricity_ nya mendekatiaangka 0. Perhitungan _Eccentricity_ diilustrasikanapada 

gambar di bawahaini: 

**==> picture [212 x 100] intentionally omitted <==**

Gambar 2. 6 Ilustrasi Perhitungan _Eccentricity_ 

Parameter lain yang dapat digunakanauntuk membedakan bentukasuatu 

objekayaitu ‘ _metric_ ’. _Metric_ merupakan nilaiaperbandingan antara luas danakeliling objek. _Metric_ memiliki rentanganilai antara 0 hingga 1. Objek yang berbentukamemanjang atau mendekatiabentuk garis lurus, nilaia _metric_ nya mendekati angka 0, sedangkanaobjek yang berbentukabulat ataualingkaran, nilai _metric_ nya mendekatiaangka 1. Perhitungan _metrica_ diilustrasikan padaagambar dibawah ini: 

**==> picture [211 x 112] intentionally omitted <==**

Gambar 2. 7 Ilustrasi Perhitungan Matric 

20 

## **2.2.3.2. Ekstataksi CiriaUkuran** 

Untuk membedakan ukuranaobjek satu denganayang lainnya menggunakan 

parameter luas dan keliling. Luasamerupakan banyaknya pikselayang menyusun 

suatuaobjek. Sedangkan kelilingamerupakan banyaknyaapiksel yang mengelilingi 

suatuaobjek. 

**==> picture [214 x 103] intentionally omitted <==**

Gambar 2. 8 Contoh Ciri Ukuran 

## **2.2.3.3. Ekstraksi CiriaGeometri** 

Ciri geometri merupakanaciri yang didasarkan padaahubungan antara dua buahatitik, garis, atau bidangadalam citra digital. Ciri geometriadi antaranya adalah jarakadan sudut. Jarakaantara dua buahatitik (dengan satuan piksel) dapat ditentukanamenggunakan persamaana _Euclidean, Minskowski, Manhattan,_ danalain 

lain. Jarakadengan satuan pikselatersebut dapat dikonversikanamenjadi satuan 

panjangaseperti _millimeter_ , _centimeter_ , _meter_ , danalain lain denganacara 

membaginya denganaresolusi spasial. Sedangkanasudut antara duaabuah garis 

dapataditentukan dengan perhitunganatrigonometri maupun dengannalisisavektor. 

**==> picture [241 x 107] intentionally omitted <==**

Gambar 2. 9 Contoh Bentuk Bentuk Geometri 

21 

## **2.2.3.4. Ekstraksi Ciri Tekstur** 

Untuk membedakan teksturaobjek satu dengan yangalainnya dapat menggunakanaciri statistic ordeapertama atau ciriasatatistik ordeadua. Ciri orde pertamaadidasarkan pada karakteristikahistogram citra. Ciri ordeapertama umumnya digunakanauntuk membedakan teksturamakrostruktur (perulangan pola local secaraaperiodic). Ciri orde pertamaaantara lain: _Mean, Variance, Skewness, Kurtois,_ dana _Entropy_ . Sedangkanaciri orde duaadidasarkan padaaprobabilitas hubungan ketetanggaanaantara dua pikselapada jarak dan orientasasudut tertentu. Ciri ordeadua umumnya digunakanauntuk membedakan teksturamikrostruktur (pola local dan perulanganatidak begitu jelas). Ciri orde duaaantara lain: _Angular Second Moment, Contras, Correlation, Variance, Invers Different Moment, dan Entropy_ . Analisisateksture juga dapatadilakukan dalam domainafrekuensi antara lain menggunakana _Filter Gabor_ . 

**==> picture [226 x 99] intentionally omitted <==**

Gambar 2. 10 Contoh Tekstu Citra 

## **2.2.3.5. Ekstraksi Ciri Warna** 

Untuk membedakan suatuaobjek dengan warnaadapat mengunakananilai 

_hue_ yangamerupakan reperesentasi dari cahayaatampak (Merah, Jingga, Kuning, Hijau, Biru, Ungun). Nilaiahue dapat dikombinasikanadengan nilai _Saturationa_ dan _Value_ yang merupakan tingkat kecerahan suatuawarna. Untuk mendapatkanaketiga 

22 

nilaiatersebut, perlu dilakukanakonversi ruang warna citra yangasemula _RGB_ ( _Red, Green, Blue_ ) menjadia _HSV_ ( _Hue, Saturation, Value_ ) melaluiapersamaan berikut: 

**==> picture [48 x 68] intentionally omitted <==**

**==> picture [123 x 109] intentionally omitted <==**

Perhitungan nilai _Hue:_ 

**==> picture [208 x 112] intentionally omitted <==**

Perhitungan nilai _Saturation_ : 

**==> picture [96 x 45] intentionally omitted <==**

Perhitungan nilai _Value_ : 

𝑉= 𝐶𝑚𝑎𝑥 

23 

**==> picture [241 x 110] intentionally omitted <==**

Gambar 2. 11 _RGB ColoraSpace_ dan _HSVaColor Space_ 

## **2.2.4. Operasi Morfologis** 

Pemrosesan gambar morfologis adalahakumpulan operasiayang terkait dengan bentuk atau morfologi fitur dalam suatu gambar. Operasiamorfologis diterapkan untuk menghilangkan _noise_ dan diskontinuitas dari latar depan yang diekstraksi. Operasi morfologis mempengaruhi bentuk, struktur, atau bentuk suatu 

objek. Diterapkan pada gambar biner. Mereka digunakan dalam pemrosesan pra 

atau pasca (penyaringan, penipisan, dan pemangkasan) atau untuk mendapatkan 

representasi atau deskripsi bentuk objek atau daerah. Dua operasi morfologi utama 

adalah _Dilation_ dan _Erosion_ . _Dilation_ memungkinkan objek untuk mengembang, 

sehingga berpotensi mengisi lubang kecil dan menghubungkan objek terpisah. 

_Erosion_ menyusutkan objek dengan mengikis batas-batasnya. Operasi ini dapat 

custom untuk suatu aplikasi dengan pemilihan yang tepat dari elemen penataan, 

yang menentukan dengan tepat bagaimana objek akan mengembang atau menyusut. 

## **2.2.4.1. Translasia** 

Translasi artinya sebuah citra dideses pada arah _(x, y)_ dimana _(x, y)_ adalah 

koordinat matriks. Operasi operasi translasi dinyatakan sebagai: 

**==> picture [167 x 13] intentionally omitted <==**

24 

## **2.2.4.2. Dilasi** 

Operasi dilasiadilakukan untuk memperbesaraukuran segmen objek dengan 

menambah lapisanadi sekeliling objek sehinggaacitra hasil dilasiacendrung menebal. Operasi dilasiaakan melakukan prosesapengisian padaacitra asal yang memilikiaukuran lebih keciladibandingkan _structuringaelement_ ( _strel_ ). Dilasi _A_ 

oleh _Ba_ dinotasikan denganaA⊕ B dan didefinisikanasebagai: 

**==> picture [81 x 32] intentionally omitted <==**

## **2.2.4.3. Erosi** 

Operasi erosi adalahakebalikan dari operasi dilasi. Pada operasi ini, ukuran 

objek diperkecil dengan mengikisasekeliling objek sehingga citra hasil cenderung diperkecil menipis. Operasi erosi akan melakukanapengurangan padaacitra asal yang lebih kecil dibandingaelemen penstruktur ( _strel_ ). Erosi _A_ oleh _B_ dinotasikan 

AƟB didefinisikan sebagai: 

**==> picture [100 x 59] intentionally omitted <==**

## **2.2.4.4. Opening** 

Proses opening padaasebuah citra _A_ oleh a _strel B_ dinotasikanadengan _A_ ∘ _B_ 

dan didefiniksikanasebagai proses erosiayang dilanjutkan denganaproses dilasi dimana keduaaproses tersebut deilakukanasecara berulang untukasemua titik(( _x,y_ ). 

**==> picture [168 x 14] intentionally omitted <==**

25 

## **2.2.5.** _**K Nearest Neighbor**_ **a** 

Dalam pengenalanapola, algoritma _k NearestaNeighbor (k- NN)_ adalah metodeanon parametrik yang digunakan untukakasifikasi dan regresi. Dalam kedua kasus, input terdiri dari _k_ contohapelatihan terdekatadiruang fitur. Outpunya tergantung pada _k- NN_ digunakan untuk klasifikasi atau regresi: 

 Dalamaklasifikasi _k-NN,_ output adalah keanggotaanakelas. Suatu objek diklasifikasikan oleh suara pluralitas tetangganya, dengan objek yang ditugaskan ke kelas paling umum diantara tetangga terdekat. Jika _k_ = 1, maka objek ditugaskan hanya untuk kelas tetangga terdekat itu. 

 Dalam regresi _k-NN, output_ aadalah nilai propertiauntuk objek. Nilai 

ini adalah rata rataanilai _k_ tetangga terdekat. 

_k- NN_ adalah jenis pembelajaran berbasis contoh ( _Instace Based Learning)_ , atau pembelajaran malas ( _Lazy Learning_ ), dimana fungsinya hanya didekati secara lokal dan semua perhitungan ditangguhkan hingga klasifikasi. 

Baik untuk klasifikasi atau regresi, teknik yang berguna adalah menetapkan bobot pada kontribusi tetangga, sehingga tetangga yang lebih dekat berkontribusi lebih banyak ke rata rata daripada yang lebih jauh. Sebagai contoh, skema pembobotan umum terdiri dari memberikan masing masing tetangga _1 / d,_ dimana _d_ adalah jarak ke tetangga. 

Tetangga diambil dari satu set objek yang kelasnya (Untuk klasifikasi _k-NN_ ) atau nilai properti objek (untuk regresi _k-NN_ ) diketahui. Ini dapat dianggap sebagai pelatihan yang ditetapkan untuk algoritma, meskipun tidak diperlukan langkah pelatihan eksplisit. 

26 

## **2.2.5.1.Cara Kerja Algoritma** _**k-NN**_ 

**==> picture [140 x 127] intentionally omitted <==**

## Gambar 2. 12 Contoh Klasifikasi _k- NN_ 

Sampel uji (titik hijau) harus diklasifikasikan menjadi kotak biru atau segitiga merah. Jika _k_ =3 (lingkaran garis padat) itu ditugaskan untuk segitiga merah karena ada 2 segitiga dan hanya 1 persegi didalam lingkaran dalam. Jika _k_ =5 (lingkaran garis putus putus) itu ditugaskan ke kotak biru (3 kotak vs 2 segitiga didalam lingkaran luar). 

Contoh pelatihan adalah vektor dalam ruang fitur multidimensi, masing masing dengan label kelas. Fase pelatihan algoritma hanya terdiri dari penyimpanan vektor fitur dan label kelas dari sampel pelatihan. 

Dalam fase klasifikasi, _k_ adalah konstanta yang ditentukan pengguna, dan vektor yang tidak berlabel ( _query_ atau _test point_ ) diklasifikasikan dengan menetapkan label yang paling sering diantara sempel pelatihan _k_ yang terdekat dengan titik _query_ itu.. 

Tujuan dari algoritma ini adalah mengklasifikasikan objek baru berdasarkan atribut dan sampel latih. Pengklasifikasian tidak menggunakan model apapun untuk dicocokkan dan hanya berdasarkan pada memori. Diberikan titik uji, akan ditemukan sejumlah _k_ (titik training) yang paling dekat dengan titik uji. Klasifikasi 

27 

|menggunakan voting mayoritas diantara klasifikasi dari_k_objek. Algoritma_k-NN_|
|---|
|menggunakan klasifikasi ketetangga sebagai nilai prediksi dari smaple uji yang|
|baru. Matrik jarak yang umum digunakan untuk variable kontinu adalah_Euclidean_|
|_Distance_. Untuk variable diskrit, seperti untuk klasifikasi teks, matrik lain dapat|
|digunakan, seperti matrik tumpang tindih (atau_Hamming Distance_).|
|Algoritma_k-NN_menggunakan klasifikasi ketetanggaan (_neighbor_) sebagai|
|nilai prediksi dari_query instance_yang baru. Algoritma ini sederhana, bekerja|
|berdasarkan jarak terpendek dari_query instance_ke_taraining_sampel untuk|
|menentukan ketetanggaannya (Rizal, 2013).|
|Ketepatan algoritmaa_k-NN_sangat dipengaruhiaada atau tidaknyaafitur fitur|
|yangatidak relevan atauabobot fitur tersebutatidak setara denganarelevansinya|
|terhadapaklasifikasi. Riset terhadapaalgoritma ini sebagianabesar membahas|
|bagaimanaamemilih dan memberiabobot terhadap fituraagar performaaklasifikasi|
|menjadi lebihabaik. Langkah langkahauntuk menghitungaAlgoritma_k-NN_:|
|1. Menentukanaparameter_k_(jumlahaparameter terdekat)|
|2. Menghitungakuadrat<br>jaraka_Euclide_<br>_(QueryaInstance)_<br>masing|
|masing objek terhadap dataasampel yangadiberikan.|
|3. Mengurutkanaobjek objek tersebutakedalam kelompok yang|
|mempunyaiajarak_Euclidea_terkecil.|
|4. Mengumpulkanakategori_y (Klasifikasi NearestaNeighbor)_|
|5. Dengan menggunakanakategori nearest neighborayang paling|
|mayoritas, makaadapat diprediksikan nilaia_query instancea_yang|
|telah dihitung.|



28 

## **2.2.5.2. Perhi** t **ungan Jarak** 

Perhitungan jarak atau distance ( _d_ ), adalah bagian penting dalam algoritma 

_k-Nearest Neighbor._ Ada beberapa cara perhitungan jarak _k-NN_ diantaranya: 

## **1.** _**Euclidean Distance**_ 

_Euclidean Distance_ adalah matrik jarak yang paling umum digunakan 

dalam set data dimensi rendah. Ini juga dikenal sebagai norma _L2_ . 

_Euclidean Distance_ adalah cara biasa dimana jarak diukur di dunia 

nyata. Rumus _Euclidean Distance:_ 

**==> picture [137 x 55] intentionally omitted <==**

**----- Start of picture text -----**<br>
𝑛<br>𝑖 −𝑦𝑖) [2] )<br>𝑖=1<br>𝑑(𝑥, 𝑦) = √(∑(𝑥<br>**----- End of picture text -----**<br>


Dimana: 

 𝑥𝑖= sampel data 

 𝑦𝑖= data uji 

 𝑖  =variable data 

 𝑑 =jarak 

 𝑛 =dimensi data 

Ide rumus ini dari rumus _Pythagoras_ : 

𝑐= √𝑎[2] + 𝑏[2] 

Sementara _Euclidean Distance_ berguna dalam dimensi rendah, dan 

tidak bekerja dengan baik dalam dimensi tinggi dan untuk variable 

kategori. Kelemahan _Euclidean Distance_ adalah mengabaikan kesamaan antara atribut. Setiap atribut deperlakukan berbeda dari semua atribut. 

29 

## **2.** _**Manhattan Distance**_ 

Disebut berdasarkan pada kota _Manhattan_ yang tersusun menjadi 

blok blok, sehingga sering disebut _City Block Distance_ , juga sering 

disebut _Absolute Value_ . Rumusnya adalah: 

𝑛 𝑖 −𝑦𝑖| 𝑖=1 𝑑(𝑥, 𝑦) = √∑|𝑥 

Rumus ini mencarai jarak hanya dengan menjumlahkan semua selisih dari jarak 𝒙𝒊 dan 𝒚𝒊. 

## **3.** _**Minkowski Distance**_ 

Adalah generalisasi jarak _Eculidean_ dan _Manhattan_ . Rumus ini 

diambil dari konsep aljabar dengan vektor berdimensi _n_ dan _r_ . 

Rumusnya adalah: 

𝑛 𝑖 −𝑦𝑖|[𝑟] )1⁄𝑟 𝑑(𝑥, 𝑦) = (∑|𝑥 𝑖=1 

Dimana: 

 𝑥𝑖= sampel data 

 𝑦𝑖= data uji 

 𝑖  =variable data 

- 𝑑 =jarak 

- 𝑛 =dimensi data 

 _r =_ parameter 

30 

**==> picture [401 x 612] intentionally omitted <==**

**----- Start of picture text -----**<br>
|||||||
|---|---|---|---|---|---|
|4.|Chebychev Distance|
|Algoritma ini adalah algoritma yang paling simpel dari dari semua|
|algoritma mesin|learning|, rumus ini mencari jarak yang terbesar|
|antara 𝒙𝒊 dan 𝒚𝒊. Rumusnya adalah:|
|𝑑(𝑥, 𝑦) = 𝑚𝑎𝑥𝑖=1𝑛||𝑥𝑖|−𝑦𝑖||
|2.2.5.3. Kinerja Algoritma|k-NN|
|Dipengaruhi oleh tiga faktor utama:|
|1.|Fungsi jarak atau|metric|jarak digunakan untuk menentukan jarak|
|tetangga terdekat.|
|2.|Aturan keputusan digunakan untuk memproleh klasifikasi dari|k-|
|Nearest Neighbor|.|
|3.|Jumlah tetangga yang digunakan untuk mengklasifikasikan contoh|
|baru.|
|2.2.5.4. Kelebihan dan Kekurangan Algoritma|k-NN|
|Algoritma|k-NN|memiliki beberapa kelebihan antara lain:|
||Sangat|non linier|
||Mudah dipahami dan diimplementasikan|
||Tangguuh terhadap data|training|sample|yang|noisy|
||Efektif apabila data|training|samplenya besar|
||Memiliki konsistensi yang kuat|
||Asymptotically coorect|

**----- End of picture text -----**<br>


31 

Algoritma _k-NN_ juga memiliki beberapa kekurangan antara lain: 

- Perlu menentukan _k_ (jumlah tetangga terdekat) 

- Tidak menangani nilai hilang ( _missing value_ ) secara implisit 

- Sensistif terhadap data pencilan ( _outlier_ ) 

- Rentan terhadap _variable_ yang _non informative_ 

- Rentan terhadap dimensional yang tinggi 

- Rentan terhadap perbedaan rentang variabel 

- Pembelajaran berdasarkan jarak tidak jelas 

- Nilai komputasi yang tinggi. 

## _**2.2.6. K Fold Cross Validationa**_ 

_K-fold cross validation_ adalah salah satu metode untuk mengevaluasi kinerja _classifier, k-fold cross validation_ mebagi data menjadi data _training_ dan _testing_ dalam _K_ bagian. Metode _k-fold cross validation_ bekerja dengan cara 

mempartisi himpunan data _D_ secara acak menjadi _k -fold_ (subhimpunan) yang saling bebas: _f1, f2, f3,_ … _fk,_ sehingga masing masing _fold_ berisi 1/k bagian data (Suyatno, 2017). Sebagai gambaran, jika kita melakukan 5- _Fold Cross-Validation_ maka desain data eksperimennya sebagai berikut: 

Tabel 2. 1 Ilustrasi _k-Fold Cross Validation_ 

|K 1|test|train|train|train|train|
|---|---|---|---|---|---|
|K 2|train|test|train|train|train|
|K 3|train|train|test|train|train|
|K 4|train|train|train|test|train|
|K 5|train|train|train|train|test|



32 

Percobaan diatas adalah contoh ilustrasi dari 5 _k-fold cross validation_ yang artinya adalah melakukan percobaan sebanyak 5 kali tahapan. Dari hasil percobaan ini, kita akan mencatat nilai evaluasi performa dari model tersebut dengan menggunakan _confussion matrix_ , kemudian menentukan nilai rata rata dari setiap percobaan. Maka akan ditemukan percobaan mana yang dapat dijadikan acuan dari penggunaan suatu model algoritma yang dipilih. K 1, yaitu menjadikan bagian partisi pertama menjadi data _testing_ dan partisi lainnya menjadi data _training_ dan seterusnya hingga K 5. Tujuan _cross validation_ adalah untuk menguji kemampuan model untuk memprediksi data baru yang tidak digunakannya, untuk menandai masalah seperti _overfitting_ atau bias seleksi (Cawley & Talbot, 2010) dan untuk memberikan wawasan tentang bagaimana model akan digeneralisasikan ke dataset independen ( yaitu, dataset yang tidak diketahui misanya dari masalah nyata). Satu putara _cross validation_ melibatkan partisi sebuah sampel dari data yang menjadi pelengkap subset, melakukan analisis pada suatu bagian (disebut _trainingset_ ), dan memvalidasi analisis pada subset lain (disebut validasi set atau pengujian set). Untuk mengurangi variabilitas, dalam sebagian besar metode, beberapa putaran validasi silang dilakukan dengan menggunakan partisi yang berbeda, dan hasil validasi digabungkan (dirata rata) selama putran untuk memberikan perkiraan kinerja prediksi model. Singkatnya _cross validation_ menggabungkan (rata rata) ukuran kebugaran dalam prediksi untuk mendapatkan perkiraan kinerja prediksi model yang lebih akurat (Seni & Elder, 2010). 

## **BAB III** 

## **DESAIN PENELITIAN** 

## **3.1. Desain Sistem** 

Untuk membangun aplikasi deteksi dan klasifikasi bangunan maka diperlukan desain sistem untuk penerapan aplikasi secara rinci dan teratur sesuai yang diinginkan. Berikut desain sistem yang diterapkan pada aplikasi 

ini. 

**==> picture [398 x 277] intentionally omitted <==**

Gambar 3. 1 Desain Sistem 

Pada desain sistem gambar 3.1 ditampilkan alur aplikasi mulai dari input, 

proses dan output sistem. 

33 

34 

## **3.1.1. Citra Satelit** _**RGB**_ 

Pada Tahap ini dilakukan _crooping_ citra Satelit _Google Earth_ , kemudian 

disimpan kedalam format ( _*.jpg_ ) yang selanjutnya akan diinputkan kedalam sistem 

untuk dilakukan proses segmentasi. 

**==> picture [259 x 118] intentionally omitted <==**

Gambar 3. 2 Citra Satelit Hasil Croping 

Citra satelit yang diambil oleh _Software Google Earth_ merupakn hasil foto 

yang ditangkap daris satelit di luar angkasa. Pada _Software Google_ ketinggian citra 

pengambilan citra diartikan sebagai nilai perbesaran gambar atau _zoom_ . Satuan panjang yang digunakan untuk pengambilan ketinggian gambar pada _Google Earth_ 

ini mengguanakan satuan panjang meter. Dalam penelitian ini Citra satelit diambil 

dari ketinggian 700-800 meter. Ketinggian dan intensitas cahaya citra sangat 

berpengaruh terhadap kualitas gambar hasil _crooping_ . 

## **3.1.2. Segmentasi** 

Pada tahap ini dilakukan segmentasi pada citra satelit setelah diinputkan 

kedalam sistem, proses segmentasi bertujuanauntuk memisahkan antaraaobjek 

_foreground_ dengana _background_ . Pada umumnyaahasil segmentasiacitra berupa citra bineradimana objek _foreground_ ayang dikehendaki berwarnaputih (1), sedangkan _background_ ayang ingin dihilangkanaberwarna hitam (0). 

35 

## **3.1.2.1. Proses Segmentasi** 

**==> picture [305 x 250] intentionally omitted <==**

Gambar 3. 3 Proses Segmentasi 

**1. Menampilkan citra** _**RGB**_ 

**==> picture [308 x 141] intentionally omitted <==**

Gambar 3. 4 Inputan Citra _RGB_ 

_Input_ citra _rgb_ hasil _Crooping_ dari _Google Earth_ . Ruang warna RGB terdiri 

dari semua kemungkinan warna yang dibuat dengan kobinasi _Red, Green_ dan _Blue_ . 

36 

## **2. Konversi warna** 

**==> picture [351 x 169] intentionally omitted <==**

Gambar 3. 5 Proses Konversi Warna 

Sebelum melakukan proses segmentasi citra _RGB_ dikonversikan ke ruang 

warna _CIE L*a*b*. CIE L*a*b*_ didefinisikan oleh cahaya ( _L_ ), dan dimensi lawan warna _a_ dan _b_ , yang didasarkan pada kordinat ruang waran _XYZ_ yang terkompresi. 

Tranformasi perhitungan niali _RGB_ : 

**==> picture [215 x 88] intentionally omitted <==**

**----- Start of picture text -----**<br>
𝑟 𝑅<br>𝑅=  ; indeks warna merah ( red )=<br>255 𝑅+𝐺+𝐵<br>𝑔 𝐺<br>𝐺= ; indeks warna hijau ( green )=<br>255 𝑅+𝐺+𝐵<br>𝑏 𝐵<br>𝐵=  ; indeks warna biru ( blue ) =<br>255 𝑅+𝐺+𝐵<br>**----- End of picture text -----**<br>


Tranformasi _RGB_ ke _CIELAB_ dimulai dengan melakukan perhitungan sebagai berikut: 

𝑋= 0,412453𝑅+ 0,357580𝐺+  0,180423𝐵 

𝑌= 0,212671𝑅+ ),715160𝐺+  0,072169𝐵 

𝑍=  0,019334𝑅+ 0,119193𝐺+ 0,950227𝐵 

37 

Selanjunta _L*a*b*_ didefinisikan sebagai berikut: 

**==> picture [132 x 72] intentionally omitted <==**

**==> picture [132 x 28] intentionally omitted <==**

Dalam hal ini, _f(q)_ dihitung seperti berikut: 

**==> picture [212 x 45] intentionally omitted <==**

𝑋𝑛𝑌𝑛𝑍𝑛 diperoleh melalui _R=G=B=1_ dengan jangkauan _R,G,B_ berupa 

[0,1]. 

**==> picture [193 x 219] intentionally omitted <==**

Gambar 3. 6 Hasil Konversi _RGB_ ke _LAB_ 

Segmentasi warna menggunakan warna _L*a*b*,_ menampilkan komposisi 

warna menjadi enam kelompok yaitu: _background_ , kuning, magenta, ungu, merah dan hijau. 

38 

Segmentasi selanjutnya memisahkan objek _Foreground_ adengan _Background_ amenggunakan metode _k MeanaClustering_ . Proses _clustering_ dilakukanadengan cara mengkonversikanaruang warna citra _RGB_ amenjadi _L*a*b_ 

aKomponen _a_ dan _b_ dariacitra _L*a*b_ digunakanasebagai nilaiamasukan dalam 

algoritmaa _k-Mean_ . 

- a. Menampilkan citra _RGB_ 

**==> picture [264 x 119] intentionally omitted <==**

Gambar 3. 7 Citra RGB 

Inputan citra _RGB_ kedalam sistem untuk di konversikan kedalam ruang 

warna _LAB_ . 

- b. Konversi _RGB_ ke _LAB_ 

**==> picture [267 x 122] intentionally omitted <==**

Gambar 3. 8 Konversi _RGB_ ke _L*a*b_ 

Setelah dikonversikan dari citra _RGB_ ke _LAB_ maka didapatkan citra _LAB_ 

yang selanjutnya akan disegmentasi dengan membaginya menjadi beberapa kluster. 

39 

- c. Hasil Segmentasi 

**==> picture [251 x 114] intentionally omitted <==**

Gambar 3. 9 Citra Hasil Segmentasi 

Hasil segmentasi menujukakkan citra _LAB_ telah terbagi mejadi 3 cluster 

warna yang membedakan objek satu dengan yang lainnya. 

**==> picture [271 x 125] intentionally omitted <==**

Gambar 3. 10 Hasil Segmentasi _Cluster_ 1 

Hasil segmentasi pada objek cluster 1 menujukan objek jalan dan lahan dan 

objek objek yang memiliki luasan yang besar. 

**==> picture [271 x 123] intentionally omitted <==**

Gambar 3. 11 Hasil Segmentasi _Cluster_ 2 

40 

Hasil segmentasi pada cluster 2 menunjukan objek tumbuhan. 

**==> picture [267 x 121] intentionally omitted <==**

Gambar 3. 12 Hasil Segmentasi _Cluster_ 3 

Hasil segmentasi pada cluster 3 menujukan objek banguan 

- d. Memilih cluster 

**==> picture [273 x 123] intentionally omitted <==**

Gambar 3. 13 Cluster Terdapat _Foreground_ Bangunan 

Memilih klusterayang terdapat _aforeground_ (bangunan) Pemilihan didasarkan padaakluster yang memiliki luasanaobjek palingakecil. Setelah 

diperoleh citraa _foreground_ saja selanjutnyaadilakukan proses operasiamorfologi yaitu _FillingaHoles_ untuk menyempurnakanahasil segementasi dana _bwareaopen_ untuk menghilangkana _noise_ . 

41 

**==> picture [267 x 120] intentionally omitted <==**

Gambar 3. 14 Hasil Morfologi _Filling Holes_ dan _Bwarea Open_ 

Hasil segementasi berupa citra biner (bangunan yang terdeteksi) yang 

selanjutnya akan dilakukan ektraksi ciri bentuk citra untuk menghitung jumlah dan klasifikasi tipe bangunan. 

## **3.1.3. Ekstraksi Ciri** 

Proses pengenalan objekadalam citra umumnyaamembutuhkan suatu ciri 

yang dapatamembedakan anataraobjek satu dengan objek lainnya. Ektaksi ciri citra 

merupakan tahapan mengekstrakaciri atau informasi dariaobjek didalam citra yang 

inginadikenali atau dibedakanadengan objek lainnya. Ciri yang telah diektrak selanjutnya digunakan sebagaiaparameter atau nilai masukan untuk membedakan antara objek satu denganalainnya pada tahap identifikasi atau klasifikasi. 

Ciri merupkan karakteristikaunik dari suatu objek, ciri dibedakan menjadi 

ciri alami merupakan bagian dari gambaramisalnya kecerahan dan tepi objek, sedangkan ciri buatanamerupakan fitur yang diperoleh dengan operasi tertentu pada gambar misalnya histogramatingkat keabuan. 

Citra disegmentasi dan didapatkan obejek bangunan hasil deteksi selanjutnya mengektraksi ciri masing masing objek dari citra hasil deteksi berdasarkan Luas, Keliling, _Eccentricity_ , dan _Metric_ . 

42 

**==> picture [232 x 318] intentionally omitted <==**

Gambar 3. 15 _Flowchart_ Ektraksi Ciri 

Citra biner hasil deteksi menunjukkan hasil bangunan terdeteksi yang akan 

diektrasi ciri ukuran (Luas dan Keliling) dan bentuk ( _Metric_ dan _Eccentricity_ ) 

sebagai ciri yang akan mebedakan objek satu dengan objek lainnya. Ciri ini akan digunakan sebagai acuan klasifikasi bangunan dengan metode _kNN_ untuk mengklasifikasikan setiap bangunan yang terdeteksi. 

**==> picture [281 x 127] intentionally omitted <==**

Gambar 3. 16 Labelling Objek 

43 

Labeling objek dilakukan untuk menandai objek yang terdeteksi, kemudian menghitung jumlah objek (bangunan). 

Tabel 3. 1 Luas, Keliling, _Eccentricity_ , dan _Metrik_ Hasil Ekstraksi 

|Object number = 1<br>Area = 2803<br>Perimeter = 1091,9483<br>Metric = 0,029541<br>Eccentricity= 0,98253|Object number = 2<br>Area = 948<br>Perimeter = 189,3381<br>Metric = 0,33231<br>Eccentricity= 0,82025|Object number = 3<br>Area = 1271<br>Perimeter = 197,7229<br>Metric = 0,40855<br>Eccentricity= 0,85386|
|---|---|---|
|Object number = 4<br>Area = 139<br>Perimeter = 54,3848<br>Metric = 0,59057<br>Eccentricity= 0,93575|Object number = 5<br>Area = 2842<br>Perimeter = 342,2325<br>Metric = 0,30492<br>Eccentricity= 0,95966|Object number = 6<br>Area = 774<br>Perimeter = 128,9533<br>Metric = 0,58491<br>Eccentricity= 0,74418|
|Object number = 7<br>Area = 1873<br>Perimeter = 289,463<br>Metric = 0,28091<br>Eccentricity= 0,90677|Object number = 8<br>Area = 2140<br>Perimeter = 256,0488<br>Metric = 0,41018<br>Eccentricity= 0,91055|Object number = 9<br>Area = 910<br>Perimeter = 124,8112<br>Metric = 0,73408<br>Eccentricity= 0,51193|
|Object number = 10<br>Area = 1516<br>Perimeter = 182,2082<br>Metric = 0,57382<br>Eccentricity = 0.,61043|Object number = 11<br>Area = 1721<br>Perimeter = 218,4508<br>Metric = 0,45319<br>Eccentricity = 0,84461|Object number = 12<br>Area = 1017<br>Perimeter = 150,6102<br>Metric = 0,56341<br>Eccentricity = 0,55984|



Luas ( _Area_ ) merupakan banyak piksel yang menyusun suatu objek Pada citra biner dilakukan operasi _thresholding_ untuk mempresentasikan luasanadari objek, Luas objekakemudian dihitung denganacara menjumlahkanaseluruh angka 1 (piksel berwarna putih) pada citraabiner yang diperoleh. Luasaobjek dihitungadalam satuanapiksel. 

Keliling ( _Perimeter_ ) merupakanabanyak piksel yang beradaapada boundary objek. Operasi morfologiadilakukan untuk mendapatkan boundariesadari citra biner. Kemudianadilakukan penghitungan keliling objek dengan cara 

44 

menjumlahkanaseluruh angkaa1 (piksel berwarna putih) padaacitra biner yang diperoleh. Kelilingaobjek dihitung dalam satuanapiksel. 

_Eccentricity_ merupakan nilaiaperbandingan antara jaraka _focil ellips minor_ 

dengana _focil ellips mayora_ suatu objek. 

**==> picture [213 x 98] intentionally omitted <==**

Gambar 3. 17 Rumus _Eccentricity_ 

_Metric_ merupakan nilaiaperbandingan antaraaluas dan keliling. 

**==> picture [218 x 116] intentionally omitted <==**

Gambar 3. 18 Rumus _Metric_ 

## **3.1.4. Klasifikasia** _**k-Nearest Neighbora**_ 

Pada tahap ini delakukan klasifikasi tipe bangunan dengan menggunakan _k_ 

_Nearest Neighbor,_ data _training_ dibagi menjadi 3 kelas bangunan yaitu tipe A 

(bangunan Besar), tipe B (bangunan sedang) dan tipe C (bangunan kecil) _._ 

45 

Tabel 3. 2 Contoh Data Training Tipe Bangunan 

**==> picture [386 x 448] intentionally omitted <==**

**----- Start of picture text -----**<br>
Bangunan Tipe A=1<br>(Besar)<br>Bangunan Tipe B=2<br>(Sedang)<br>Bangunnan Tipe C=3<br>(Kecil)<br>**----- End of picture text -----**<br>


Data training diambil dari citra satelit _Google Earth_ , Setelah objek 

(bangunan) terdeteksi selanjut pengklasifikasian tipe bangunan menggunakan ciri 

objek yaitu: Luas dan Keliling. Klasifikasi tipe bangunan dengan _k-Nearest Neighbor_ pada penelitian ini mengguanakan perhitungan jarak _Euclidean Distance._ 

46 

## **3.1.4.1. Flowchart Algoritma** _**k-Nearest Neighbor**_ 

**==> picture [193 x 367] intentionally omitted <==**

Gambar 3. 19 Flowchat Algoritma _k-NN_ 

Menentukan _k_ tetangga terdekat adalah tahap pertama dalam klasifikasi _k-_ 

_Nearest Neighbor_ dalah menentukan parameter _k_ tetatngga terdekat, misanyal k=3, 

berarti mencari jarak terdekat data uji terhadap 3 tetangga terdekat dari data trainingnya. 

47 

Tabel 3. 3 Sampel Data Latih Bangunan 

Sampel Data latih Objek Bangunan Hasil deteksi dan Ekstraksi Ciri 

**==> picture [228 x 131] intentionally omitted <==**

Bangunan Tipe (A) 

**==> picture [234 x 141] intentionally omitted <==**

Bangunan Tipe (B) Bangunan Tipe (C) 

48 

_Sample_ data latih adalah objek bangunan hasil deteksi citra satelit _Google Earth (rgb)_ yang telah dikonversikan kedalam ruang warna biner untuk diektraksi ciri tipe objeknya dan kemudian dikelompokkan berdasarkan kesamaan cirinya. 

Tabel 3. 4 Sampel Data Training Tipe Bangunan 

|Tabel 3. 4 Sampel Data Training Tipe Bangunan|Tabel 3. 4 Sampel Data Training Tipe Bangunan|Tabel 3. 4 Sampel Data Training Tipe Bangunan|Tabel 3. 4 Sampel Data Training Tipe Bangunan|Tabel 3. 4 Sampel Data Training Tipe Bangunan|Tabel 3. 4 Sampel Data Training Tipe Bangunan|Tabel 3. 4 Sampel Data Training Tipe Bangunan|
|---|---|---|---|---|---|---|
||||||||
||||Data Training||||
|No.|Luas|Keliling|Metric|Eccentricity|Tipe|Kategori|
|1|8333|610,68|0,28|0,97|1|A|
|2|8786|603,69|0,30|0,97|1|A|
|3|7802|527,18|0,35|0,96|1|A|
|4|7855|519,91|0,37|0,96|1|A|
|5|8923|589,08|0,32|0,97|1|A|
|6|3104|264,79|0,56|0,69|2|B|
|7|3231|239,48|0,71|0,65|2|B|
|8|3196|238,51|0,71|0,77|2|B|
|9|3306|301,89|0,46|0,73|2|B|
|10|2940|253,61|0,57|0,80|2|B|
|11|1687|180,65|0,65|0,77|3|C|
|12|2157|209,28|0,62|0,61|3|C|
|13|2000|211,62|0,56|0,68|3|C|
|14|1834|193,54|0,62|0,68|3|C|
|15|1802|193,76|0,60|0,51|3|C|
||||Data Uji||||
|1|2889|311,06|0,38|0,47|?|?|



Data _training_ diambil dari hasil ekstraksi ciri objek detetksi yaitu ciri Luas, Keliling, _Eccentricity_ dan _Metric_ nya kemudian dikelompokkan mejadi 3 kelompok tipe data bangunan berdasarkan cirinya. Data _training_ ini akan menjadi acuan data uji untuk diklasifikasikan berdasarkan jarak terdekatnya. Data uji adalah data baru yang belum masuk kedalam kelompok, data uji diambil dari salah satu hasil deteksi kemudian diektraksi cirinya untuk diuji dan diklasifikasi. 

49 

Dari hasil deteksi bangun dari citra _Satelit Google Earth,_ setelah objek bangunan dideteksi maka selanjutnya adalah mengklasifikasikannya kedalam salah satu dari 3 tipe bangunan dengan mencari kecocokan cirinya dengan perhitungan _Euclidean distance_ terhadap _k_ mayoritas tetangga tertdekat. 

## **3.1.4.2. Menghitung** _**Euclidean Distance**_ 

Tabel 3. 5 Tabel Pehitungan _Euclidean Distance_ 

|||Tabel 3. 5 Tabel Pehitungan_Euclidean Distance_|
|---|---|---|
|No.||Euclidean Distance|
|1|√(8333 −2889)2 +(610,68 −311,06)2 +(0,28 −0,38)2 +(0,97 −0,47)2||
|2|√(8786 −2889)2 +(603,69 −311,06)2 +(0,30 −0,38)2 +(0,97 −0,47)2||
|3|√(7802 −2889)2 +(527,18 −311,06)2 +(0,35 −0,38)2 +(0,96 −0,47)2||
|4|√(7855 −2889)2 +(519,91 −311,06)2 +(0,37 −0,38)2 +(0,96 −0,47)2||
|5|√(8923 −2889)2 +(589,08 −311,06)2 +(0,32 −0,38)2 +(0,97 −0,47)2||
|6|√(3104 −2889)2 +(264,79 −311,06)2 +(0,56 −0,38)2 +(0,69 −0,47)2||
|7|√(3231 −2889)2 +(239,48 −311,06)2 +(0,71 −0,38)2 +(0,65 −0,47)2||
|8|√(3196 −2889)2 +(238,51 −311,06)2 +(0,71 −0,38)2 +(0,77 −0,47)2||
|9|√(3306 −2889)2 +(301,89 −311,06)2 +(0,46 −0,38)2 +(0,73 −0,47)2||
|10|√(2940 −2889)2 +(253,61 −311,06)2 +(0,57 −0,38)2 +(0,80 −0,47)2||
|11|√(1687 −2889)2 +(180,65 −311,06)2 +(0,65 −0,38)2 +(0,77 −0,47)2||
|12|√(2157 −2889)2 +(209,28 −311,06)2 +(0,62 −0,38)2 +(0,61 −0,47)2||
|13|√(2000 −2889)2 +(211,62 −311,06)2 +(0,56 −0,38)2 +(0,68 −0,47)2||
|14|√(1834 −2889)2 +(193,54 −311,06)2 +(0,62 −0,38)2 +(0,68 −0,47)2||
|15|√(1802 −2889)2 +(193,76 −311,06)2 +(0,60 −0,38)2 +(0,51 −0,47)2||



Tabel perhitungan jarak pada table 3.5 menggunakan rumus perhitungan jarak _Euclidean Distance_ : 

**==> picture [137 x 54] intentionally omitted <==**

**----- Start of picture text -----**<br>
𝑛<br>𝑖 −𝑦𝑖) [2] )<br>𝑖=1<br>𝑑(𝑥, 𝑦) = √(∑(𝑥<br>**----- End of picture text -----**<br>


Dimana: 

**•** d𝑥𝑖= sampel data **•** 𝑦𝑖 = data uji **•** 𝑖 = variable data **•** 𝑑 = jarak **•** 𝑛 = dimensi data 

50 

Tabel 3. 6 Hasil Perhitngan _Euclidean Distance_ 

|No.|Rangking|_Euclidean Dinstance_|Tipe|
|---|---|---|---|
|1|13|5452,24|A|
|2|14|5904,26|A|
|3|11|4917,75|A|
|4|12|4970,39|A|
|5|15|6040,40|A|
|6|2|219,92|B|
|7|4|349,41|B|
|8|3|315,46|B|
|9|5|417,10|B|
|10|1|76,83|B|
|11|10|1209,05|C|
|12|6|739,04|C|
|13|7|894,54|C|
|14|8|1061,53|C|
|15|9|1093,31|C|



Tabel hasil perhitungan _Euclidean Distance_ didapatkan dari hasil perhitungan jarak dari data uji terhadap data _training_ . 

## **3.1.4.3. Klasifikasi Data** 

Setelah hasil perhitungan jarak _Euclidean_ didapatkan maka selanjuntanya mengurutkan jarak terdekat data uji terhadap data _training_ berdasarkan mayoritas nilai _**k**_ kemudian mengelompokkanya kedalam tipe data bangunan. 

Hasil pengujian data uji terhadap data _training_ dengan nilai _k_ =3, 5, 7 dan 9. 

Tabel 3. 7 _k_ =3 

||Tabel 3. 7_k_=3||
|---|---|---|
|Ranking|_Euclidean distance_|Tipe|
|1|76,83|B|
|2|219,92|B|
|3|315,46|B|



51 

Berdasarkan hasil uji dengan _k=3,_ mayoritas jarak terpendek terhadap label 

_k_ adalah kategori _B_ maka data uji masuk kedalam kelompok data Tipe B berdasarkan _Euclidean Distance_ . 

Tabel 3. 8 _k=_ 5 

||Tabel 3. 8_k=_5||
|---|---|---|
|Ranking|Euclidean Distance|Tipe|
|1|76,83|B|
|2|219,92|B|
|3|315,46|B|
|4|349,41|B|
|5|417,10|B|



Berdasarkan hasil uji dengan _k=5,_ mayoritas jarak terpendek terhadap label 

_k_ adalah kategori B, maka data uji termaksuk dalam kelompok Tipe B berdasarkan _Euclidean Distance_ . 

Tabel 3. 9 _k=_ 7 

||Tabel 3. 9_k=_7||
|---|---|---|
|Ranking|_Euclidean Distance_|Tipe|
|1|76,83|B|
|2|219,92|B|
|3|315,46|B|
|4|349,41|B|
|5|417,10|B|
|6|739,04|C|
|7|894,54|C|



Berdasarkan hasil uji dengan _k=7_ , mayoritas jarak terpendek terhadap 

label _k_ adalah kategori B, maka data uji termaksuk dalam kelompok Tipe B 

berdasarkan _Euclidean Distance_ . 

52 

Tabel 3. 10 _k=9_ 

||Tabel 3. 10_k=9_||
|---|---|---|
|Ranking|_Euclidean Distance_|Tipe|
|1|76,83|B|
|2|219,92|B|
|3|315,46|B|
|4|349,41|B|
|5|417,10|B|
|6|739,04|C|
|7|894,54|C|
|8|1061,53|C|
|9|1093,31|C|



Berdasarkan hasil uji dengan _k=9_ , mayoritas jarak terpendek terhadap label 

_k_ adalah kategori B, maka data uji termaksuk dalam kelompok Tipe B berdasarkan _Euclidean Distance_ . 

Jadi berdasarkan nilai _k=3, k=5, k=7, dan k=9_ menunjukakn mayoritas jarak terpendek terhadap tipe data B, maka dapat disimpulkan data uji termasuk kedalam kelompok bangunan Tipe B. 

## **3.1.5. Perhitungan Akurasi** 

_Confusion matric_ adalah suatu metode yang digunakan untuk melakukan perhitungan akurasi pada konsep data mining. Evaluasi dengan _confusion matrix_ menghasilkan nilai akurasi, presisi dan _recall_ . Akurasi dalam klasifikasi adalah persentase ketepatan record data yang diklasifikasikan secara benar setelah dilakukan pengujian pada hasil klasifikasi (Han & Kamber, 2006). Presisi atau 

_confidence_ adalah proporsi kasus yang diprediksi positif yang juga positif benar pada data yang sebenarnya. Recall atau _sensitivity_ adalah proporsi kasus positif yang sebenarnya yang diprediksi positif secara benar (Powers, 2011). 

53 

**==> picture [398 x 169] intentionally omitted <==**

**----- Start of picture text -----**<br>
Tabel 3. 11  Confusion Matric Model<br>Nilai Sebenarnya<br>True  False<br>TP  FP<br>True  (True Positive)  (False Positive)<br>Correct result  Unexpected Result<br>Nilai<br>Prediksi  TN<br>FN<br>(True Negative)<br>False  (False Negative)<br>Correct absence of<br>Missing Result<br>result<br>**----- End of picture text -----**<br>


Rumus untuk menghitung Akurasi, presisi dan _recall_ pada _confusion matrix_ adalah sebagai berikut (Gorunescu, 2011) : 𝑇𝑃 _Prescision_ = × 100% 𝑇𝑃+𝐹𝑃 Presisi adalah tingkat ketepatan antara informasi yang diminta oleh pengguna dengan jawaban yang diberikan oleh sistem 𝑇𝑃+𝑇𝑁 _Akurasi_ = × 100% 𝑇𝑃+𝑇𝑃+𝐹𝑃+𝐹𝑁 _Accuracy_ didifinisikan sebagai tingkat kedekatan antara nilai prediksi dengan nilai aktual. 𝑇𝑃+𝑇𝑁 _Recall_ = × 100% 𝑇𝑃+𝐹𝑁 

_Recall_ adalah tingkat keberhasilan sistem dalam menemukan kembali 

sebuah informasi. 

## **BAB IV** 

## **UJICOBA DAN PEMBAHASAN** 

Pada Bab ini akan dijelaskan rangkaian uji coba dan pembahasan dari hasil penelitian yang telah dilakukan. Uji coba dilakukan untuk melihat sejauh mana keberhasilan metode yang diterapkan, sedangkan pembahasan dilakukan dengan melakukan analisa hasil uji coba agar memperoleh kesimpulan dan saran untuk penelitian selanjutnya. **4.1. Implementasi** Lingkungan implementasi deteksi dan klasifikasi bangunan pada citra satelit menggunakan _k- Nearest Neigbor_ terbagi menjadi lingkungan _hardware_ dan lingkungan _software_ . 

## **4.1.1. Software** 

Perangkat lunak atau _software_ yang digunakan untuk pembuatan dan pengujian sistem sebagai berikut: 

a) Sistem Operasi _Windows_ 10 64 bit b) Bahasa Pemrograman MATLAB (R2015a) c) Program Citra Satelit _Google Earth_ 

## **4.1.2. Hardware** 

Perangakat keras atau _hardware_ yang digunakan untuk pembuatan dan pengujian sistem adalah sebagai berikut: 

a) _Processor_ : _Intel(R) Core(TM)_ i3-3110M b) _Memory_ : RAM DDR3 6,00 GB c) _Harddisk_ : 500 GB 

54 

55 

## **4.2. Uji Coba Deteksi Bangunan** 

Pada proses pengujian deteksi bangunan ini digunakan metode segmentasi 

warna untuk mendeteksi objek bangunan pada citra satelit. 

**==> picture [372 x 104] intentionally omitted <==**

Gambar 4. 1 Blok Deteksi Bangunan 

Langkah langkah uji coba deteksi bangunan sebagai berikut: 

a) Input citra satelit: citra satelit diambil dari _google earth_ kemudian dilakukan _crooping_ dan diinputkan kedalam sistem. 

b) Segmentasi warna: citra satelit _RGB_ dikonversikan kedalam warna _CIE LAB_ , kemudian _CIE LAB_ dibagi menjadi beberapa kluster. Setipa kluster dianalisa untuk mencari kluster target (kluster bangunan). 

- c) Konversi Biner: Setelah kluster bangunan ditemukan maka dilakukan konversi ke biner dan dilakukan perbaikan kualitas citra. 

- d) Perhitungan Jumlah Bangunan: Objek yang terdeteksi dilabeling kemudian dihitung jumlah objek bangunan. 

## **4.2.1. Citra Hasil Segmentasi** 

Segmentasi citra dilakukan setelah citra uji (citra bangunan _RGB_ ) dinputkan 

ke dalam sistem, kemudian citra RGB akan dikonversikan kedalam _CIE LAB_ , warna _CIE LAB_ akan dibagi menjadi beberapa cluster warna. Pada setiap cluster akan diidentifikasi objek bangunan. Setelah objek bangunan ditemukan, cluster 

56 

bangunan akan dikonversikan ke dalam ruang warna biner dan dilakukan perbaikan hasil deteksi selanjutnya melakukan labeling objek untuk menghitung jumlah objek 

bangunan terdeteksi. 

Tabel 4. 1 Hasil Segmentasi Citra 

**==> picture [398 x 535] intentionally omitted <==**

**----- Start of picture text -----**<br>
(a)  (b)<br>(c)  (d)<br>(e)  (f)<br>(g)  (h)<br>**----- End of picture text -----**<br>


57 

Pada table hasil segmentasi citra di atas: 

a) Citra satelit _RGB_ yang di inputkan kedalam sistem b) Konversi warna _RGB_ ke _CIE LAB_ c) _Labelling index_ pada _CIE LAB_ 

d) Objek pada _cluster_ 1 e) Objek pada _cluster_ 2 f) Objek pada _cluster_ 3 g) Objek Bangunan yang terdeteksi ( _rgb_ ) h) Citra bangunan Biner setelah mengalami perbaikan hasil deteksi 

## **4.2.2. Citra Hasil Deteksi Bangunan** 

Objek bangunan hasil deteksi dari citra satelit dan akurasi deteksi akan 

ditampilkan pada pembahasan ini. 

Tabel 4. 2 Tabel Hasil Deteksi Bangunan 

|No.|Citra Uji|Hasil Deteksi Bangunan|
|---|---|---|
|1|||
|2|||



58 

**==> picture [398 x 655] intentionally omitted <==**

**----- Start of picture text -----**<br>
3<br>4<br>5<br>6<br>7<br>8<br>**----- End of picture text -----**<br>


59 

**==> picture [398 x 239] intentionally omitted <==**

**----- Start of picture text -----**<br>
9<br>10<br>**----- End of picture text -----**<br>


Pada table 4.1 ditampilkan hasil deteksi bangunan setelah melalui proses segmentasi sehingga objek bangunan dapat dihitung. 

Nilai akurasi dibutuhkan untuk mengetahui seberapa besar ketepatan sistem 

dalam mendeteksi jumlah bangunan. Nilai akurasi dapat dinyatakan dalam satuan 

%. Adapun perhitungan untuk mencari nilai akurasi yaitu: 

(𝑗𝑢𝑚𝑙𝑎ℎ 𝑜𝑏𝑗𝑒𝑘 𝑏𝑛𝑔𝑢𝑛𝑎𝑛+𝑗𝑢𝑚𝑙𝑎ℎ 𝑜𝑏𝑗𝑒𝑘 𝑏𝑢𝑘𝑎𝑛 𝑏𝑎𝑛𝑔𝑢𝑛𝑎𝑛) Akurasi = × 100% 

𝑗𝑢𝑚𝑙𝑎ℎ 𝑡𝑜𝑡𝑎𝑙 𝑜𝑏𝑗𝑒𝑘 

## Tabel 4. 3 Akurasi Deteksi Sistem 

|No.|Objek|Jumlah Real|Jumlah Deteksi|Akurasi(%)|
|---|---|---|---|---|
|1|Gambar 1|70|65|92.8%|
|2|Gambar 2|57|55|96.4%|
|3|Gambar 3|66|57|86.3%|
|4|Gambar 4|10|10|100%|
|5|Gambar 5|137|115|83.9%|
|6|Gambar 6|40|32|80%|
|7<br>|Gambar 7<br>|46<br>|43<br>|93.4%<br>|
|8|Gambar 8|80|66|82.5%|
|9|Gambar9|50|48|96%|
|10|Gambar 10|63|61|96.8%|
|Akurasi rata rata(%)||||90.8%|



60 

Akurasi rata rata sistem dalam mendeteksi banguna adalah 90.8% dengan 

menggunakan _areaopen_ =700 piksel yang berarti menghilangkan citra hasil deteksi 

yang bernilai piksel dibawah 700 piksel, sehingga dianggap sebagai _noise_ kemudian 

dihilangkan. 

## **4.3. Proses Klasifikasi Bangunan** 

Pada proses klasifikasi bangunan ini objek terdeteksi akan diklasifikasikan 

berdasarkan nilai ektraksi cirinya ukurannya yaitu nilai Luas, Keliling, dengan cara 

mengukur jarak data uji dengan data latih. 

**==> picture [398 x 271] intentionally omitted <==**

Gambar 4. 2 Diagram Blok Klasifikasi sistem 

Pada diagram blok diatas akan dijelaskan proses klasifikasi bangun pada 

sistem sebagai berikut: 

- Data latih citra bangunan merupakan data yang di _crooping_ dari 

_Google Earth_ kemudian disimpan dalam format _.jpg_ . 

61 

- Ekstraksi ciri bangunan merupakan proses mendapatkan ciri bangunan setelah dilakukan proses segmentasi gambar. 

- Simpan nilai _.xls_ adalah proses penyimpanan nilai ciri ekstraksi objek kedalam format _.xls_ yang akan digunakan sebagai nilai referensi dan akan digunakan untuk pencocokan nilai dari data testing. 

- Data _testing_ adalah data baru hasil ektraksi sistmem yang akan diuji kecocokannya dengan data _training_ . 

- Pencocokan ciri adalah proses perhitungan jarak terdekat ( _Euclidean distance_ ) data _testing_ dengan data _training_ untuk mencari nilai jarak terkecil dan pengklasifikasian menggunakan metode _k Nerest Neighbor_ berdasarkan mayoritas jumlah tetangga terdekanya. 

## **4.3.1. Ektraksi Ciri Objek Deteksi** 

Pada tahap ini akan dilakukan ekstraksi ciri pada objek yang terdeteksi. Ciri 

yang dideteksi yaitu nilai Luas, Keliling, _Metric_ , dan _Eccentricity_ . 

**==> picture [349 x 184] intentionally omitted <==**

Gambar 4. 3  Gambar Uji 

62 

Pada gambar 4.3 objek akan diekstraksi cirinya setelah di konversikan ke warna biner dan hasil ektraksi akan di tampilkan pada table hasil ektraksi ciri. 

Tabel 4. 4 Tabel Hasil Ekstraksi Ciri 

|Objek|Luas|Keliling|Meric|Eccentricity|
|---|---|---|---|---|
|1|10667|676,4163|0,293|0,9711|
|2|9576|591,8061|0,3436|0,9606|
|3|9606|588,1909|0,3489|0,9601|
|4|10174|677,4041|0,2786|0,9751|
|5|10801|657,0782|0,3144|0,9722|
|6|9260|607,1198|0,3157|0,9661|
|7|9539|622,333|0,3095|0,9637|
|8|5805|386,7696|0,4876|0,9703|
|9|2170|218,2082|0,5727|0,8221|
|10|3826|322,0244|0,4636|0,9652|



Pada table hasil ekstraksi terdapat 10 objek yang terdeteksi nilai Luas objek, 

nilai Keliling objek, nilai _Metric_ objek dan nilai _Eccentricity_ objek. Nilai ekstraksi ciri yang terdeteksi akan digunakan sebagai nilai uji untuk pengklasifikasian objek terhadap data latih menggunakan metode _k Nearest Neighbor_ . 

## **4.3.2. Uji Coba Akurasi Klasifikasi KNN** 

Pada tahan ini akan dilakukan beberapa tahap untuk menguji akurasi klasifikasi _k Nearest Neighbor_ dalam mengklasifikasikan objek bangunan hasil deteksi dan ektraksi ciri. Pengujian ini akan dilakukan dengan beberapa skenario 

pengujian. 

## **4.3.2.1. Dataset Uji Coba Klasifikasi KNN** 

Data yang digunakan dalam pengujian ini menggunakan dataset 3 kategori 

tipe bangunan hasil deteksi dan ektraksi ciri yaitu tipe A, B dan C sebanyak 150 

data dan telah dikategorikan berdasarkan ciri ukuran luas dan kelilingnya: 

63 

Tabel 4. 5 Tipe Bangunan A 

|Objek|Luas|Keliling|Metric|Eccentricity|Kategori|Tipe|
|---|---|---|---|---|---|---|
|1|5989|330,2914|0,6899|0,6391|1|A|
|2|5430|334,8356|0,6086|0,9163|1|A|
|3|6162|342,5757|0,6598|0,5436|1|A|
|4|5913|353,3625|0,5951|0,8293|1|A|
|5|5565|318,8772|0,6877|0,8577|1|A|
|…|…|…|…|…|…|…|
|50|12549|460,7767|0,7427|0,7013|1|A|



Ciri bangunan tipe A dikategorikan dengan angka 1 sebanyak 50 objek bangunan. 

|||Tabel 4. 6 Tipe Bangunan B|Tabel 4. 6 Tipe Bangunan B|Tabel 4. 6 Tipe Bangunan B|||
|---|---|---|---|---|---|---|
|Objek|Luas|Keliling|Metric|Eccentricity|Kategori|Tipe|
|1|3922|280,0071|0,6286|0,8878|2|B|
|2|3021|230,0244|0,7175|0,782|2|B|
|3|3429|295,7473|0,4926|0,9315|2|B|
|4|3910|273,6224|0,6563|0,8558|2|B|
|5|3836|270,5513|0,6586|0,8584|2|B|
|…|…|…|…|…|…|…|
|50|3773|296,0904|0,5408|0,9176|2|B|



Ciri bangunan tipe B dikategorikan dengan angka 2 sebanyak 50 objek bangunan. 

Tabel 4. 7 Tipe Bangunan C 

|Objek<br>1<br>2<br>3<br>4<br>5<br>…<br>50|Luas|Keliling|Metric|Eccentricity|Kategori|Tipe|
|---|---|---|---|---|---|---|
||2315|208,7523|0,6676|0,509|3|C|
||1537|153,0955|0,8241|0,6472|3|C|
||2315|232,2914|0,5391|0,5007|3|C|
||2162|223,664|0,5431|0,9543|3|C|
||2501|251,0193|0,4988|0,6273|3|C|
||…|…|…|…|…|…|
||1854|214,3087|0,5073|0,6873|3|C|



64 

Ciri bangunan tipe C dikategorikan dengan angka 3 sebanyak 50 objek bangunan. Berdsarkan data setiap dataset diatas menunjukkan informasi ciri dari 3 kategori bangunan yang terdeteksi yaitu luas, keliling, _eccentricity_ dan _matric_ . 

**4.3.2.2. Skenario Pengujian 1** Tahap pertama dalam pengujian ini adalah proses klasifikasi dimana data uji bangunan hasil deteksi dan ektraksi ciri yaitu luas dan keliling digunakan untuk mengklasifikasikan tipe bangunan dengan berdasarkan jarak terdekatnya terhadap data latihnya dengan menggunakan metode _k Nearest Neighbor_ . Pada pengujian ini akan mencari nilai _k_ (nilai tertangga terdekat) terbaik untuk klasifikasi _k Nearest Neighbor_ , proses pengujian dilakukan dengan menguji dataset bangunan sebanyak 150 tipe bangunan hasil ektraksi yang telah dikategorikan berdasarkan ciri ukuran luas dan kelilingnya. Pengujian ini dilakukan dengan membagi dataset menjadi 2 bagian dengan perbandinngan (80:20) yaitu 120 data tipe banguna sebagai data latih dan 30 data tipe bangunan sebagai data uji yang diambil secara acak dari dataset. Klasifikasi tipe bangunan ini menggunakan fungsi _fitcknn_ untuk mencari kesamaan karakteristik tipe bangunan berdasarkan jarak terdekat menggunakan perhitungan jarak _Euclidean Distance_ . 

65 

Tabel 4. 8 Hasil Klasifikasi Knn 

||Data Uji|Data Uji|Target Klasifikasi|Target Klasifikasi||Pengujian dengan k-n|Pengujian dengan k-n|Pengujian dengan k-n||
|---|---|---|---|---|---|---|---|---|---|
|Objek|Luas|Keliling|Kategori|Tipe|_k_=3|_k_=5|_k=7_|_k_=9|_k=11_|
|1|5989|330,2914|1|A|1|1|1|1|1|
|2|5430|334,8356|1|A|1|1|1|1|1|
|3|6162|342,5757|1|A|1|1|1|1|1|
|4|5913|353,3625|1|A|1|1|1|1|1|
|5|5565|318,8772|1|A|1|1|1|1|1|
|6|5123|302,1493|1|A|1|1|1|1|1|
|7|8503|599,3036|1|A|1|1|1|1|1|
|8|5795|374,2325|1|A|1|1|1|1|1|
|9|7723|524,2498|1|A|1|1|1|1|1|
|10|7739|525,7056|1|A|1|1|1|1|1|
|11|3558|250,2082|2|B|2|2|2|2|2|
|12|3369|232,4924|2|B|2|2|2|2|2|
|13|3656|255,2792|2|B|2|2|2|2|2|
|14|2680|205,4386|2|B|3|3|3|3|3|
|15|2846|218,1665|2|B|2|2|2|2|2|
|16|3218|249,7645|2|B|2|2|2|2|2|
|17|2348|199,6812|2|B|3|3|3|3|3|
|18|2435|223,9239|2|B|2|2|3|3|3|
|19|4165|259,664|2|B|2|2|2|2|2|
|20|4223|289,1371|2|B|2|2|2|2|2|
|21|2315|208,7523|3|C|3|3|3|3|3|
|22|1537|153,0955|3|C|3|3|3|3|3|
|23|2315|232,2914|3|C|2|3|3|3|3|
|24|2162|223,664|3|C|3|3|3|3|3|
|25|2501|251,0193|3|C|3|3|3|2|2|
|26|2242|243,1198|3|C|3|3|3|3|3|
|27|1838|183,3381|3|C|3|3|3|3|3|
|28|1888|201,7645|3|C|3|3|3|3|3|
|29|1989|201,3209|3|C|3|3|3|3|3|
|30|1767|174,1249|3|C|3|3|3|3|3|



Pada table hasil pengujian diatas didapatkan hasil klasifiksi menggunakan 

_k_ =3, _k=_ 5, _k=_ 7, _k_ =9, dan _k=_ 11. Selanjutnya menghitung _accuracy_ dari masing masing hasil klasifikasi dengan _confussion matrix_ . 

66 

Tabel 4. 9 Rumus _Confussion Matrix_ 

|||Kenyataan|Kenyataan|
|---|---|---|---|
|||_true_|_false_|
|Hasil Prediksi|_true_|TP|FP|
||_false_|FN|TN|



𝑇𝑃+𝑇𝑁 _Accuracy_ = × 100% 𝑇𝑃+𝑇𝑃+𝐹𝑃+𝐹𝑁 

Tabel 4. 10 _Confussion matrix k_ =3 

|Hasil prediksi||Kenyataan|Kenyataan|
|---|---|---|---|
||Tipe A|Tipe B|Tipe C|
|Tipe A|10|0|0|
|Tipe B|0|8|2|
|Tipe C|0|1|9|



Pada pengujian _k=3_ terdpat 3 objek miss klasifikasi yaitu 2 objek tipe B 

yang di klasifikasikan ke tipe C dan 1 objek tipe C yang diklasifikasikan ke tipe B. 

Tabel 4. 11 _Confussion Matrix k_ =5 

|Hasil prediksi||Kenyataan|Kenyataan|
|---|---|---|---|
||Tipe A|Tipe B|Tipe C|
|Tipe A|10|0|0|
|Tipe B|0|8|2|
|Tipe C|0|0|10|



Pada pengujian _k_ =5 terdapat 2 objek misklasifikasi yaitu 2 objek tipe B yang diklasifikasikan ke tipe C. 

67 

Tabel 4. 12 _Confussion Matrix k_ =7 

|Hasil prediksi||Kenyataan|Kenyataan|
|---|---|---|---|
||Tipe A|Tipe B|Tipe C|
|Tipe A|10|0|0|
|Tipe B|0|7|3|
|Tipe C|0|0|10|



Pada pengujian _k_ =7 terdapat 3 objek misklasifikasi yaitu 3 objek Tipe B yang diklasifikasikan ke Tipe C. 

Tabel 4. 13 _Confussion Matrix k=_ 9 

|Hasil prediksi||Kenyataan|Kenyataan|
|---|---|---|---|
||Tipe A|Tipe B|Tipe C|
|Tipe A|10|0|0|
|Tipe B|0|7|3|
|Tipe C|0|1|9|



Pada pengujian _k_ =9 terdapat 4 objek misklasifikasi yaitu 3 objek tipe B yang 

diklasifikasikan ke Tipe C dan 1 objek tipe C yang diklsifikasikan ke Tipe B. 

Tabel 4. 14 _Confussion Matrix k=_ 11 

|Hasil prediksi||Kenyataan|Kenyataan|
|---|---|---|---|
||Tipe A|Tipe B|Tipe C|
|Tipe A|10|0|0|
|Tipe B|0|7|3|
|Tipe C|0|1|9|



Pada pengujian _k_ =11 terdapat 4 objek misklasifikasi yaitu 3 objek tipe B 

yang diklasifikasikan ke Tipe C dan 1 objek tipe C yang diklsifikasikan ke Tipe B. 

68 

Tabel 4. 15 Akurasi Hasil Klasifikasi _k_ 

|Tabel 4. 15 Akurasi|Hasil Klasifikasi_k_|
|---|---|
|Hasil Uji_k_|Akurasi|
|_k=_3|90%|
|_k=_5|93%|
|_k=_7|90%|
|_k=_9|86%|
|_k=_11|86%|
|Rata rata akurasi|89%|



Hasil akurasi terbaik dari pengujian klasifikasi _k Nearest Neighbor_ adalah 93% menggunakan _k=_ 5. Maka klasifikasi pada sistem akan menggunakan _k=_ 5 untuk _k_ tetangga terdekanya. 

## **4.3.2.3. Skenario Pengujian 2:** 

Pada tahap pengujian kedua ini akan menguji keakuratan model klasifikasi 

_kNN_ dengan menggunakan _k-fold cross validation_ . _Cross validation_ merupakan metode untuk memvalidasi keakuratan sebuah model yang dibangun berdasarkan dataset tertentu. _K Fold Cross Validation_ mengulang _k-kali_ untuk membagi sebuah himpunan contoh secara acak menjadi _k_ subset yang saling bebas, setiap ulangan disisikan satu subset untuk pengujian dan subset lainnya untuk pelatihan (Fu, 1994). 

_Cross model_ yang dibuat pada matlab: 

```
classreg.learning.partition.ClassificationPartitionedModel
CrossValidatedModel: 'KNN'
PredictorNames: {'x1'  'x2'}
ResponseName: 'Y'
NumObservations: 150
KFold: 5
Partition: [1x1 cvpartition]
ClassNames: [1 2 3]
ScoreTransform: 'none'
```

Cross model akan memvalidasi model klasifikasi _kNN_ dengan 

_PredictorNames_ yaitu kolom x1= Luas dan x2= Keliling dan akan merespon Y= 

69 

kategori bangunan yaitu kategori tipe A, B dan C dengan _Class names_ [1 2 3]. Dataset yang diobservasi sebanyak 150 data tipe bangunan, dengan melakukan 

_kfold =_ 5 atau 5 kali tahap pengujian. 

_Cross model partition_ pada matlab: 

```
K-fold cross validation partition
NumObservations: 150
NumTestSets: 5
TrainSize: 120  120  120  120  120
TestSize: 30  30  30  30  30
```

Selanjutnya membuat partisi pengujian _k-fold =_ 5, yaitu dataset sebanyak 150 data tipe bangunan dibagi menjadi 5 bagian _trainingset_ dengan setiap bagian _trainsize_ 120 data , dan 5 bagian _testset_ dengan setiap bagian _testsize_ 30 data. 

Tabel 4. 16 Pengujian _k-fold_ =5 

||Semua Data|Semua Data|Semua Data|Semua Data|Semua Data||
|---|---|---|---|---|---|---|
||Trainingdata|||||Test data|
||Fold1|Fold 2|Fold 3|Fold 4|Fold 5|} mencari parameter|
|Split 1|Fold 1|Fold 2|Fold 3|Fold 4|Fold 5||
|Split 2|Fold 1|Fold 2|Fold 3|Fold 4|Fold 5||
|Split 3|Fold 1|Fold 2|Fold 3|Fold 4|Fold 5||
|Split 4|Fold 1|Fold 2|Fold 3|Fold 3|Fold 5||
|Split 5|Fold 1|Fold 2|Fold 3|Fold 4|Fold 5||
||evaluasi akhir|||||{test data|



Pada tabel diatas dilakukan 5 kali tahap pengujian untuk mencari hasil kalsifikasi dari _kNN_ dengan menggunakan _k Fold Cross Validation._ 

Tabel 4. 17 Test _fold_ 1 

|Ta|bel 4. 17 Te|st_fold_1|st_fold_1|
|---|---|---|---|
|Hasil prediksi<br>||Kenyataan||
||Tipe A<br>|Tipe B<br>|Tipe C<br>|
|Tipe A|10|0|0|
|Tipe B|0|8|0|
|Tipe C|0|0|12|



70 

Pada pengujian _fold_ 1, 30 kategori bangunan diklasifikasikan dengan benar, yaitu 10 tipe A, 8 tipe B dan 12 tipe C. 

Tabel 4. 18 Test _fold_ 2 

|Ta|bel 4. 18 Te|st_fold_2|st_fold_2|
|---|---|---|---|
|Hasil prediksi||Kenyataan||
||Tipe A|Tipe B|Tipe C|
|Tipe A|11|0|0|
|Tipe B|0|6|1|
|Tipe C|0|2|10|



Pada pengujian _fold_ 2, 27 bangunan dikategorikan dengan benar dan terdapat 3 misklasifikasi yaitu satu 1 bangunan tipe B diklasifikasi tipe C dan 2 tipe 

C diklasifikasi tipe B. 

Tabel 4. 19 Test _fold_ 3 

|Ta|bel 4. 19 Te|st_fold_3|st_fold_3|
|---|---|---|---|
|Hasil prediksi||Kenyataan||
||Tipe A|Tipe B|Tipe C|
|TipeA|10|0|0|
|Tipe B|0|12|1|
|Tipe C|0|0|7|



Pada pengujian _fold_ 3, 29 bangunan dikategorikan dengan benar dan 1 

bangunan misklasifikasi yaitu 1 bangunan tipe B yang di klasifikasikan ke tipe C. 

Tabel 4. 20 Test _fold_ 4 

|Ta|bel 4. 20 Te|st_fold_4|st_fold_4|
|---|---|---|---|
|Hasil prediksi||Kenyataan||
||Tipe A|Tipe B|Tipe C|
|Tipe A|6|2|0|
|Tipe B|0|11|1|
|Tipe C|0|0|10|



71 

Pada pengujian _fold_ 4, 27 bangunan dikategorikan dengan benar dan 3 bangunan misklasifikasi yaitu 2 bangunan tipe A diklasifikasikan tipeB dan bangunan 1 tipe B yang di klasifikasikan ke tipe C. 

Tabel 4. 21 Test _fold_ 5 

|Ta|bel 4. 21 T|est_fold_5|est_fold_5|
|---|---|---|---|
|Hasil prediksi||Kenyataan||
||Tipe A|Tipe B|Tipe C|
|Tipe A|11|0|0|
|Tipe B|0|9|1|
|Tipe C|0|1|8|



Pada pengujian _fold_ 5, 28 bangunan dikategorikan dengan benar dan 2 

bangunan misklasifikasi yaitu 1 bangunan tipe B yang di klasifikasikan  tipe C dan 1 bangunan tipe C diklasifikasikan tipe B. 

Tabel 4. 22 Akurasi _k fold_ 

|T|abel 4. 22 Akurasi_k fold_|abel 4. 22 Akurasi_k fold_||
|---|---|---|---|
|Skenario|Jumlah data||Akurasi|
||Training|Testing||
|_fold_1|120|30|100%|
|_fold_2|120|30|90%|
|_fold_3|120|30|96%|
|_fold_4|120|30|90%|
|_fold_5|120|30|93%|
|Akurasi rata rata|||93%|



Pada table akurasi _k Fold Cross Validation_ dengan _k fold_ = 5 didapatkan 

hasil akurasi rata rata pengujian dari _k-fold_ yaitu 93% ketepatan hasil validasi dari metode _k Nearest Neighbor_ . 

72 

Tabel 4. 23 Perbandingan akurasi _k NN_ dan _k Fold_ 

|Tab|el 4. 23 Perbandingan a|el 4. 23 Perbandingan a|kurasi_k NN_dan_k Fold_|kurasi_k NN_dan_k Fold_|
|---|---|---|---|---|
|No.|Akurasi_k-NN_||Akurasi_k-fold_||
|1|_k=_3|90%|_fold1_|100%|
|2|_k=_5|93%|_fold2_|90%|
|3|_k=_7|90%|_fold3_|96%|
|4|_k=_9|86%|_fold4_|90%|
|5|_k=_11|86%|_fold5_|93%|
|6|rata rata|89%|rata rata|93%|



Pada table di atas menujukkan bahwa akurasi klasifikasi _k Nearest Neighbor_ 

dengan _k_ =5 menujukkan tingakat akurasi paling optimal dalam mengklasifikasikan 

data, dan _k Fold Cross Validation_ menujukkan rata rata 93% ketepatan akurasi dari 

model klasifikasi _k Nearest Neighbor._ 

## **4.3.2.4. Skenario pengujian 3** 

Pada tahap pengujian ketiga ini setelah pengujian akurasi model klasifikasi 

_k Nearest Neighbor_ dengan _k Fold Cross Validation_ dan ditentukan _k_ terbaik hasil 

pengujian yaitu _k=5_ . Maka tahap selanjutnya akan menguji sistem deteksi dan klasifikasi banguna yang telah dibangun pada matlab dengan data baru hasil deteksi bangunan pada citra satelit. 

Sistem klasifikasi bangunan yang dibangun pada matlab menggunkan fungsi _fitcknn_ untuk klasifikasi data. 

Fungsi _knn_ pada matlab menggunkan _syntax_ : 

```
Md1=fitcknn(X,Y,'NumNeighbors',5,'Standardize',1)
Class = predict(Md1,sample);
```

```
ClassificationKNN
     PredictorNames: {'x1'  'x2'}
       ResponseName: 'Y'
         ClassNames: [1 2 3]
     ScoreTransform: 'none'
    NumObservations: 150
           Distance: 'euclidean'
             NumNeighbors: 5
```

73 

**Md1** adalah _classifier kNN_ yang terlatih, dan beberapa propertinya muncul di _Command Window_ . Md1, dikembalikan sebagai objek model _Clasification kNN_ . **Md1** _= fitcknn_ (X, Y), mengembalikan model klasifikasi _k- Nearest Neighbor_ berdasarkan data predictor **X** dan respon **Y** . **X** adalah matrik numerik yang berisi dua pengukuran kelompok 137 data bangunan. **X** _**-** Predictor data (numeric matric)_ setiap baris sesuai dengan satu pengamatan juga dikenal sebagai _instance_ atau contoh dan setiap kolom sesuai dengan satu variable predictor juga dikenal sebagai fitur. Panjang **Y** dan jumlah baris **X** harus sama. 

**Y** adalah array sel vertor yang berisi kategori bangunan. **Y** _- Class Label_ , label kelas ditentukan sebagai _categorical array, character array, string array, logical vector, numeric vector_ atau _cell array of character vector_ . Setiap baris **Y** mewakili klasifikasi baris _x_ yang sesuai. Selanjutnya menampiklan jarak terdekat hasil klasifikasi data uji dengan data latih menggunkan fungsi _knnsearch_ , _Syntax_ : `Idx = knnsearch(X,Y)` **Idx** = _knnsearch_ (X, Y) menemukan tetangga terdekat di X untuk setiap titik permintaan di Y dan mengembalikan indeks tetangga di Idx vektor kolom. Idx memiliki jumlah baris yang sama dengan Y. **X** _input data (numeric matric)_ , input data ditentukan sebagai matrik numerik. Baris X sesuai dengan pengamatan dan kolom sesuai dengan variable. **Y** _query point (numeric matric), queri point_ ditentukan sebagai matrik nnumerik. Baris Y sesuai dengan pengamatan, dan kolom sesuai dengan variable. Y haris memiliki jumlah kolom yang sama dengan X. 

74 

Langkah langkah pemrograman matlab untuk mengklasifikasikan bentuk suatu objek dalam citra digital adalah sebagai berikut: 1. Mempersiapkan data latih ektraksi ciri objek bangunan, yaitu: 50 ciri objek bangunan tipe A (Bangunan Besar) yang dikategorikan ke nilai= 1, 50 ciri objek bangunan tipe B (Bangunan Sedang) yang dikategorikan ke nilai=2, 50 ciri objek bangunan tipe C (Bangunan Kecil) yang dikategorikan ke nilai=3, total 150 dataset tipe bangunan. 2. Mempersiapkan data uji berupa hasil ekstraksi ciri dari masing masing objek yang terdeteksi pada citra uji yang diproses didalam sistem. 3. Klasifikas Tipe bangunan dengan menggunakan metode _kNN_ ( _fitcknn)_ . 4. Mencari jarak terdekat masing masing objek terhadap data latih dengan menggunakan _kNN search_ . 5. Menampilkan Hasil klasifikasi dan sebaran data klasifikasi. Pengujian sistem deteksi dan klasifikasi bangunan dengan metode _knn_ yang dibangun pada matlab sebagai berikut: 

75 

- A. Gambar Uji yang digunakan 

**==> picture [307 x 156] intentionally omitted <==**

Gambar 4. 4 Citra Bangunan 

Citra satelit bangunan ini akan digunakan sebagai gambar uji untuk menguji 

kemampuan deteksi sistem dalam mendeteksi objek bangunan pada citra satelit dan hasil ektraksi ciri yang didapatkan akan digunakan sebagai data uji untuk proses klasifikasi bangunan dengan menggukan algoritma _knn_ yang telah diterapkan didalam sistem sehingga didapatkan hasik akurasi klasifikasi sistem. 

- B. Interface Uji Sistem 

**==> picture [363 x 179] intentionally omitted <==**

Gambar 4. 5 Interface Sistem 

76 

Pada interface ditampilkan jumlah bangunan terdeteksi, hasil ektraksi ciri dan sebaran data bangunan. Dan proses segmentasi warna untuk mencari objek bangunan akan ditampilkan pada setiap  figure yang muncul ketiga menekan _button_ proses. Proses yang ditampilkan pada _Figure_ : a. _Figure_ 1 citra Rgb dikonversikan ke warna LAB b. _Figure_ 2 warna LAB dibagi menjadi 3 berdasarkan _cluster index_ c. _Figure_ 3 menampilkan cluster 1 d. _Figure_ 4 menampilkan cluster 2 e. _Figure_ 5 menampilkan cluster 3 f. _Figure_ 6 menampilkan hasil deteksi ( terdapat noise) g. _Figure_ 7 menampilkan hasil deteksi (tanpa noise) h. _Figure_ 8 menampilkan hasil konversi biner bangunan terdeteksi i. _Figure_ 9 menampilkan penyempurnaan hasil deteksi pada warna biner j. _Figure_ 10 menampilkan labeling objek terdeteksi. Selanjutnya hasil klasifikasi dengan menggunakan _k Nearest Neighbor_ akan ditampilkan pada _command window_ matlab: 

77 

Tabel 4. 24 Hasil Deteksi dan Klasifikasi Sistem 

|Objek|Luas|Keliling|Klasifikasi|Tipe|Distance  Luas|Distance  Luas|Distance Keliling|
|---|---|---|---|---|---|---|---|
|1|869|125,11|3|C|1,28||0,17|
|2|2995|275,38|2|B|3,02||0,23|
|3|3635|298,61|2|B|3,65||0,27|
|4|2588|234,27|2|B|2,58||0,21|
|5|1682|175,84|3|C|1,68||0,18|
|6|1734|181,24|3|C|1,74||0,20|
|7|1429|156,75|3|C|1,52||0,19|
|8|1674|179,05|3|C|1,68||0,18|
|9|2342|214,81|3|C|2,35||0,20|
|10|4791|398,69|1|A|4,70||0,37|
|11|1197|148,81|3|C|1,28||0,17|
|12|4165|333,68|2|B|4,18||0,30|
|13|2303|211,15|3|C|2,32||0,21|
|14|1687|168,43|3|C|1,68||0,18|
|15|2790|246,81|2|B|2,80||0,25|
|16|1465|155,24|3|C|1,52||0,19|
|17|1485|159,25|3|C|1,52||0,19|
|18|3688|329,14|2|B|3,74||0,28|
|19|1515|155,84|3|C|1,54||0,15|
|20|4023|337,48|1|A|4,06||0,26|
|21|1238|142,18|3|C|1,28||0,17|
|22|2184|211,30|3|C|2,16||0,22|
|23|1268|144,43|3|C|1,28||0,17|
|24|5001|375,52|1|A|4,94||0,34|
|25|1871|177,11|3|C|1,87||0,17|
|26|1529|159,50|3|C|1,54||0,15|
|27|1502|158,43|3|C|1,52||0,19|
|28|1575|159,94|3|C|1,55||0,16|
|29|1853|199,44|3|C|1,85||0,21|
|30|1402|147,36|3|C|1,28||0,17|
|||Akurasi k Nearest Neighbor Sistem||||||
|Correct Rate||Error Rate||Sensitivity||Specificity||
|0,9667||0,0333||1||0,9900||



Pada table diatas hasil klasifikasi sistem ditampilkan pada _coman window matlab_ yaitu 30 objek bangunan terdeteksi kemudian sistem mengklasifikasikan dengan _knn_ berdasarkan jarak terdekat dengan 150 data latih menggunakan 

78 

_Euclidean Distance_ dan parameter _k_ = 5. Akurasi _k Nearest Neighbor_ sistem menujukkna _Correct Rate_ : 96,67%, _Error Rate_ : 3,33%, _Sensitivity_ : 100%, _Specificity_ : 99%. 

## **4.4. Integrasi Dengan Al Quran** 

Penelitian ini menggunakan metode segmentasi warna untuk mendeteksi ciri objek yang terdeteksi kemudian metode _k Kearest Ninghbor_ untuk mengklasifikasikan objek yang terdeteksi yaitu bangunan dengan ciri ukuran Luas dan Kelilingnya _._ Metode _kNN_ bekerja dengan menghitung jarak terdekat data uji dengan data latih menggunakan perhitungan jarak _Euclidean_ kemudian melakukan voting mayoritas nilai _k_ terhadap jarak data uji ke jarak data latih. 

Penelitian ini erat sekali kaitannya dengan proses pengataman sehingga 

manusia bisa mengambil pelajaran dan manfaat dari apa yang diamatinya. Dalam Al Quranasurat Ali Imranaayat 190-191 Allah berfirman: 

> [َ َٰ] بل ٱ و ه ٱو[َ َٰ] تِلخٱو ٱو[َ َٰ] و[َ َٰ] ملسٱ ل َّبَِّ ۡل َِّلِ تٖ َّۡل[َ َٰ] ٓأَليَّارَِّ نل َّ َّ َّللَِّ[  ۡ] َّٱفِ َّ َّ َّۡرضِ َّۡل َّ َّتَِّ قِ َّ َّخِفَِّ إِنَّ قَِّلَّخ َِّفِ ونركفتي َّووبِهِمنَّج لَع[َ َ َٰ] ا َّوودعقا َّوم[َ َٰ] قِيَّ ّللَّ ٱ[  َ] َّ ونركذيَّ ِينَّ َّلٱَّ ٠٩١ ٱ ابذ قِن كن[َ َٰ] حب ذ تقل نبر ٱو[َ َٰ] و[َ َٰ] ملسٱ َّ َّ ١٩١ َّ نلارَِّ َّ اَّع َّف َّسطِٗل[َ َٰ] اَّب[َ َٰ] َّه اَّخاَّم َّۡرضِ َّۡل َّ َّتَِّ َّ 

190. _Sesungguhnya dalam penciptaan langit dan bumi, dan silih bergantinya malam dan siang terdapat tanda-tanda bagi orang-orang yang berakal_ 

191. _(yaitu) orang-orang yang mengingat Allah sambil berdiri atau duduk atau dalam keadan berbaring dan mereka memikirkan tentang penciptaan langit dan_ 

79 

_bumi (seraya berkata): "Ya Tuhan kami, tiadalah Engkau menciptakan ini dengan sia-sia, Maha Suci Engkau, maka peliharalah kami dari siksa neraka._ Dalam Tafsir al Muyassar dijelaskan bahwa dengan mengamati penciptaan langit dan bumi yang tejadi tanpa ada contoh seblemunnya merupakan bukti dan petunjuk akan ke Esaan Allah bagi orang orang yang berfikir. Sehingga manusia akan semakin bermanfaat dan semakin taat dengan menyadari bahwa tiadak ada hal yang sia sia yang diciptakan Allah. Dalam penelitian ini objek deteksi yaitu bangunan di indetifikasi ciri cirnya kemudian dikelompokkan dengan jarak terdekat menggunkann metode _kNN_ . Metode _kNN_ sangan erat sekai kaitannya dengan hadis Nabi. Dalam sebuahahadis Rasulullah shallallahu ‘alaihi wa sallam bersabda: _“Agama seseorang tergantung dengan agama teman dekatnya. Hendaklah kalian memerhatikan, siapa yang dia jadikan teman dekatnya.” (HR. Abu Daud dan Tirmidzi, dishahihkan oleh Syaikh Al Albani dalam Silsilah Ash-Shahihah, no. 927)”._ Pada hadis diatas kita bisa mengambil pelajaran bahwa cara kerja metode _KNN_ hampir sama seperti penjelasan hadis diatas yaitu suatu objek akan di golongkan ke dalam objek terdekatnya. Begitu juga yang di jelaskan pada hadis yang lain. Dari Abu Musa Al-Asy’ariy radhiyallahu ‘anhu berkata, Rasulullah shallallahu ‘alaihi wa sallam bersabda: 

_“Permisalan teman duduk yang shalih dan buruk adalah seperti penjual minyak wangi dan tukang pandai besi. Adapun penjual minyak wangi, bisa jadi ia akan memberimu minyak wangi, atau kamu akan membeli darinya atau kamu akan_ 

80 

_mendapat bau harum darinya. Adapun tukang pandai besi, bisa jadi ia akan membuat pakaianmu terbakar, atau kamu akan mendapat bau yang tidak sedap darinya.” (HR. Bukhari No. 2101, Muslim No. 2628)”_ . Pada ayat Al Quran dan Hadis diatas kita dapat mengambil pelajaran dari proses pengamatan dan pengelompokan, yaitu bagaiman kecendrungan suatu objek terhadap objek terdekatnya. Begitu juga dalam kehidupan sehari hari orang orang terdekat terutama lingkungan tempat tinggal akan mempengaruhi tumbuh kembang seseorang apakah akan menjadi lebih baik atau sebaliknya. 

## **BAB V** 

## **KESIMPULAN DAN SARAN** 

## **5.1. Kesimpulan** 

Berdasarkan hasil penelitian yang telah disajikan pada bab sebelumnya maka kesimpulan dalam penelitian ini adalah sebagai berikut: 1. Sistem deteksi bangunan dibangun menggunakan segmentasi warna untuk mendeteksi objek bangunan pada citra satelit dengan rata rata akurasi deteksi bangunan 90,8% dan sistem klasifikasi dibangun dengan metode _k Neraest Neighbor_ dengan perhitungan jarak _Euclidean Distance_ menggunakan parameter _k=_ 5. 2. Akurasi metode _k Nearest Neighbor_ pada sistem klasifikasi tipe bangunan didapatkan dengan pengujian _k Fold Cross Validation_ dengan _k fold_ = 5, didapatkan tingkat akurasi rata rata _k Nearest Neighbor_ 93% dalam ketepatan klasifikasi data _testing_ dengan data _training_ . **5.2. Saran** Dari hasil penelitian deteksi dan klasifikasi tipe bangunan pada citra satelit menggunkan metode _k Nerest Neighbor_ ada beberapa saran yang diberikian penulis untuk penelitian selanjutnya dengan tema yang sama: 1. Jarak ketinggian citra satelit dan kualitas warna citra yang akan di _crooping_ dari _Google Earth_ akan mempengaruhi ciri objek yang akan dideteksi. 

81 

82 

2. Perbaikan kualitas citra hasil segmentasi mempengaruhi nilai hasil ekstraksi ciri setiap objek deteki berupa penambahan dan pengurangan _pixel_ objek yaitu luas, keliling, _metric_ dan _eccentricity_ 3. Menggunakan metode perhitungan jarak selain _Euclidean distance_ antara lain _Manhatan distance_ , _Minkowsky distance, Chebychev distance_ dan lain lain dapat digunakan untuk meningkatkan akurasi deteksi, 4. Penambahan jumlah data _training_ klasifikasi akan mempengruhi tingkat akurasi klasifikasi _k Nearest Neighbor._ 

## **DAFTAR PUSTAKA** 

Akcay, H., & Aksoy, S. (2010). Building Detection Using Directional Spatial Constaraints. _IEEE International Geoscience and Remote Sensing Symposium_ , 1932-1935. Awrangjeb, M., Ravanbakhsh, M., & Fraser, C. (2010). Automatic detection of residential buildings using LIDAR data and Multispectral imagery. _ISPRS Journal of Photogrammetry and Remote Sensing_ , 457–467. Cawley, G. C., & Talbot, N. C. (2010). On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation. _Journal of Machine Learning Research_ , 2079-2107. Fu, L. (1994). _Neural Networks in Computer Intelligence._ Singapura: McGraw-Hill Companies. Gonzalez, R., & Woods, R. (2002). _Digital Image Processing. 2nd Edition._ Upper Saddle River: Prentice Hall. Gorunescu, F. (2011). _Data Mining: Concepts and Techniques._ Verlag berlin Heidelberg: Springer. Han, J., & Kamber, M. (2006). _Data Mining : Concepts and Techniques 2nd Edition._ San Fransisco: Elsevier. Izadi, M., & Saeedi, P. (2010). Automatic Building Detection in Aerial Images using a Hierarchical Feature Based Image Segmentation. _International Conference on Pattern Recognition_ , 472-475. Kurniawan, F., Nugroho, S. M., & Hariadi, M. (2018). Smart City Priority Correlation Using Differential Equation. _IEEE Computing in Science & Engineering_ . Liang, C., Gong, J., Chen, X., & Han, P. (2008). Building boundary extraction from high resolution imagery and LIDAR data. _International Archives of the Photogrammetry, Remote Sensing and Spatial Information Science 37 (Part B3)_ , 693-698. Powers, D. M. (2011). Evaluation: From Precision, Recall, and F-Measure to ROC, Infomedness, Markedness & Correlation. _Journal of Machine Learning Technologies_ , 37-63. Rizal, A. (2013). Perbandingan Performa antara Imputasi Metode Konvensional dan Imputasi dengan Algoritma Mutual Nearest Neighbor. _Jurusan Teknik Informatika, Fakultas Teknologi Informasi, Institut Teknologi Sepuluh Nopember. Surabaya_ . 

83 

84 

Seni, G., & Elder, J. (2010). Ensemble Methods in Data Mining: Improving Accuracy Through Combining Predictions. _Synthesis Lectures on Data Mining and Knowledge Discovery_ , 1-126. Setiawan, W., & Damayanti, F. (2016). Klasifikasi Citra Retina Menggunakan K Nearest Neighbor Untuk Mendeteksi Mokulopati Diabetik. _Seminar Nasional Sains and Teknologi_ , 1-6. Sinaga, A. S. (2019). Segmentasi Ruang Warna L*a*b. _Jurnal Mantik Penusa_ , 43-46. Subairi, Rahmadwati, & Yudaningtyas, E. (2018). Implementasi Metode k- Nearest Neighbor pada Pengenalan Pola Tekstur Citra Saliva untuk Deteksi Ovulasi. _Jurnal EECCIS Vol. 12,_ , 9-14. Suyatno. (2017). _Data mining untuk klasifikasi dan klasterisasi data._ Bandung: Informatika Bandung. Wahyudi, M. Z. (2012, Agustus 23). _Nasional News_ . Retrieved from www.kompas.com: https://nasional.kompas.com/read/2012/08/23/21232065/%20Hampi r.54.Persen.Penduduk.Indonesia.Tinggal.di.Kota Whidhiasih, R. N., Wahanani, N. A., & Supriyanto. (2013). Klasifikasi Buah Belimbing Berdasarkan Citra Red-Green-Blue Menggunakan k-NN dan LDA. _Jurnal Penelitian Ilmu Komputer, System Embedded & Logic_ , 29-35. Wu, X., & Kumar, V. (2009). _The Top Ten Algorithms In Data Mining._ London: CRC PRESS, Taylor & Francis Group. 

## **LAMPIRAN** 

**==> picture [384 x 476] intentionally omitted <==**

**----- Start of picture text -----**<br>
    Gambar Uji:<br>No.  Gambar<br>1<br>2<br>3<br>**----- End of picture text -----**<br>


83 

86 

**==> picture [370 x 607] intentionally omitted <==**

**----- Start of picture text -----**<br>
4<br>5<br>6<br>7<br>**----- End of picture text -----**<br>


87 

**==> picture [370 x 616] intentionally omitted <==**

**----- Start of picture text -----**<br>
8<br>9<br>10<br>11<br>**----- End of picture text -----**<br>


88 

**==> picture [370 x 634] intentionally omitted <==**

**----- Start of picture text -----**<br>
12<br>13<br>14<br>15<br>**----- End of picture text -----**<br>


89 

**==> picture [370 x 527] intentionally omitted <==**

**----- Start of picture text -----**<br>
16<br>17<br>18<br>**----- End of picture text -----**<br>


