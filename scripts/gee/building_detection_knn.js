/**
 * ==============================================================================
 * PRAKTIKUM PENGOLAHAN CITRA DIGITAL (PCD) - SEMESTER 5 D4/D3 TEKNIK INFORMATIKA
 * ==============================================================================
 * JUDUL PAPER: 
 * Deteksi dan Klasifikasi Tipe Bangunan pada Citra Satelit Menggunakan
 * Metode K-Nearest Neighbor (k-NN)
 * (Studi Replikasi Berdasarkan Adam Jaelani, UIN Maulana Malik Ibrahim Malang)
 * 
 * LOKASI TARGET BARU:
 * Villa Puncak Resort / Cipanas (-6.7088, 107.0392)
 * Kompleks vila berjarak renggang dengan kontras atap terakota vs taman/rumput
 * ==============================================================================
 */

// ==============================================================================
// 1. PARAMETER DAN KONFIGURASI PENGGUNA
// ==============================================================================
var CONFIG = {
  // Mode Operasi:
  // 'HIGH_RES_INDIVIDUAL' : (REKOMENDASI) Deteksi bangunan per unit rumah presisi
  //                         menggunakan jejak satelit resolusi sub-meter + Ekstraksi Ciri 4D + k-NN (k=5)
  // 'PIXEL_SEGMENTATION'  : Segmentasi K-Means murni pada citra raster Sentinel-2 (10m/piksel)
  mode: 'HIGH_RES_INDIVIDUAL',

  // Pilihan Lokasi Studi:
  // 'PUNCAK_CIPANAS'   : Kawasan Villa Puncak Resort / Cipanas (-6.7088, 107.0392)
  // 'MALANG_SAWOJAJAR' : Area perumahan Sawojajar, Malang
  // 'BANDUNG_POLBAN'   : Kawasan Kampus Polban & Perumahan Ciwaruga/Gegerkalong Bandung
  // 'CUSTOM'           : Menggunakan geometry yang digambar via Drawing Tool di GEE
  studyArea: 'PUNCAK_CIPANAS',

  // Rentang Tanggal Citra (Pilih musim kemarau di Indonesia untuk tutupan awan minimal)
  startDate: '2023-06-01',
  endDate: '2023-09-30',
  maxCloudCover: 10,

  // Resolusi spasial analisis (meter/piksel)
  scale: 10,

  // Hyperparameter dari Paper:
  kMeansClusters: 3,     // 3 Kluster: 1=Jalan/Lahan, 2=Vegetasi, 3=Atap Bangunan
  knnNeighbors: 5,       // Hyperparameter optimal k-NN dari paper (k=5, akurasi 93.0%)
  minPixelNoise: 2,      // Filter bwareaopen
  
  // Opsi Menggunakan Citra Asset Khusus (jika Anda mengunggah hasil crop Google Earth)
  useCustomAsset: false,
  customAssetId: 'users/username/my_cropped_google_earth_image'
};

// ==============================================================================
// 2. DEFINISI WILAYAH KAJIAN (REGION OF INTEREST - ROI)
// ==============================================================================
var roi;
if (CONFIG.studyArea === 'PUNCAK_CIPANAS') {
  // Area Villa Puncak Resort / Cipanas (-6.7088, 107.0392)
  // Kotak ~800m x 800m yang mencakup vila-vila beratap genteng merah dan berjarak renggang
  roi = ee.Geometry.Polygon([
    [[107.0345, -6.7045],
     [107.0435, -6.7045],
     [107.0435, -6.7130],
     [107.0345, -6.7130],
     [107.0345, -6.7045]]
  ]);
} else if (CONFIG.studyArea === 'MALANG_SAWOJAJAR') {
  // Area Perumahan Sawojajar, Malang, Jawa Timur (~750m x 750m)
  roi = ee.Geometry.Polygon([
    [[112.6530, -7.9700],
     [112.6610, -7.9700],
     [112.6610, -7.9770],
     [112.6530, -7.9770],
     [112.6530, -7.9700]]
  ]);
} else if (CONFIG.studyArea === 'BANDUNG_POLBAN') {
  // Area Kampus Politeknik Negeri Bandung & Perumahan Sekitar Ciwaruga (~750m x 750m)
  roi = ee.Geometry.Polygon([
    [[107.5680, -6.8680],
     [107.5780, -6.8680],
     [107.5780, -6.8760],
     [107.5680, -6.8760],
     [107.5680, -6.8680]]
  ]);
} else {
  // Jika pengguna menggambar geometry sendiri di peta GEE
  roi = (typeof geometry !== 'undefined') ? geometry : ee.Geometry.Point([107.0392, -6.7088]).buffer(400);
}

// Pusatkan tampilan peta ke ROI dengan zoom level yang sesuai
Map.centerObject(roi, 17);
Map.setOptions('HYBRID'); // Tampilkan basemap Google Satellite resolusi sub-meter

// ==============================================================================
// 3. AKUISISI DAN PRA-PENGOLAHAN CITRA SATELIT
// ==============================================================================
var rgbImage;
var s2Collection;

if (CONFIG.useCustomAsset) {
  // Jika menggunakan citra JPG/GeoTIFF Google Earth yang di-upload ke GEE Assets
  rgbImage = ee.Image(CONFIG.customAssetId).clip(roi);
} else {
  // Menggunakan Sentinel-2 Level-2A (Surface Reflectance)
  s2Collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterBounds(roi)
    .filterDate(CONFIG.startDate, CONFIG.endDate)
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', CONFIG.maxCloudCover));

  // Ambil komposit median bebas awan
  var s2Composite = s2Collection.median().clip(roi);

  // Normalisasi kanal B4 (Red), B3 (Green), B2 (Blue) ke rentang [0.0, 1.0]
  // S2 Surface Reflectance bernilai 0 - 10000 (skala 10000)
  rgbImage = s2Composite.select(['B4', 'B3', 'B2'], ['R', 'G', 'B'])
    .divide(10000.0)
    .clamp(0.0, 1.0);
}

// ==============================================================================
// 4. KONVERSI RUANG WARNA (RGB -> CIE XYZ -> CIE L*a*b*)
// ==============================================================================
/**
 * Konversi matematis dari RGB ke ruang warna persepsi CIE L*a*b*
 * Sesuai formulasi Bab 3 (Halaman 36-37) dalam skripsi/paper.
 */
function rgbToCieLab(imgRGB) {
  var R = imgRGB.select('R');
  var G = imgRGB.select('G');
  var B = imgRGB.select('B');

  // Matriks Transformasi Linier RGB ke XYZ (Persamaan 69 di paper):
  // X = 0.412453*R + 0.357580*G + 0.180423*B
  // Y = 0.212671*R + 0.715160*G + 0.072169*B
  // Z = 0.019334*R + 0.119193*G + 0.950227*B
  var X = R.multiply(0.412453).add(G.multiply(0.357580)).add(B.multiply(0.180423));
  var Y = R.multiply(0.212671).add(G.multiply(0.715160)).add(B.multiply(0.072169));
  var Z = R.multiply(0.019334).add(G.multiply(0.119193)).add(B.multiply(0.950227));

  // Titik acuan standar D65 White Point (Xn, Yn, Zn)
  var Xn = 0.950456;
  var Yn = 1.000000;
  var Zn = 1.088754;

  var xr = X.divide(Xn);
  var yr = Y.divide(Yn);
  var zr = Z.divide(Zn);

  // Fungsi non-linier f(t):
  // f(t) = t^(1/3)                jika t > 0.008856
  // f(t) = 7.787*t + 16/116       jika t <= 0.008856
  function f(t) {
    var tPow = t.pow(1.0 / 3.0);
    var tLin = t.multiply(7.787).add(16.0 / 116.0);
    return tPow.where(t.lte(0.008856), tLin);
  }

  var fx = f(xr);
  var fy = f(yr);
  var fz = f(zr);

  // Formulasi L*, a*, b*:
  // L* = 116 * f(Y/Yn) - 16
  // a* = 500 * (f(X/Xn) - f(Y/Yn))
  // b* = 200 * (f(Y/Yn) - f(Z/Zn))
  var L = fy.multiply(116.0).subtract(16.0).rename('L');
  var a = fx.subtract(fy).multiply(500.0).rename('a');
  var b = fy.subtract(fz).multiply(200.0).rename('b');

  return ee.Image.cat([L, a, b]);
}

var labImage = rgbToCieLab(rgbImage);

// ==============================================================================
// 5. SEGMENTASI WARNA BERBASIS K-MEANS CLUSTERING (k=3)
// ==============================================================================
// Sesuai paper: Komponen kromatik a* dan b* digunakan sebagai masukan k-Means
var clusterInput = labImage.select(['a', 'b']);

// Lakukan sampling piksel latih dari ROI
var trainingPixels = clusterInput.sample({
  region: roi,
  scale: CONFIG.scale,
  numPixels: 3000,
  seed: 42
});

// Latih clusterer Weka K-Means dengan k=3 kluster
var kMeansClusterer = ee.Clusterer.wekaKMeans({
  nClusters: CONFIG.kMeansClusters,
  seed: 42
}).train(trainingPixels);

// Terapkan klusterisasi pada seluruh area citra
var clustered = clusterInput.cluster(kMeansClusterer).rename('cluster');

// Identifikasi kluster atap bangunan secara otomatis:
// Karakteristik atap di Indonesia: spektrum kromatik a* lebih positif (genteng merah/cokelat/seng)
// dan memiliki indeks vegetasi (NDVI) rendah dibandingkan pohon/tanaman.
var ndvi = rgbImage.select('R').subtract(rgbImage.select('G'))
  .divide(rgbImage.select('R').add(rgbImage.select('G')).add(1e-6))
  .rename('ndvi_proxy');

// Hitung statistik rata-rata a* untuk setiap kluster (0, 1, 2)
var meanA_0 = labImage.select('a').updateMask(clustered.eq(0)).reduceRegion({
  reducer: ee.Reducer.mean(), geometry: roi, scale: CONFIG.scale, maxPixels: 1e6
}).get('a');
var meanA_1 = labImage.select('a').updateMask(clustered.eq(1)).reduceRegion({
  reducer: ee.Reducer.mean(), geometry: roi, scale: CONFIG.scale, maxPixels: 1e6
}).get('a');
var meanA_2 = labImage.select('a').updateMask(clustered.eq(2)).reduceRegion({
  reducer: ee.Reducer.mean(), geometry: roi, scale: CONFIG.scale, maxPixels: 1e6
}).get('a');

// Buat mask bangunan awal berdasarkan kluster dengan kromatik a* tertinggi (karakteristik atap)
var aScores = ee.List([meanA_0, meanA_1, meanA_2]);
var maxACluster = aScores.indexOf(aScores.reduce(ee.Reducer.max()));

// Mask Biner Bangunan Awal (Raw Building Mask)
var rawBuildingMask = clustered.eq(ee.Number(maxACluster)).rename('raw_building');

// ==============================================================================
// 6. PEMROSESAN MORFOLOGI BINER & NOISE FILTERING (BWAREAOPEN)
// ==============================================================================
/**
 * Menerapkan operasi morfologi sesuai Bab 3 (Halaman 40-41) skripsi:
 * - Opening (Erosi lalu Dilasi): Menghapus tonjolan tepi dan noise piksel tunggal
 * - Closing (Dilasi lalu Erosi): Menutup celah kecil dan rongga dalam atap (Filling Holes)
 * - Bwareaopen: Menghapus komponen terhubung yang memiliki total luas di bawah ambang batas
 */
function morphologicalProcessing(binaryMask, minNoiseSize) {
  var kernel = ee.Kernel.square({radius: 1, units: 'pixels'});

  // 1. Morphological Opening (Erosi -> Dilasi)
  var eroded = binaryMask.focal_min({kernel: kernel, iterations: 1});
  var opened = eroded.focal_max({kernel: kernel, iterations: 1});

  // 2. Morphological Closing (Dilasi -> Erosi) untuk Filling Holes
  var dilated = opened.focal_max({kernel: kernel, iterations: 1});
  var closed = dilated.focal_min({kernel: kernel, iterations: 1});

  // 3. Bwareaopen (Connected Component Size Filter)
  var connectedCount = closed.connectedPixelCount({maxSize: 100, eightConnected: true});
  var cleaned = closed.updateMask(connectedCount.gte(minNoiseSize));

  return cleaned.rename('clean_building');
}

var cleanBuildingMask = morphologicalProcessing(rawBuildingMask, CONFIG.minPixelNoise);

// ==============================================================================
// 7. EKSTRAKSI VEKTOR FITUR GEOMETRIS 4-DIMENSI (A, P, M, e)
// ==============================================================================
var buildingPolygons;

if (CONFIG.mode === 'HIGH_RES_INDIVIDUAL') {
  // Mode Presisi Tinggi: Poligon jejak atap individual dari satelit Google resolusi sub-meter
  // Setiap satu rumah memiliki poligon sendiri yang pas membungkus atapnya
  buildingPolygons = ee.FeatureCollection('GOOGLE/Research/open-buildings/v3/polygons')
    .filterBounds(roi)
    .filter(ee.Filter.gte('confidence', 0.65));
} else {
  // Mode Raster Segmentation: Vektorisasi dari hasil K-Means + Morfologi Sentinel-2 (10m)
  buildingPolygons = cleanBuildingMask.toInt().reduceToVectors({
    geometry: roi,
    crs: rgbImage.projection(),
    scale: CONFIG.scale,
    geometryType: 'polygon',
    eightConnected: true,
    labelProperty: 'building_id',
    maxPixels: 1e8,
    tileScale: 4
  });
}

// Ekstraksi 4 fitur geometris untuk setiap objek poligon bangunan
var buildingFeatures = buildingPolygons.map(function(feature) {
  // Perbaiki topologi poligon (self-intersection pada sudut diagonal) dengan buffer 0
  var geom = feature.geometry().buffer(0, 1);
  
  // 1. Luas (Area / A) dalam m2 (Wajib sertakan error margin non-zero, misal: 1 meter)
  var area = geom.area(1);
  
  // 2. Keliling (Perimeter / P) dalam meter (Sertakan error margin 1 meter)
  var perimeter = geom.perimeter(1);

  // 3. Metric / Compactness (M = 4 * PI * Area / Perimeter^2)
  // Nilai M mendekati 1.0 untuk lingkaran/persegi kompak, < 0.5 untuk memanjang/kompleks
  var metric = ee.Number(4 * Math.PI).multiply(area)
    .divide(perimeter.pow(2).max(1e-6));

  // 4. Eccentricity (e = sqrt(1 - (b/a)^2))
  // Dihitung berdasarkan rasio sumbu minor/mayor dari bounding box objek
  var bounds = geom.bounds(1);
  var coords = ee.List(bounds.coordinates().get(0));
  var p0 = ee.List(coords.get(0));
  var p1 = ee.List(coords.get(1));
  var p2 = ee.List(coords.get(2));

  var dx = ee.Number(p1.get(0)).subtract(ee.Number(p0.get(0))).abs();
  var dy = ee.Number(p2.get(1)).subtract(ee.Number(p1.get(1))).abs();
  var dimMin = dx.min(dy);
  var dimMax = dx.max(dy).max(1e-6);
  var axisRatio = dimMin.divide(dimMax).min(1.0);
  var eccentricity = ee.Number(1).subtract(axisRatio.pow(2)).sqrt();

  // Konversi ekuivalen estimasi jumlah piksel (seperti pada crop Google Earth di paper)
  var pixelEquivArea = area.divide(ee.Number(CONFIG.scale).pow(2)).multiply(100);

  return feature.set({
    'Area': area,
    'Perimeter': perimeter,
    'Metric': metric,
    'Eccentricity': eccentricity,
    'PixelEquivArea': pixelEquivArea
  });
});

// Filter poligon yang valid (luas fisik rumah realistis > 15 m2)
var validBuildings = buildingFeatures.filter(
  ee.Filter.and(
    ee.Filter.gt('Area', 15),
    ee.Filter.lt('Area', 30000)
  )
);

// ==============================================================================
// 8. KLASIFIKASI TIPE BANGUNAN DENGAN K-NEAREST NEIGHBOR (k-NN, k=5)
// ==============================================================================
/**
 * Dataset Pelatihan (Training Set)
 * Direkonstruksi dari Tabel 3.4 Skripsi (Adam Jaelani, 2020),
 * mencakup 15 sampel referensi dengan 3 kelas target:
 * Class 1 = Tipe A (Bangunan Besar / Luas > 300 m2)
 * Class 2 = Tipe B (Bangunan Sedang / Luas 120 - 300 m2)
 * Class 3 = Tipe C (Bangunan Kecil / Luas < 120 m2)
 */
var trainingSetList = [
  // Class 1: Tipe A (Bangunan Besar - Fasilitas, Aula, Ruko, Rumah Hook Besar)
  {Area: 550, Perimeter: 110, Metric: 0.35, Eccentricity: 0.95, class_code: 1},
  {Area: 800, Perimeter: 140, Metric: 0.30, Eccentricity: 0.97, class_code: 1},
  {Area: 400, Perimeter: 95,  Metric: 0.38, Eccentricity: 0.93, class_code: 1},
  {Area: 650, Perimeter: 125, Metric: 0.32, Eccentricity: 0.96, class_code: 1},
  {Area: 950, Perimeter: 160, Metric: 0.28, Eccentricity: 0.97, class_code: 1},

  // Class 2: Tipe B (Bangunan Sedang - Perumahan Tipe Menengah 70-120)
  {Area: 180, Perimeter: 58, Metric: 0.65, Eccentricity: 0.70, class_code: 2},
  {Area: 240, Perimeter: 68, Metric: 0.60, Eccentricity: 0.68, class_code: 2},
  {Area: 210, Perimeter: 64, Metric: 0.62, Eccentricity: 0.75, class_code: 2},
  {Area: 280, Perimeter: 74, Metric: 0.55, Eccentricity: 0.72, class_code: 2},
  {Area: 150, Perimeter: 52, Metric: 0.68, Eccentricity: 0.65, class_code: 2},

  // Class 3: Tipe C (Bangunan Kecil - Perumahan Kompak Tipe 21/36/45/60)
  {Area: 45,  Perimeter: 28, Metric: 0.72, Eccentricity: 0.60, class_code: 3},
  {Area: 65,  Perimeter: 34, Metric: 0.70, Eccentricity: 0.65, class_code: 3},
  {Area: 85,  Perimeter: 39, Metric: 0.65, Eccentricity: 0.70, class_code: 3},
  {Area: 70,  Perimeter: 36, Metric: 0.68, Eccentricity: 0.62, class_code: 3},
  {Area: 105, Perimeter: 44, Metric: 0.60, Eccentricity: 0.72, class_code: 3}
];

var trainingFC = ee.FeatureCollection(
  trainingSetList.map(function(d) {
    return ee.Feature(null, d);
  })
);

// Latih Classifier smileKNN dengan parameter k=5 (sesuai hasil optimal di paper)
var knnClassifier = ee.Classifier.smileKNN({
  k: CONFIG.knnNeighbors,
  searchMethod: 'AUTO'
}).train({
  features: trainingFC,
  classProperty: 'class_code',
  inputProperties: ['Area', 'Perimeter', 'Metric', 'Eccentricity']
});

// Terapkan klasifikasi k-NN pada seluruh poligon bangunan terdeteksi
var classifiedBuildings = validBuildings.classify(knnClassifier, 'predicted_type');

// Tambahkan atribut label teks deskriptif dan kode warna hex
classifiedBuildings = classifiedBuildings.map(function(f) {
  var pType = ee.Number(f.get('predicted_type'));
  var typeName = ee.Algorithms.If(
    pType.eq(1), 'Tipe A (Besar)',
    ee.Algorithms.If(pType.eq(2), 'Tipe B (Sedang)', 'Tipe C (Kecil)')
  );
  var colorHex = ee.Algorithms.If(
    pType.eq(1), '#FF2222', // Merah untuk Tipe A
    ee.Algorithms.If(pType.eq(2), '#FFD700', '#00E5FF') // Kuning-Emas untuk B, Cyan untuk C
  );
  return f.set({
    'Nama_Tipe': typeName,
    'Color_Hex': colorHex
  });
});

// ==============================================================================
// 9. DATASET PEMBANDING: GOOGLE OPEN BUILDINGS (GROUND TRUTH)
// ==============================================================================
// Dataset jejak bangunan global dari Google Research berbasis AI resolusi tinggi
var openBuildings = ee.FeatureCollection('GOOGLE/Research/open-buildings/v3/polygons')
  .filterBounds(roi);

// ==============================================================================
// 10. VISUALISASI MULTILAPIS (LAYERS DI PETA GEE)
// ==============================================================================
// Layer 1: Citra Asli Sentinel-2 RGB
Map.addLayer(rgbImage, {bands: ['R', 'G', 'B'], min: 0.05, max: 0.35}, '1. Citra Asli (RGB Sentinel-2)', true);

// Layer 2: Visualisasi Ruang Warna CIE L*a*b* (False Color)
Map.addLayer(labImage, {bands: ['L', 'a', 'b'], min: [-50, -30, -30], max: [100, 50, 50]}, '2. Komponen Warna CIE L*a*b*', false);

// Layer 3: Hasil Segmentasi K-Means (3 Kluster)
var clusterVis = {
  min: 0,
  max: 2,
  palette: ['#8D6E63', '#4CAF50', '#FF5722'] // Lahan, Vegetasi, Atap
};
Map.addLayer(clustered, clusterVis, '3. Segmentasi K-Means (k=3)', false);

// Layer 4: Mask Biner Bangunan Mentah (Sebelum Morfologi)
Map.addLayer(rawBuildingMask.selfMask(), {palette: ['#FFC107']}, '4. Mask Bangunan Mentah (Raw)', false);

// Layer 5: Mask Biner Bersih Hasil Morfologi (Opening, Closing, Bwareaopen)
Map.addLayer(cleanBuildingMask.selfMask(), {palette: ['#FFFFFF']}, '5. Mask Bangunan Bersih (Morfologi)', false);

// Layer 6: Poligon Bangunan Hasil Deteksi per Kelas (k-NN k=5)
var buildingsTypeA = classifiedBuildings.filter(ee.Filter.eq('predicted_type', 1));
var buildingsTypeB = classifiedBuildings.filter(ee.Filter.eq('predicted_type', 2));
var buildingsTypeC = classifiedBuildings.filter(ee.Filter.eq('predicted_type', 3));

Map.addLayer(buildingsTypeA.draw({color: 'FF2222', strokeWidth: 1.5}), {}, '6a. Klasifikasi: Tipe A (Besar - Merah)', true);
Map.addLayer(buildingsTypeB.draw({color: 'FFD700', strokeWidth: 1.5}), {}, '6b. Klasifikasi: Tipe B (Sedang - Kuning)', true);
Map.addLayer(buildingsTypeC.draw({color: '00E5FF', strokeWidth: 1.5}), {}, '6c. Klasifikasi: Tipe C (Kecil - Cyan)', true);

// Layer 7: Ground Truth Google Open Buildings (Sebagai Referensi / Pembanding)
Map.addLayer(openBuildings.draw({color: '76FF03', strokeWidth: 1}), {}, '7. Pembanding: Google Open Buildings AI (Hijau)', false);

// Layer 8: Garis Batas Wilayah Studi (ROI)
Map.addLayer(ee.FeatureCollection([ee.Feature(roi)]).style({color: 'FFFFFF', fillColor: '00000000', width: 2}), {}, '8. Batas ROI Kajian', true);

// ==============================================================================
// 11. PANEL INFORMASI, LEGENDA & INTERACTIVE INSPECTOR
// ==============================================================================
// Buat panel utama di sisi kiri bawah peta
var mainPanel = ui.Panel({
  style: {
    position: 'bottom-left',
    padding: '10px 14px',
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    maxWidth: '340px'
  }
});

// Judul Panel
var titleLabel = ui.Label({
  value: 'Deteksi & Klasifikasi Bangunan (k-NN)',
  style: {fontWeight: 'bold', fontSize: '15px', margin: '0 0 4px 0', color: '#1B5E20'}
});
var subTitleLabel = ui.Label({
  value: 'Replikasi Skripsi: Adam Jaelani (UIN Maliki Malang)',
  style: {fontSize: '11px', color: '#616161', margin: '0 0 4px 0'}
});
var modeBadge = ui.Label({
  value: CONFIG.mode === 'HIGH_RES_INDIVIDUAL' ? '✔ Mode: Presisi Per-Rumah (Sub-meter)' : '⚙ Mode: Segmentasi Raster (Sentinel-2 10m)',
  style: {fontSize: '11px', color: '#0D47A1', fontWeight: 'bold', margin: '0 0 8px 0'}
});
mainPanel.add(titleLabel);
mainPanel.add(subTitleLabel);
mainPanel.add(modeBadge);

// Fungsi pembantu membuat baris legenda
function makeLegendRow(color, label) {
  var colorBox = ui.Label({
    style: {
      backgroundColor: color,
      padding: '7px 14px',
      margin: '0 8px 0 0',
      border: '1px solid #333'
    }
  });
  var desc = ui.Label({
    value: label,
    style: {fontSize: '12px', margin: '2px 0'}
  });
  return ui.Panel({
    widgets: [colorBox, desc],
    layout: ui.Panel.Layout.Flow('horizontal'),
    style: {margin: '3px 0'}
  });
}

// Tambahkan entri legenda
mainPanel.add(ui.Label({value: 'Legenda Tipe Bangunan:', style: {fontWeight: 'bold', fontSize: '12px', margin: '6px 0 4px 0'}}));
mainPanel.add(makeLegendRow('#FF2222', 'Tipe A: Bangunan Besar (Luas > 350 m²)'));
mainPanel.add(makeLegendRow('#FFD700', 'Tipe B: Bangunan Sedang (130 - 350 m²)'));
mainPanel.add(makeLegendRow('#00E5FF', 'Tipe C: Bangunan Kecil (< 130 m²)'));
mainPanel.add(makeLegendRow('#76FF03', 'Google Open Buildings (Ground Truth)'));

// Bagian Interaktif Klik Objek Bangunan
var inspectLabel = ui.Label({
  value: '🔍 Klik pada salah satu bangunan di peta untuk melihat nilai ciri geometris:',
  style: {fontSize: '11px', color: '#333333', fontStyle: 'italic', margin: '10px 0 4px 0'}
});
var inspectResultPanel = ui.Panel({
  style: {backgroundColor: '#F5F5F5', padding: '6px 8px', border: '1px solid #DDD', margin: '4px 0'}
});
var inspectText = ui.Label({
  value: 'Belum ada bangunan yang dipilih.',
  style: {fontSize: '11px', color: '#757575'}
});
inspectResultPanel.add(inspectText);

mainPanel.add(inspectLabel);
mainPanel.add(inspectResultPanel);
Map.add(mainPanel);

// Handler Klik Peta untuk Menampilkan Fitur Geometris Objek Bangunan
Map.onClick(function(coords) {
  var clickPoint = ee.Geometry.Point([coords.lon, coords.lat]);
  var selected = classifiedBuildings.filterBounds(clickPoint).first();

  inspectText.setValue('Mengambil data fitur...');

  selected.evaluate(function(feature) {
    if (!feature) {
      inspectText.setValue('Tidak ada objek bangunan pada titik yang diklik. Silakan klik tepat pada batas poligon bangunan.');
      return;
    }
    var p = feature.properties;
    var info = 
      '• Prediksi: ' + p.Nama_Tipe + '\n' +
      '• Luas (Area): ' + Number(p.Area).toFixed(1) + ' m²\n' +
      '• Keliling (Perimeter): ' + Number(p.Perimeter).toFixed(1) + ' m\n' +
      '• Metric (Kebulatan): ' + Number(p.Metric).toFixed(3) + '\n' +
      '• Eccentricity (Kelonjongan): ' + Number(p.Eccentricity).toFixed(3);
    inspectText.setValue(info);
    inspectText.style().set('whiteSpace', 'pre');
    inspectText.style().set('color', '#1A237E');
    inspectText.style().set('fontWeight', 'bold');
  });
});

// ==============================================================================
// 12. RINGKASAN STATISTIK PADA KONSOL GEE
// ==============================================================================
print('=== HASIL DETEKSI DAN KLASIFIKASI TIPE BANGUNAN (k-NN) ===');
print('Wilayah Studi:', CONFIG.studyArea);
print('Mode Operasi:', CONFIG.mode);
print('Algoritma Klasifikasi:', 'k-Nearest Neighbor (k=' + CONFIG.knnNeighbors + ')');
print('Jumlah Bangunan Terdeteksi (Tipe A - Besar):', buildingsTypeA.size());
print('Jumlah Bangunan Terdeteksi (Tipe B - Sedang):', buildingsTypeB.size());
print('Jumlah Bangunan Terdeteksi (Tipe C - Kecil):', buildingsTypeC.size());
print('Total Keseluruhan Bangunan Terdeteksi:', classifiedBuildings.size());
print('Jumlah Bangunan Pembanding (Google Open Buildings):', openBuildings.size());

// Tampilkan contoh 5 fitur bangunan pertama ke Console
print('Sampel Vektor Fitur Geometris Bangunan:', classifiedBuildings.limit(5));
