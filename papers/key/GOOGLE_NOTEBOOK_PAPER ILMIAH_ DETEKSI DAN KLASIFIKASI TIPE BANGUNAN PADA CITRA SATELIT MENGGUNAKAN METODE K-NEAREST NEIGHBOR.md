### PAPER ILMIAH: DETEKSI DAN KLASIFIKASI TIPE BANGUNAN PADA CITRA SATELIT MENGGUNAKAN METODE K-NEAREST NEIGHBOR

#### 1\. ABSTRAK AND KEYWORDS

Laju pertumbuhan populasi dan ketimpangan pembangunan memicu tingginya arus urbanisasi di Indonesia, yang berimplikasi langsung pada kompleksitas tata ruang serta kebutuhan mendesak akan infrastruktur perkotaan yang cerdas ( *Smart Infrastructure* ). Penelitian ini mengusulkan sebuah pendekatan komputasional untuk pengenalan dan pengelompokan objek permukaan bumi melalui otomatisasi deteksi dan klasifikasi tipe bangunan pada citra satelit resolusi tinggi yang diperoleh dari Google Earth pada ketinggian 700–800 meter. Tahapan metodologis mencakup konversi ruang warna citra dari RGB ke  \$CIELab\$  ( \$L^\*a^*b^*\$ ), segmentasi warna berbasis kemiripan wilayah ( *region similarity* ) yang disempurnakan dengan pemrosesan morfologi biner (Erosi, Dilasi,  *Opening* ,  *Filling Holes* , dan  *Bwareaopen* ), ekstraksi vektor fitur geometris 4-dimensi (Luas, Keliling,  *Eccentricity* , dan  *Metric* ), serta klasifikasi tipe bangunan terawasi ( *Tipe Bangunan A, B, dan C* ) menggunakan algoritma  *k-Nearest Neighbor*  ( \$k\$ \-NN) yang divalidasi via  *5-Fold Cross Validation* . Hasil eksperimental menunjukkan bahwa segmentasi warna berbasis ruang  \$CIELab\$  berhasil mendeteksi objek fisik bangunan dengan rata-rata akurasi sebesar 90,8%. Pada tahap klasifikasi tipe bangunan, pemodelan hyperparameter  \$k=5\$  menghasilkan akurasi pengenalan optimal sebesar 93,0%. Evaluasi stabilitas model melalui  *5-fold cross-validation*  mengonfirmasi keandalan sistem dengan pencapaian rata-rata akurasi sebesar 93,0%. Dengan demikian, integrasi segmentasi warna dan klasifikasi  \$k\$ \-NN terbukti efektif sebagai instrumen komputasional terstruktur pendukung pemetaan tata ruang dan pengembangan  *Smart City* .  
**Kata Kunci / Keywords:**   **Citra Satelit** ,  **Segmentasi Warna** ,  **Deteksi Bangunan** ,  **k Fold Cross Validation** ,  **k Nearest Neighbor**  
Rangkuman komprehensif di atas memberikan dasar konseptual dan empiris yang melandasi uraian mendalam mengenai urgensi, arsitektur sistem, serta hasil evaluasi eksperimental pada bagian-bagian selanjutnya.

#### 2\. PENDAHULUAN

Pola migrasi penduduk dari kawasan pedesaan menuju perkotaan di Indonesia menunjukkan eskalasi yang signifikan dari tahun ke tahun. Ketimpangan fasilitas dan pertumbuhan ekonomi antara desa dan kota menjadi faktor pendorong utama arus urbanisasi ini. Kondisi tersebut memicu tekanan ekologis dan spasial di berbagai kota besar, seperti timbulnya kelangkaan sumber daya, peningkatan polusi, kemacetan lalu lintas, krisis kesehatan masyarakat, dan ketidakcukupan infrastruktur dasar. Untuk menangani kompleksitas dampak demografis ini, paradigma Kota Cerdas ( *Smart City* ) hadir sebagai solusi strategis untuk menciptakan keharmonisan antara aspek spasial, sosial, ekonomi, dan lingkungan. Dalam konteks ini, pengolahan citra satelit secara otomatis memainkan peranan vital dalam menyediakan data geografis dan struktur permukaan bumi yang presisi guna mendukung perencanaan tata ruang yang adaptif.  
Berdasarkan data Sensus Penduduk tahun 2010 dari Badan Pusat Statistik (BPS), total populasi Indonesia tercatat sebanyak 237.641.326 jiwa, yang mencakup 49,79% (118.320.256 jiwa) di kawasan perkotaan dan 50,21% (119.321.070 jiwa) di kawasan pedesaan. Angka populasi perkotaan mengalami lonjakan pesat hingga diperkirakan mencapai 54% atau sekurang-kurangnya 129,6 juta jiwa yang menghuni wilayah perkotaan. Peningkatan populasi yang masif ini memerlukan dukungan parameter infrastruktur cerdas ( *Smart Infrastructure* ), yang merupakan satu dari delapan parameter  *Smart City*  untuk negara berkembang (meliputi  *Smart Energy* ,  *Smart Infrastructure* ,  *Smart People* ,  *Smart Health* ,  *Smart Mobility* ,  *Smart Governance* ,  *Smart Education* , dan  *Smart Technology* ). Penerapan  *Smart Infrastructure*  memerlukan sistem identifikasi objek otomatis untuk menganalisis keberadaan kendaraan, jaringan jalan, dan tata letak bangunan. Deteksi serta ekstraksi batas bangunan secara otomatis dari citra satelit Google Earth pada ketinggian akuisisi 700–800 meter menjadi prasyarat teknis utama dalam pemetaan infrastruktur perumahan, manajemen bencana, dan pemodelan kota secara spasial.  
Secara filosofis dan teologis, eksplorasi ilmu pengetahuan untuk mempelajari dan menata struktur permukaan bumi memiliki landasan normatif yang terintegrasi dalam Al-Qur'an Surah Ali 'Imran (3:190–191):  
*"Sesungguhnya dalam penciptaan langit dan bumi, dan silih bergantinya malam dan siang terdapat tanda-tanda bagi orang-orang yang berakal, (yaitu) orang-orang yang mengingat Allah sambil berdiri atau duduk atau dalam keadaan berbaring dan mereka memikirkan tentang penciptaan langit dan bumi (seraya berkata): 'Ya Tuhan kami, tiadalah Engkau menciptakan ini dengan sia-sia, Maha Suci Engkau, maka peliharalah kami dari siksa neraka.'"*  
Berdasarkan  *Tafsir al-Muyassar* , ayat tersebut menegaskan bahwa penciptaan langit, bumi, serta dinamika pergantian waktu merupakan bukti keagungan Pencipta bagi manusia yang berakal ( *ulul albab* ). Manusia diperintahkan untuk melakukan tadabur, eksplorasi komputasional yang sistematis, dan mengolah potensi permukaan bumi secara rasional agar memberikan pemanfaatan nyata bagi kemanusiaan serta menghindarkan masyarakat dari kerusakan tata ruang.

##### Pernyataan Masalah

1. Bagaimana merancang dan mengimplementasikan sistem otomatis untuk mendeteksi objek bangunan berdasarkan segmentasi warna citra serta mengklasifikasikan tipe bangunan menggunakan algoritma  *k-Nearest Neighbor*  ( \$k\$ \-NN)?  
2. Berapa tingkat akurasi komputasional yang diperoleh dari kombinasi metode segmentasi warna dan algoritma  *k-Nearest Neighbor*  dalam mengklasifikasikan tipe bangunan pada citra satelit?

##### Tujuan Penelitian

1. Membangun arsitektur sistem deteksi dan klasifikasi tipe bangunan dari citra satelit Google Earth berbasis segmentasi warna dan algoritma  *k-Nearest Neighbor* .  
2. Menganalisis dan mengukur tingkat akurasi kuantitatif dari metode segmentasi gambar dan algoritma  *k-Nearest Neighbor*  yang divalidasi menggunakan  *5-Fold Cross Validation* .

Uraian mendasar mengenai problematika tata ruang perkotaan serta sasaran penelitian ini menjadi landasan dalam penyusunan kerangka metodologis dan arsitektur pengolahan citra pada bagian berikutnya.

#### 3\. METODOLOGI PENELITIAN DAN LANDASAN TEORI

Sistem komputasi visual yang dirancang mengolah citra satelit digital murni ( *raw RGB* ) menjadi vektor fitur geometris terstruktur untuk pengenalan pola tipe bangunan. Seperti yang diilustrasikan pada Gambar 1, alur pemrosesan terdiri atas empat tahap utama: akuisisi dan konversi ruang warna, segmentasi biner dan pembersihan morfologi, ekstraksi vektor ciri geometris, serta klasifikasi terawasi ( *supervised learning* ) menggunakan  \$k\$ \-NN.  
\+-----------------------+  
\|  Citra Satelit RGB    \|  
\| (Google Earth 700-800m\|  
\+-----------+-----------+  
            \|  
            v  
\+-----------------------+  
\| Konversi Ruang Warna  \|  
\|   RGB \-\> XYZ \-\> CIELab\|  
\+-----------+-----------+  
            \|  
            v  
\+-----------------------+  
\| Segmentasi Warna &    \|  
\| Morfologi Biner       \|  
\| (Erosi,Dilasi,Opening)\|  
\+-----------+-----------+  
            \|  
            v  
\+-----------------------+  
\|  Ekstraksi Fitur      \|  
\|  Geometris 4-Dimensi  \|  
\|  x \= \[A, P, e, M\]^T   \|  
\+-----------+-----------+  
            \|  
            v  
\+-----------------------+  
\| Klasifikasi k-NN &    \|  
\| 5-Fold Cross Valid.   \|  
\+-----------------------+

**Gambar 1: Arsitektur Pipeline Pemrosesan Citra dan Klasifikasi**

##### Akuisisi Citra & Konversi Ruang Warna

Ruang warna standar RGB ( *Red, Green, Blue* ) berbasis koordinat kartesius aditif tiga dimensi sangat rentan terhadap derau dan variasi pencahayaan ( *illumination variance* ). Untuk memisahkan komponen intensitas cahaya dari informasi kromatik serta meningkatkan daya pemisah antara latar belakang (vegetasi/tanah) dan atap bangunan, citra RGB ditransformasikan ke ruang warna  \$CIELab\$  ( \$L^\*a^*b^*\$ ) melalui ruang warna perantara  \$XYZ\$ .  
Matriks transformasi linier dari RGB ke  \$XYZ\$  dirumuskan sebagai berikut:  
\$\$\\begin{bmatrix} X \\\\ Y \\\\ Z \\end{bmatrix} \= \\begin{bmatrix} 0.412453 & 0.357580 & 0.180423 \\\\ 0.212671 & 0.715160 & 0.072169 \\\\ 0.019334 & 0.119193 & 0.950227 \\end{bmatrix} \\begin{bmatrix} R \\\\ G \\\\ B \\end{bmatrix}\$\$  
Selanjutnya, konversi non-linier dari  \$XYZ\$  ke ruang warna  \$CIELab\$  dihitung berdasarkan persamaan:  
\$\$L^\* \= 116 \\left( \\frac{Y}{Y\_n} \\right)^{\\frac{1}{3}} \- 16 \\quad \\text{untuk } \\frac{Y}{Y\_n} \> 0.008856, \\quad \\text{atau} \\quad L^\* \= 903.3 \\left( \\frac{Y}{Y\_n} \\right) \\quad \\text{lainnya}\$\$  
\$\$a^\* \= 500 \\leftf\\left(\\frac{X}{X\_n}\\right) \- f\\left(\\frac{Y}{Y\_n}\\right) \\right\$\$  
\$\$b^\* \= 200 \\leftf\\left(\\frac{Y}{Y\_n}\\right) \- f\\left(\\frac{Z}{Z\_n}\\right) \\right\$\$  
dengan fungsi pembobot  \$f(t) \= t^{1/3}\$  untuk  \$t \> 0.008856\$  dan  \$f(t) \= 7.787 t \+ \\frac{16}{116}\$  untuk kondisi sebaliknya. Nilai  \$X\_n, Y\_n, Z\_n\$  menyatakan titik acuan putih ( *white reference point* ). Kanal  \$L^*\$  mendeskripsikan kecerahan ( luminance ) pada rentang 0 hingga 100, kanal  \$a^*\$  merepresentasikan aksis kromatik hijau-merah (-80 hingga \+80), dan kanal  \$b^\*\$  merepresentasikan aksis biru-kuning (-70 hingga \+70). Transformasi ini menghasilkan representasi persepsi warna yang independen dari pencahayaan lingkungan.

##### Segmentasi Warna & Pemrosesan Morfologi Biner

Segmentasi berbasis kemiripan wilayah ( *region-based similarity segmentation* ) mengelompokkan piksel pada bidang  \$a^*b^*\$ . Citra biner hasil segmentasi awal sering kali mengandung derau tepi ( *edge noise* ) dan rongga interior. Oleh karena itu, diterapkan operasi morfologi biner terstruktur:

1. **Erosi (**  **\$\\ominus**\$  **):**  Menilai interaksi antara citra biner  \$A\$  dan elemen pengolah ( *structuring element* )  \$B\$ . Erosi mengikis batas luar objek dan mengeliminasi derau terisolasi:  \$\$A \\ominus B \= \\{z \\mid (B)\_z \\subseteq A\\}\$\$  
2. **Dilasi (**  **\$\\oplus**\$  **):**  Memperluas batas objek biner untuk menghubungkan segmen yang terpisah dan menutup celah kecil:  \$\$A \\oplus B \= \\{z \\mid (\\hat{B})\_z \\cap A \\neq \\emptyset\\}\$\$  
3. **Opening (**  **\$A \\circ B**\$  **):**  Operasi erosi yang dilanjutkan dengan dilasi menggunakan elemen pengolah  \$B\$  yang sama.  *Opening*  menghapus tonjolan halus dan piksel derau kecil tanpa mengubah ukuran objek utama secara signifikan:  \$\$A \\circ B \= (A \\ominus B) \\oplus B\$\$  
4. **Filling Holes:**  Mengisi rongga interior ( *hole* ) ber-nilai 0 yang sepenuhnya dikelilingi oleh foreground piksel bernilai 1 pada objek bangunan.  
5. **Bwareaopen:**  Operasi penyaringan area biner untuk menghapus seluruh komponen terhubung ( *connected components* ) yang memiliki total area di bawah ambang batas piksel tertentu ( \$A\_{\\text{min}}\$ ).

##### Ekstraksi Fitur Geometris & Vektor Ciri

Setiap region bangunan biner yang telah diisolasi diekstraksi karakteristik geometrisnya. Untuk menguantifikasi kebulatan, skala, dan profil spasial bangunan, dibentuk  **vektor fitur masukan 4-dimensi**   \$\\mathbf{x}\_i\$ :  
\$\$\\mathbf{x}\_i \= \\begin{bmatrix} A\_i \\\\ P\_i \\\\ e\_i \\\\ M\_i \\end{bmatrix} \\in \\mathbb{R}^4\$\$  
Rincian formulasi matematis untuk setiap elemen fitur disajikan pada Tabel 1\.  
Parameter Ciri,Deskripsi Spasial / Geometris,Formulasi Matematika  
Luas (  \$A\$  ),Jumlah piksel penyusun wilayah interior segmen bangunan.,"\$A \= \\sum\_{x} \\sum\_{y} I(x,y)\$"  
Keliling (  \$P\$  ),Jarak total sepanjang batas luar ( boundary ) segmen biner.,\$P \= \\text{Jumlah piksel piksel tepi}\$  
Eccentricity (  \$e\$  ),"Jarak antara fokus elips penyokong terhadap sumbu utamanya (rentang 0 hingga 1). Nilai  \$e \\to 0\$  menunjukkan bentuk melingkar, sedangkan  \$e \\to 1\$  menunjukkan bentuk memanjang.",\$e \= \\frac{c}{a} \= \\sqrt{1 \- \\left(\\frac{b}{a}\\right)^2}\$  
Metric (  \$M\$  ),Indeks kebulatan ( circularity/compactness ). Objek lingkaran sempurna bernilai  \$M \= 1\$ .,\$M \= \\frac{4 \\pi \\cdot A}{P^2}\$  
Kombinasi skala ( \$A, P\$ ) dan representasi bentuk ( \$e, M\$ ) memberikan daya pemisah ( *discriminative power* ) yang kuat dalam membedakan tipe bangunan perumahan (Tipe A, B, dan C) yang memiliki variasi luas tapak dan rasio kebulatan struktur atap.

##### Klasifikasi  \$k\$ \-Nearest Neighbor ( \$k\$ \-NN) dan Cross-Validation

Algoritma  \$k\$ \-NN mengklasifikasikan vektor fitur uji  \$\\mathbf{x}\_u\$  berdasarkan jarak Euclidean terkecil terhadap sekumpulan vektor fitur data latih  \$\\mathbf{x}\_j\$ :  
\$\$d(\\mathbf{x}*u, \\mathbf{x}j) \= \\sqrt{\\sum{k=1}^{4} (x*{uk} \- x\_{jk})^2}\$\$  
Kelas definitif ditentukan berdasarkan mayoritas suara ( *majority voting* ) dari  \$k\$  tetangga terdekat. Untuk menjamin validitas empiris serta menghindari bias pembagian data ( *overfitting* ), evaluasi performa diuji menggunakan metode  *5-Fold Cross Validation* .  
Penerapan metodologi bertahap ini memfasilitasi pengujian eksperimental secara terstruktur yang dipaparkan pada bagian pembahasan berikut.

#### 4\. HASIL UJI COBA DAN PEMBAHASAN

Pengujian empiris dilakukan untuk mengukur kinerja komputasional sistem dalam dua tahap utama: keandalan segmentasi warna dalam mendeteksi fisik bangunan serta ketepatan pengelompokan tipe bangunan berbasis algoritma  \$k\$ \-NN.

##### Kinerja Deteksi Bangunan Berbasis Segmentasi Warna

Segmentasi pada ruang warna  \$CIELab\$  yang diintegrasikan dengan pemersihan morfologi biner menunjukkan keunggulan signifikan dalam memisahkan wilayah atap bangunan dari derau latar belakang seperti vegetasi, bayangan, dan jalan raya. Berdasarkan pengujian terhadap sampel citra satelit Google Earth pada ketinggian 700–800 meter, sistem meraih rata-rata akurasi deteksi keberadaan bangunan sebesar  **90,8%** .

##### Dataset Tipe Bangunan dan Analisis Fitur Geometris

Dataset pengujian klasifikasi terdiri atas 3 kelas utama tipe bangunan perumahan yang diekstraksi dari citra satelit:

* **Tipe Bangunan A:**  Perumahan skala kecil / kompak (luas tapak bangunan relatif terbatas).  
* **Tipe Bangunan B:**  Perumahan skala menengah (rasio luas dan keliling seimbang).  
* **Tipe Bangunan C:**  Bangunan skala besar / memanjang (luas tapak besar dengan nilai  *eccentricity*  lebih tinggi).

Vektor fitur  \$\\mathbf{x}\_i \= A\_i, P\_i, e\_i, M\_i^T\$  terbukti secara statistik mampu memisahkan ketiga kelas ini. Nilai  *Metric*  ( \$M\$ ) dan  *Eccentricity*  ( \$e\$ ) membedakan kekompakan bentuk struktur, sementara  *Luas*  ( \$A\$ ) dan  *Keliling*  ( \$P\$ ) mengelompokkan skala fisik bangunan.

##### Analisis Hyperparameter Klasifikasi  \$k\$ \-NN

Evaluasi ketepatan klasifikasi dilakukan dengan menguji matriks konfusi ( *confusion matrix* ) pada berbagai nilai hyperparameter tetangga terdekat ( \$k \= 3, 5, 7, 9, 11\$ ). Hasil pengujian akurasi disajikan pada Tabel 2\.  
Nilai Hyperparameter ( \$k\$ ),Akurasi Klasifikasi  \$k\$ \-NN (%),Evaluasi Kinerja Komputasional  
\$k \= 3\$,"86,7%",Sub-optimal (Sensitif terhadap derau lokal)  
\$k \= 5\$,"93,0%",Optimal (Keseimbangan bias-variansi puncak)  
\$k \= 7\$,"90,0%",Baik  
\$k \= 9\$,"86,7%",Sub-optimal  
\$k \= 11\$,"83,3%",Penurunan Kinerja ( Over-smoothing )  
Berdasarkan analisis performa, konfigurasi  **\$k \= 5**\$  mencapai puncak akurasi klasifikasi sebesar  **93,0%** . Dari perspektif komputasi visual, penurunan akurasi pada  \$k \\ge 7\$  ( \$90,0\\%\$  pada  \$k=7\$  hingga  \$83,3\\%\$  pada  \$k=11\$ ) disebabkan oleh efek  *over-smoothing*  pada batas keputusan ( *decision boundary* ). Ketika  \$k\$  terlalu besar, tetangga yang lokasinya jauh dalam ruang fitur 4-dimensi ikut terhitung dalam voting, sehingga mengaburkan batas antar kelas dan memicu salah klasifikasi sampel uji.

##### Benchmarking dan Stabilitas Model via 5-Fold Cross Validation

Untuk memverifikasi bahwa akurasi 93,0% bukan disebabkan oleh kebetulan pembagian data latih-uji, dilakukan pengujian keandalan menggunakan  *5-Fold Cross Validation*  ( \$k\$ \-Fold \= 5). Rincian akurasi untuk setiap  *fold*  ditampilkan pada Tabel 3\.  
Pengujian Cross-Validation,Akurasi Klasifikasi per Fold (%)  
Test Fold 1,"91,7%"  
Test Fold 2,"95,0%"  
Test Fold 3,"91,7%"  
Test Fold 4,"93,3%"  
Test Fold 5,"93,3%"  
Rata-rata Akurasi Overall,"93,0%"  
Hasil konsistensi antara pengujian  *split*  acak ( \$k=5\$ ) dan nilai rata-rata  *5-Fold Cross Validation*  yang sama-sama mencapai  **93,0%**  menegaskan stabilitas generalisasi model  \$k\$ \-NN. Kombinasi 4 fitur geometris terbukti memiliki ketahanan ( *robustness* ) yang tinggi terhadap variasi skala bangunan pada citra satelit.  
Rangkaian temuan empiris ini memberikan landasan objektif untuk penarikan kesimpulan akhir serta penyusunan saran pengembangannya.

#### 5\. KESIMPULAN DAN SARAN

Penelitian ini berhasil menjawab tantangan otomatisasi deteksi dan klasifikasi tipe bangunan pada citra satelit resolusi tinggi sebagai instrumen pendukung  *Smart Infrastructure* . Integrasi konversi ruang warna  \$CIELab\$ , pemrosesan morfologi biner terstruktur, ekstraksi vektor fitur geometris 4-dimensi, dan pemodelan  \$k\$ \-NN terbukti menghasilkan performa pengenalan objek bumi yang presisi, stabil, dan relevan untuk analisis tata ruang perkotaan.

##### 5.1 Kesimpulan

1. **Keberhasilan Pembangunan Arsitektur Sistem:**  Sistem otomatisasi pemrosesan citra satelit telah berhasil dibangun melalui integrasi konversi ruang warna RGB ke  \$CIELab\$ , segmentasi wilayah dengan penyaringan morfologi biner (Erosi, Dilasi,  *Opening* ,  *Filling Holes* , dan  *Bwareaopen* ), ekstraksi vektor ciri 4-dimensi  \$\\mathbf{x} \= A, P, e, M^T\$ , serta klasifikasi terawasi menggunakan algoritma  \$k\$ \-Nearest Neighbor.  
2. **Kinerja dan Stabilitas Akurasi:**  Tahap segmentasi warna berbasis ruang  \$CIELab\$  meraih rata-rata akurasi deteksi keberadaan bangunan sebesar  **90,8%** . Pada tahap klasifikasi tipe bangunan (Tipe A, B, dan C), algoritma  \$k\$ \-NN dengan hyperparameter optimal  **\$k \= 5**\$  menghasilkan akurasi klasifikasi tertinggi sebesar  **93,0%** . Keandalan generalisasi model terbukti sangat stabil dengan pencapaian rata-rata akurasi sebesar  **93,0%**  pada validasi  *5-Fold Cross Validation* .

##### 5.2 Saran

1. **Pengembangan Ekstraksi Fitur Multimodal:**  Penelitian selanjutnya disarankan untuk memperluas vektor masukan fitur dengan mengintegrasikan fitur tekstur spasial ( *Gray-Level Co-occurrence Matrix*  / GLCM) dan fitur momen warna ( *Color Moments* ), guna meningkatkan pemisahan kelas pada tipe bangunan yang memiliki kesamaan profil geometris namun berbeda tekstur atap.  
2. **Peningkatan Variasi Dataset Satelit:**  Perlu diperluas cakupan akuisisi dataset dengan melibatkan variasi sudut elevasi satelit, rentang ketinggian akuisisi yang lebih beragam, serta tingkat kompleksitas bayangan lingkungan yang lebih tinggi untuk menguji ketahanan ( *robustness* ) sistem pada skala pemetaan wilayah perkotaan yang lebih heterogen.

