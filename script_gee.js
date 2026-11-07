// =========================================================================
// TUGAS BESAR PENGOLAHAN CITRA DIGITAL (PCD) - VERSI 3 (V3 - ULTIMATE PROOF)
// DILENGKAPI:
// 1. SISTEM 3 FASE KRONOLOGIS MUTLAK:
//    - T0: BEFORE (Sebelum Terbakar Mei - Juli 2019)
//    - T1: PAS KEBAKARAN (Arang Segar Bebas Asap/Awan 25 Okt - 25 Des 2019)
//    - T2: AFTER (>5 Tahun Pasca-Bakar: Evaluasi Transisi 2024/2025)
// 2. DUAL INTERACTIVE TOOL:
//    - MODE A: 3 PETA BERDAMPINGAN SINKRON (TRIPLE-VIEW: BEFORE | SAAT BAKAR | AFTER)
//    - MODE B: TIRAI GESER 3 FASE (TRUE DUAL-WIPE SLIDER & DROPDOWN PEMILIH FASE)
// 3. CITRA PAS KEBAKARAN JERNIH (FRESH BURN SCAR WINDOW + PENETRASI SWIR B12)
// 4. MASKING AIR HITAM GAMBUT (NDWI < 0.05) & MORFOLOGI OPENING (R=1.5)
// 5. INSPEKTOR SPEKTRAL INTERAKTIF (KLIK PETA -> DIAGNOSIS BIOFISIK OTOMATIS)
// 6. K-MEANS CLUSTERING 3 KELAS MUTLAK (HIJAU PULIH, SEMAK COKLAT, PERKOTAAN)
// 7. STATISTIK KONSOL ANTI-LAG & EKSPOR DATA KE GOOGLE DRIVE
//
// TIM PENELITI (KELOMPOK 3B - D4 TEKNIK INFORMATIKA POLBAN):
// - Idotoho Reimon Simajuntak (241524047)
// - Ihsan Fauzi (241524048)
// - Muhammad Azzar MannalHadi (241524051)
// =========================================================================

// -------------------------------------------------------------------------
// 1. AREA STUDI & BATAS ADMINISTRASI KALIMANTAN TENGAH
// -------------------------------------------------------------------------
var kaltengProvince = ee.FeatureCollection('FAO/GAUL_SIMPLIFIED_500m/2015/level1')
  .filter(ee.Filter.eq('ADM1_NAME', 'Kalimantan Tengah'));

var kaltengDistricts = ee.FeatureCollection('FAO/GAUL_SIMPLIFIED_500m/2015/level2')
  .filter(ee.Filter.eq('ADM1_NAME', 'Kalimantan Tengah'));

var roi = kaltengProvince.geometry();

// Pusatkan peta ke area bekas kebakaran hebat antara Palangka Raya & Pulang Pisau
Map.centerObject(ee.Geometry.Point([114.02, -2.28]), 10);
Map.setOptions('HYBRID');

// -------------------------------------------------------------------------
// 2. PRE-PROCESSING: PENAPISAN KABUT ASAP & AWAN TINGKAT TINGGI (SCL + QA60 + AEROSOL)
// -------------------------------------------------------------------------
// a) Scene Classification Layer (SCL): membuang awan tebal (9), awan sedang (8),
//    cirrus tipis (10), dan bayangan awan (3) secara presisi 20 meter.
// b) Bitwise AND pada band QA60: eliminasi awan tebal (bit 10) & cirrus (bit 11).
// c) Ambang batas aerosol ketat (B1 < 1400 & B2 < 1650): membuang kabut asap tipis & embun.
// d) Temporal Median Filter: menambal piksel kosong dengan observasi bebas awan 100%.
var preprocessSmokeAndCloud = function (img) {
  var scl = img.select('SCL');
  var sclMask = scl.neq(3).and(scl.neq(8)).and(scl.neq(9)).and(scl.neq(10));

  var qa = img.select('QA60');
  var qaMask = qa.bitwiseAnd(1 << 10).eq(0).and(qa.bitwiseAnd(1 << 11).eq(0));

  var hazeMask = img.select('B1').lt(1400).and(img.select('B2').lt(1650));

  return img.updateMask(sclMask.and(qaMask).and(hazeMask))
    .select(['B2', 'B3', 'B4', 'B8', 'B11', 'B12']);
};

// -------------------------------------------------------------------------
// 3. AKUISISI CITRA 3 FASE KRONOLOGIS (BEFORE vs PAS KEBAKARAN vs AFTER)
// -------------------------------------------------------------------------

// A. T0 - BEFORE (Sebelum Kebakaran Hebat 2019: Mei - Juli 2019)
// Kondisi vegetasi hutan alami sebelum terbakar
var imgPre2019 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(roi)
  .filterDate('2019-05-01', '2019-07-31')
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 100))
  .map(preprocessSmokeAndCloud)
  .median()
  .clip(roi);

// B. T1_RAW - SAAT PUNCAK KARHUTLA MENTAH (September - Oktober 2019)
// Sebagai bukti kontras betapa tebalnya kabut asap bila tidak difilter
var imgFire2019Smoky = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(roi)
  .filterDate('2019-09-10', '2019-10-20')
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 60))
  .select(['B2', 'B3', 'B4', 'B8', 'B11', 'B12'])
  .median()
  .clip(roi);

// C. T1 - PAS KEBAKARAN BERSIH JERNIH (FRESH BURN SCAR GOLDEN WINDOW: 15 Okt - 28 Nov 2019)
// *** KUNCI JAWABAN AGAR CITRA PAS KEBAKARAN BEBAS AWAN & KABUT: ***
// 1. Ambil jendela waktu emas (15 Oktober - 28 November 2019):
//    Hujan pertama membilas kabut asap dari udara, dan belum masuk musim awan hujan lebat Desember!
// 2. Di tanah, arang luka bakar masih 100% segar, hitam pekat, belum tertutup semak!
// 3. Filter multi-layer SCL + Aerosol B1/B2 melenyapkan sisa kabut tipis -> Hasilnya hitam pekat 10 meter!
var imgDuringFireClean = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(roi)
  .filterDate('2019-10-15', '2019-11-28')
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 35))
  .map(preprocessSmokeAndCloud)
  .median()
  .clip(roi);

// D. T2 - AFTER (EVALUASI PASCA-BAKAR >5 TAHUN: 2024 - 2025)
// Kondisi mutakhir tutupan lahan setelah masa suksesi > 5 tahun
var imgCurrent = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(roi)
  .filterDate('2024-05-01', '2025-09-30')
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30))
  .map(preprocessSmokeAndCloud)
  .median()
  .clip(roi);

// -------------------------------------------------------------------------
// 4. MASKING BADAN AIR GAMBUT (NDWI) & SEGMENTASI LUKA BAKAR (dNBR)
// -------------------------------------------------------------------------
// Sungai rawa gambut (misal Sei Kahayan) berwarna hitam pekat karena tanin.
// Tanpa NDWI, air hitam bisa salah diidentifikasi sebagai arang kebakaran!
var ndwi2019 = imgPre2019.normalizedDifference(['B3', 'B8']).rename('NDWI');
var landMask = ndwi2019.lt(0.05); // True = Daratan, False = Badan Air

var nbrPre = imgPre2019.normalizedDifference(['B8', 'B12']);
var nbrPost = imgDuringFireClean.normalizedDifference(['B8', 'B12']);
var dNBR = nbrPre.subtract(nbrPost).rename('dNBR');

// Segmentasi Kasar Luka Bakar 2019 (dNBR > 0.20 pada daratan)
var rawBurn2019 = dNBR.gt(0.20).and(landMask).rename('Raw_Burn');

// -------------------------------------------------------------------------
// 5. OPERASI MORFOLOGI MATEMATIS (OPENING & CLOSING MULTI-SKALA)
// -------------------------------------------------------------------------
// Eliminasi bintik noise terisolasi (salt-and-pepper) dari atap seng dan tanah kering
var kernelR10 = ee.Kernel.circle({ radius: 1.0 });
var kernelR15 = ee.Kernel.circle({ radius: 1.5 }); // Kernel Optimal PCD
var kernelR25 = ee.Kernel.circle({ radius: 2.5 });

var burnOpeningR10 = rawBurn2019
  .focalMin({ kernel: kernelR10, iterations: 1 })
  .focalMax({ kernel: kernelR10, iterations: 1 })
  .and(landMask);

var openedBurnR15 = rawBurn2019
  .focalMin({ kernel: kernelR15, iterations: 1 })
  .focalMax({ kernel: kernelR15, iterations: 1 });

// Closing (focalMax lalu focalMin) untuk menambal lubang kecil di dalam luka bakar
var cleanBurn2019 = openedBurnR15
  .focalMax({ kernel: kernelR15, iterations: 1 })
  .focalMin({ kernel: kernelR15, iterations: 1 })
  .and(landMask)
  .rename('Clean_Burn');

var burnOpeningR25 = rawBurn2019
  .focalMin({ kernel: kernelR25, iterations: 1 })
  .focalMax({ kernel: kernelR25, iterations: 1 })
  .and(landMask);

var noiseEliminated = rawBurn2019.and(cleanBurn2019.not()).rename('Noise_Eliminated');

// -------------------------------------------------------------------------
// 6. EKSTRAKSI 4 INDEKS BIOFISIK SPEKTRAL & K-MEANS CLUSTERING (3 KELAS)
// -------------------------------------------------------------------------
var ndviNow = imgCurrent.normalizedDifference(['B8', 'B4']).rename('NDVI');
var ndmiNow = imgCurrent.normalizedDifference(['B8', 'B11']).rename('NDMI');
var bsiNow = imgCurrent.select('B11').add(imgCurrent.select('B4'))
  .subtract(imgCurrent.select('B8').add(imgCurrent.select('B2')))
  .divide(
    imgCurrent.select('B11').add(imgCurrent.select('B4'))
      .add(imgCurrent.select('B8').add(imgCurrent.select('B2')))
  ).rename('BSI');
var ndbiNow = imgCurrent.normalizedDifference(['B11', 'B8']).rename('NDBI');

var rawIndicesNow = ee.Image.cat([ndviNow, ndmiNow, bsiNow, ndbiNow]).updateMask(landMask);

// Min-Max Scaling (0-1)
var featuresNow = ee.Image.cat([
  ndviNow.unitScale(0, 0.85).clamp(0, 1).rename('NDVI_Norm'),
  ndmiNow.unitScale(-0.3, 0.5).clamp(0, 1).rename('NDMI_Norm'),
  bsiNow.unitScale(-0.4, 0.3).clamp(0, 1).rename('BSI_Norm'),
  ndbiNow.unitScale(-0.5, 0.3).clamp(0, 1).rename('NDBI_Norm')
]).updateMask(landMask);

// Sampling se-provinsi untuk K-Means
var sampleNow = featuresNow.sample({
  region: roi, scale: 300, numPixels: 4500, seed: 100, tileScale: 8
});

// Latih K-Means (K = 3)
var kmeansModel3 = ee.Clusterer.wekaKMeans(3).train(sampleNow);
var rawKMeansNow = featuresNow.cluster(kmeansModel3);

// Pengurutan Otomatis Berdasarkan Nilai NDVI Tertinggi -> Terendah:
// Kelas 0: NDVI Tertinggi -> Lahan Hijau / Kanopi Vegetasi Pulih
// Kelas 1: NDVI Sedang    -> Lahan Terbengkalai / Semak Kritis (Gambut Coklat Kering)
// Kelas 2: NDVI Terendah  -> Perkotaan / Lahan Terbangun / Kupasan Tanah Mati
var clusteredSample = sampleNow.cluster(kmeansModel3);
var centroidStats = clusteredSample.reduceColumns({
  reducer: ee.Reducer.mean().repeat(4).group({ groupField: 4, groupName: 'cluster' }),
  selectors: ['NDVI_Norm', 'NDMI_Norm', 'BSI_Norm', 'NDBI_Norm', 'cluster']
});
var centroidGroups = ee.List(centroidStats.get('groups'));

var clusterIds = centroidGroups.map(function (g) {
  return ee.Dictionary(g).getNumber('cluster');
});
var clusterMeanNdvi = centroidGroups.map(function (g) {
  return ee.List(ee.Dictionary(g).get('mean')).getNumber(0);
});

var idsSortedByNdviDesc = clusterIds.sort(clusterMeanNdvi).reverse();
var targetLabels = ee.List([0, 1, 2]);

var mapClassNowRaw = rawKMeansNow.remap(idsSortedByNdviDesc, targetLabels, 1).rename('Class_Now_Raw');

// Haluskan klaster dengan Morfologi Majority Filter (3x3 mode)
var mapClassNow = mapClassNowRaw.focalMode({ kernel: ee.Kernel.square(1), iterations: 1 })
  .updateMask(landMask)
  .rename('Class_3_Now');

// -------------------------------------------------------------------------
// 7. NASIB LAHAN PADA AREA BEKAS KEBAKARAN (POST-FIRE TRAJECTORY)
// -------------------------------------------------------------------------
// 1 = Pulih Jadi Lahan Hijau Lembab (Hijau Terang #00E676)
// 2 = Semak Kritis Terbengkalai (Oranye #FF9100)
// 3 = Alih Fungsi Perkotaan / Kupasan Mati (Merah #FF1744)
var burnedDestiny3 = mapClassNow.add(1).updateMask(cleanBurn2019).rename('Burned_Destiny_3');

// -------------------------------------------------------------------------
// 8. LAYER PETA UTAMA
// -------------------------------------------------------------------------
var adminBoundaryVis = ee.Image().byte().paint({
  featureCollection: kaltengDistricts, color: 1, width: 2
});

Map.addLayer(imgPre2019, { bands: ['B4', 'B3', 'B2'], min: 200, max: 2200 },
  '1A. [T0: BEFORE 2019] Kondisi Alami Sebelum Karhutla (RGB)', false);

Map.addLayer(imgFire2019Smoky, { bands: ['B4', 'B3', 'B2'], min: 400, max: 3200 },
  '1B. [SAAT KEBAKARAN MENTAH] Puncak Asap Tebal Tanpa Filter (RGB)', false);

Map.addLayer(imgDuringFireClean, { bands: ['B4', 'B3', 'B2'], min: 200, max: 2200 },
  '1C. [T1: PAS KEBAKARAN BERSIH] Arang Segar Pasca-Hujan Bebas Asap (RGB)', false);

Map.addLayer(imgDuringFireClean, { bands: ['B12', 'B8', 'B4'], min: 300, max: 3500 },
  '1D. [T1: BUKTI SWIR B12] Penetrasi Gelombang SWIR: Arang Hitam Kontras Tinggi!', false);

Map.addLayer(imgCurrent, { bands: ['B4', 'B3', 'B2'], min: 200, max: 2200 },
  '1E. [T2: AFTER RGB BIASA] Tampak Sama-Sama Hijau di Mata Manusia', false);

Map.addLayer(imgCurrent, { bands: ['B11', 'B8', 'B4'], min: 300, max: 3500 },
  '1F. [T2: BUKTI SWIR SEKARANG] Hijau Neon vs Coklat Semak vs Magenta Kota', true);

// Morfologi
Map.addLayer(rawBurn2019.selfMask(), { palette: ['#FFA500'] },
  '2A. [LUKA BAKAR KASAR] dNBR Mentah (Bintik Noise Salt-and-Pepper)', false);

Map.addLayer(noiseEliminated.selfMask(), { palette: ['#00FFFF'] },
  '2B. [BUKTI MORFOLOGI] Bintik Noise Palsu yang Dibuang Opening (Cyan)', false);

Map.addLayer(cleanBurn2019.selfMask(), { palette: ['#FF0000'] },
  '2C. [LUKA BAKAR BERSIH 2019] Poligon Luka Bakar Morfologi Optimal (R=1.5)', false);

// Klasifikasi & Nasib Lahan
Map.addLayer(mapClassNow, {
  min: 0, max: 2, palette: ['#1B8A2A', '#D97706', '#DC2626']
}, '3A. [KLASIFIKASI 3 KELAS SE-KALTENG] 1. Hijau, 2. Semak Coklat, 3. Perkotaan', false);

Map.addLayer(burnedDestiny3, {
  min: 1, max: 3, palette: ['#00E676', '#FF9100', '#FF1744']
}, '3B. [HIGHLIGHT UTAMA] Nasib Bekas Karhutla 2019 (>5 Tahun)', true);

Map.addLayer(adminBoundaryVis, { palette: ['#FFFFFF'] }, '4. Batas Kabupaten/Kota Se-Kalimantan Tengah', true);

// -------------------------------------------------------------------------
// 9. BUKTI STATISTIK SPEKTRAL KE CONSOLE
// -------------------------------------------------------------------------
var proofSample = rawIndicesNow.addBands(mapClassNow).sample({
  region: roi, scale: 300, numPixels: 4500, seed: 42, tileScale: 8
});

var groupedMeans = proofSample.reduceColumns({
  reducer: ee.Reducer.mean().repeat(4).group({ groupField: 4, groupName: 'Class_3_Now' }),
  selectors: ['NDVI', 'NDMI', 'BSI', 'NDBI', 'Class_3_Now']
});

var classNamesMap = ee.Dictionary({
  '0': '1. Lahan Hijau (Kanopi Lembab)',
  '1': '2. Terbengkalai (Semak Coklat Kering)',
  '2': '3. Perkotaan / Terbangun / Kupasan'
});

var groupsList = ee.List(groupedMeans.get('groups'));
var spectralProofTable = ee.FeatureCollection(groupsList.map(function (item) {
  var d = ee.Dictionary(item);
  var clsStr = ee.Number(d.get('Class_3_Now')).format('%d');
  var means = ee.List(d.get('mean'));
  return ee.Feature(null, {
    'Kelas': classNamesMap.get(clsStr),
    '1_NDVI_(Klorofil)': means.getNumber(0),
    '2_NDMI_(Kelembaban_Tajuk)': means.getNumber(1),
    '3_BSI_(Tanah_Coklat_Terbuka)': means.getNumber(2),
    '4_NDBI_(Bangunan_Perkotaan)': means.getNumber(3)
  });
}));

var spectralChart = ui.Chart.feature.byFeature({
  features: spectralProofTable,
  xProperty: 'Kelas',
  yProperties: [
    '1_NDVI_(Klorofil)',
    '2_NDMI_(Kelembaban_Tajuk)',
    '3_BSI_(Tanah_Coklat_Terbuka)',
    '4_NDBI_(Bangunan_Perkotaan)'
  ]
}).setChartType('ColumnChart')
  .setOptions({
    title: 'BUKTI PEMISAHAN KLASTER K-MEANS: Profil Spektral 3 Kelas Utama',
    hAxis: { title: 'Kelas Tutupan Lahan' },
    vAxis: { title: 'Rata-rata Indeks Spektral (-1 s/d +1)' },
    colors: ['#2E7D32', '#0288D1', '#D97706', '#C62828'],
    bar: { groupWidth: '65%' },
    legend: { position: 'top' }
  });

print('========================================================================');
print('🔬 BUKTI 1: PROFIL SPEKTRAL MULTI-INDEKS (PEMISAHAN 3 KELAS)');
print('========================================================================');
print(spectralChart);
print('Tabel Rata-rata Nilai Spektral:', spectralProofTable);

// Luas Hektar
var haImg = ee.Image.pixelArea().divide(10000);
var combinedStatsImage = ee.Image.cat([
  rawBurn2019.multiply(haImg).rename('A1_Luka_Bakar_Kasar_Ha'),
  burnOpeningR10.multiply(haImg).rename('A2_Morfologi_R1_0_Ha'),
  cleanBurn2019.multiply(haImg).rename('A3_Morfologi_Optimal_R1_5_Ha'),
  burnOpeningR25.multiply(haImg).rename('A4_Morfologi_R2_5_Ha'),
  noiseEliminated.multiply(haImg).rename('A5_Noise_Dieliminasi_Ha'),
  burnedDestiny3.eq(1).multiply(haImg).rename('B1_Pulih_Lahan_Hijau_Ha'),
  burnedDestiny3.eq(2).multiply(haImg).rename('B2_Terbengkalai_Semak_Coklat_Ha'),
  burnedDestiny3.eq(3).multiply(haImg).rename('B3_Perkotaan_Terbangun_Kupasan_Ha')
]);

var summaryProvinsi = combinedStatsImage.reduceRegion({
  reducer: ee.Reducer.sum(),
  geometry: roi,
  scale: 250,
  tileScale: 8,
  bestEffort: true,
  maxPixels: 1e9
});

var totalCleanBurnHa = ee.Number(summaryProvinsi.get('A3_Morfologi_Optimal_R1_5_Ha')).max(1);
var pctHijau = ee.Number(summaryProvinsi.get('B1_Pulih_Lahan_Hijau_Ha')).divide(totalCleanBurnHa).multiply(100);
var pctSemak = ee.Number(summaryProvinsi.get('B2_Terbengkalai_Semak_Coklat_Ha')).divide(totalCleanBurnHa).multiply(100);
var pctKota = ee.Number(summaryProvinsi.get('B3_Perkotaan_Terbangun_Kupasan_Ha')).divide(totalCleanBurnHa).multiply(100);

var pieTable = ee.FeatureCollection([
  ee.Feature(null, { 'Kategori': '1. Lahan Hijau (Pulih)', 'Persentase': pctHijau }),
  ee.Feature(null, { 'Kategori': '2. Semak Gambut Coklat (Terbengkalai)', 'Persentase': pctSemak }),
  ee.Feature(null, { 'Kategori': '3. Perkotaan / Terbangun / Kupasan', 'Persentase': pctKota })
]);

var pieChart = ui.Chart.feature.byFeature({
  features: pieTable,
  xProperty: 'Kategori',
  yProperties: ['Persentase']
}).setChartType('PieChart')
  .setOptions({
    title: 'PROPORSI NASIB LAHAN BEKAS LUKA BAKAR 2019 (>5 TAHUN)',
    colors: ['#00E676', '#FF9100', '#FF1744'],
    pieHole: 0.38
  });

print('========================================================================');
print('📊 BUKTI 2: PIE CHART & PERSENTASE TRANSISI LAHAN PASCA-BAKAR');
print('========================================================================');
print(pieChart);
print('Ringkasan Luas Hektar Provinsi:', summaryProvinsi);

// -------------------------------------------------------------------------
// 10. EKSPOR DATA (.TIF & .CSV) UNTUK TUGAS "GET DATA" DOSEN
// -------------------------------------------------------------------------
// A. Ekspor Sampel Area Studi 10x10 km (.TIF) untuk Pemrosesan Lokal di Python (OpenCV/NumPy)
var sampleAreaRoi = ee.Geometry.Point([114.02, -2.28]).buffer(5000).bounds(); // 10 km x 10 km

// 1. Ekspor Citra Before 2019 (Warna Alami RGB Hutan Hijau)
Export.image.toDrive({
  image: imgPre2019.select(['B4', 'B3', 'B2']).clip(sampleAreaRoi),
  description: 'Citra_Sentinel2_Kalteng_2019_Before',
  folder: 'PCD_PraTubes',
  scale: 10,
  region: sampleAreaRoi,
  maxPixels: 1e8,
  fileFormat: 'GeoTIFF'
});

// 2. Ekspor Citra Pas Kebakaran 2019 (Warna Alami RGB Coklat Arang Bersih Bebas Asap)
Export.image.toDrive({
  image: imgDuringFireClean.select(['B4', 'B3', 'B2']).clip(sampleAreaRoi),
  description: 'Citra_Sentinel2_Kalteng_2019_PasBakar',
  folder: 'PCD_PraTubes',
  scale: 10,
  region: sampleAreaRoi,
  maxPixels: 1e8,
  fileFormat: 'GeoTIFF'
});

// 3. Ekspor Citra Multi-Band Lengkap (B2, B3, B4, B8, B11, B12, dNBR, Masker)
var exportSampleImage = imgDuringFireClean.select(['B2', 'B3', 'B4', 'B8', 'B11', 'B12'])
  .addBands(dNBR)
  .addBands(cleanBurn2019)
  .clip(sampleAreaRoi);

Export.image.toDrive({
  image: exportSampleImage,
  description: 'Sampel_Karhutla_Kalteng_10km',
  folder: 'PCD_PraTubes',
  scale: 10,
  region: sampleAreaRoi,
  maxPixels: 1e8,
  fileFormat: 'GeoTIFF'
});

// B. Ekspor Rekapitulasi Statistik per Kabupaten (.CSV)
var perKabupatenStats = combinedStatsImage.reduceRegions({
  collection: kaltengDistricts.select(['ADM2_NAME', 'ADM1_NAME']),
  reducer: ee.Reducer.sum(),
  scale: 300,
  tileScale: 8
});

Export.table.toDrive({
  collection: perKabupatenStats,
  description: 'Rekapitulasi_Karhutla_Kalteng_Per_Kabupaten',
  folder: 'PCD_PraTubes',
  fileFormat: 'CSV'
});

// C. Data Ground-Truth Validasi: Titik Api NASA FIRMS 2019 (CSV)
var firmsHotspots2019 = ee.FeatureCollection('FIRMS')
  .filterBounds(sampleAreaRoi)
  .filterDate('2019-08-01', '2019-11-30')
  .filter(ee.Filter.gte('confidence', 70));

Export.table.toDrive({
  collection: firmsHotspots2019.limit(3000),
  description: 'GroundTruth_Hotspot_NASA_FIRMS_2019',
  folder: 'PCD_PraTubes',
  fileFormat: 'CSV'
});

// -------------------------------------------------------------------------
// 11. UI CONTROL PANEL DENGAN SISTEM TIRAI 3 FASE
// -------------------------------------------------------------------------
var mainPanel = ui.Panel({
  style: {
    position: 'top-left',
    padding: '10px 14px',
    backgroundColor: 'rgba(255, 255, 255, 0.96)',
    border: '1px solid #333',
    maxWidth: '380px'
  }
});

mainPanel.add(ui.Label({
  value: '🛰️ SISTEM BUKTI 3 FASE PCD (V3)',
  style: { fontWeight: 'bold', fontSize: '13px', color: '#1B5E20', margin: '0 0 2px 0' }
}));

mainPanel.add(ui.Label({
  value: 'Before (2019) ➔ Pas Kebakaran (2019) ➔ After (>5 Thn)',
  style: { fontSize: '10px', color: '#444', fontWeight: 'bold', margin: '0 0 8px 0' }
}));

// A. Tombol Loncat Lokasi Ground Truth
mainPanel.add(ui.Label({
  value: '📍 1. Loncat ke Lokasi Ground-Truth:',
  style: { fontWeight: 'bold', fontSize: '11px', color: '#222', margin: '4px 0 2px 0' }
}));

var btnGrid1 = ui.Panel({ layout: ui.Panel.Layout.Flow('horizontal') });
var btnGrid2 = ui.Panel({ layout: ui.Panel.Layout.Flow('horizontal') });

btnGrid1.add(ui.Button({
  label: '🌲 Sabangau (Pulih Hijau)',
  style: { fontSize: '10px', margin: '2px 4px 2px 0' },
  onClick: function () { Map.setCenter(113.82, -2.35, 12); }
}));

btnGrid1.add(ui.Button({
  label: '🍂 Eks-PLG (Semak Terbengkalai)',
  style: { fontSize: '10px', margin: '2px 0 2px 0' },
  onClick: function () { Map.setCenter(114.18, -2.32, 12); }
}));

btnGrid2.add(ui.Button({
  label: '🏙️ Palangka Raya (Kupasan/Kota)',
  style: { fontSize: '10px', margin: '2px 4px 2px 0' },
  onClick: function () { Map.setCenter(113.92, -2.21, 13); }
}));

btnGrid2.add(ui.Button({
  label: '🌊 Sei Kahayan (Air Hitam NDWI)',
  style: { fontSize: '10px', margin: '2px 0 2px 0' },
  onClick: function () { Map.setCenter(114.05, -2.25, 13); }
}));

mainPanel.add(btnGrid1);
mainPanel.add(btnGrid2);

// B. SISTEM TIRAI 3 FASE & 3 PETA BERDAMPINGAN
mainPanel.add(ui.Label({
  value: '🪟 2. Alat Pembuktian Visual 3 Fase:',
  style: { fontWeight: 'bold', fontSize: '11px', color: '#222', margin: '8px 0 2px 0' }
}));

// 1. Tombol Mode 3 Peta Berdampingan Sekaligus (Triple Synchronized Maps)
var btnTripleView = ui.Button({
  label: '🎬 Buka 3 Peta Sinkron Sekaligus (Before | Saat Bakar | After)',
  style: { fontSize: '10px', fontWeight: 'bold', color: '#B71C1C', margin: '2px 0 4px 0' },
  onClick: function () {
    var mapT0 = ui.Map();
    mapT0.setCenter(114.02, -2.28, 11);
    mapT0.setOptions('HYBRID');
    mapT0.addLayer(imgPre2019, { bands: ['B4', 'B3', 'B2'], min: 200, max: 2200 }, 'T0: Before 2019 (RGB)');
    mapT0.add(ui.Label({
      value: '🌲 1. BEFORE (Mei-Juli 2019)\nHutan/Vegetasi Alami',
      style: { position: 'top-left', fontSize: '11px', fontWeight: 'bold', backgroundColor: 'rgba(255,255,255,0.9)', padding: '4px' }
    }));

    var mapT1 = ui.Map();
    mapT1.setOptions('HYBRID');
    mapT1.addLayer(imgDuringFireClean, { bands: ['B4', 'B3', 'B2'], min: 150, max: 1800 }, 'T1: Pasca-Bakar RGB Hitam Arang', true);
    mapT1.addLayer(cleanBurn2019.selfMask(), { palette: ['#FF0000'] }, 'Deliniasi Luka Bakar 2019', false);
    mapT1.addLayer(imgDuringFireClean, { bands: ['B12', 'B8', 'B4'], min: 200, max: 2800 }, 'T1: Bukti SWIR Arang', false);
    mapT1.add(ui.Label({
      value: '🔥 2. PAS KEBAKARAN (Nov-Des 2019)\nHangus Hitam Arang Nyata Bebas Asap (Bukti Terbakar!)',
      style: { position: 'top-center', fontSize: '11px', fontWeight: 'bold', color: '#B71C1C', backgroundColor: 'rgba(255,255,255,0.9)', padding: '4px' }
    }));

    var mapT2 = ui.Map();
    mapT2.setOptions('HYBRID');
    mapT2.addLayer(imgCurrent, { bands: ['B11', 'B8', 'B4'], min: 300, max: 3500 }, 'T2: SWIR 2024/2025');
    mapT2.addLayer(burnedDestiny3, { min: 1, max: 3, palette: ['#00E676', '#FF9100', '#FF1744'] }, 'Nasib Pasca-Bakar', true);
    mapT2.add(ui.Label({
      value: '🌱 3. AFTER (>5 Tahun 2024/2025)\nNasib Transisi (Hijau vs Semak Coklat)',
      style: { position: 'top-right', fontSize: '11px', fontWeight: 'bold', color: '#1B5E20', backgroundColor: 'rgba(255,255,255,0.9)', padding: '4px' }
    }));

    var linker = ui.Map.Linker([mapT0, mapT1, mapT2]);

    var rightSplit = ui.SplitPanel({
      firstPanel: mapT1,
      secondPanel: mapT2,
      orientation: 'horizontal',
      wipe: false,
      style: { stretch: 'both' }
    });

    var tripleSplit = ui.SplitPanel({
      firstPanel: mapT0,
      secondPanel: rightSplit,
      orientation: 'horizontal',
      wipe: false,
      style: { stretch: 'both' }
    });

    var closeBtn = ui.Button({
      label: '✖️ Kembali ke Mode Normal',
      style: { position: 'bottom-center', fontSize: '11px', fontWeight: 'bold' },
      onClick: function () {
        ui.root.clear();
        ui.root.add(Map);
        Map.add(mainPanel);
      }
    });

    mapT1.add(closeBtn);
    ui.root.clear();
    ui.root.add(tripleSplit);
  }
});
mainPanel.add(btnTripleView);

// 2. SISTEM MASTER TIRAI GESER INTERAKTIF (SWIPE SUITE TERPADU)
var openMasterSwipe = function () {
  var leftMap = ui.Map();
  leftMap.setCenter(114.02, -2.28, 11);
  leftMap.setOptions('HYBRID');

  var rightMap = ui.Map();
  rightMap.setOptions('HYBRID');

  var linker = ui.Map.Linker([leftMap, rightMap]);

  var split = ui.SplitPanel({
    firstPanel: linker.get(0),
    secondPanel: linker.get(1),
    orientation: 'horizontal',
    wipe: true,
    style: { stretch: 'both' }
  });

  var labelLeft = ui.Label({
    value: '',
    style: { position: 'top-left', fontSize: '11px', fontWeight: 'bold', backgroundColor: 'rgba(255,255,255,0.92)', padding: '5px' }
  });
  var labelRight = ui.Label({
    value: '',
    style: { position: 'top-right', fontSize: '11px', fontWeight: 'bold', backgroundColor: 'rgba(255,255,255,0.92)', padding: '5px' }
  });

  leftMap.add(labelLeft);
  rightMap.add(labelRight);

  var setMode = function (mode) {
    leftMap.layers().reset();
    rightMap.layers().reset();

    if (mode === 1) {
      // 1. Before vs Pas Bakar (Warna Alami)
      leftMap.addLayer(imgPre2019, { bands: ['B4', 'B3', 'B2'], min: 150, max: 1800 }, 'Before 2019 (RGB)');
      labelLeft.setValue('🌲 KIRI: 1. Sebelum Terbakar 2019 (Hutan Hijau Alami)');

      rightMap.addLayer(imgDuringFireClean, { bands: ['B4', 'B3', 'B2'], min: 150, max: 1800 }, 'Pas Kebakaran (Hitam Gosong)');
      labelRight.setValue('🔥 KANAN: 2. Pas Kebakaran (HITAM GOSONG ARANG NYATA)');
    } else if (mode === 2) {
      // 2. Pas Bakar vs After
      leftMap.addLayer(imgDuringFireClean, { bands: ['B4', 'B3', 'B2'], min: 150, max: 1800 }, 'Pas Kebakaran (Hitam Gosong)');
      labelLeft.setValue('🔥 KIRI: 2. Pas Kebakaran (Hitam Gosong Arang)');

      rightMap.addLayer(burnedDestiny3, { min: 1, max: 3, palette: ['#00E676', '#FF9100', '#FF1744'] }, 'Nasib Pasca-Bakar');
      labelRight.setValue('🌱 KANAN: 3. Kondisi Sekarang (>5 Thn Hijau vs Semak Coklat)');
    } else if (mode === 3) {
      // 3. Before vs After
      leftMap.addLayer(imgPre2019, { bands: ['B4', 'B3', 'B2'], min: 150, max: 1800 }, 'Before 2019 (RGB)');
      labelLeft.setValue('🌲 KIRI: 1. Sebelum Terbakar 2019 (Hutan Hijau Alami)');

      rightMap.addLayer(burnedDestiny3, { min: 1, max: 3, palette: ['#00E676', '#FF9100', '#FF1744'] }, 'Nasib Pasca-Bakar');
      labelRight.setValue('🌱 KANAN: 3. Kondisi Sekarang (>5 Thn Transisi Kumulatif)');
    } else if (mode === 4) {
      // 4. RGB Alami vs Highlight Merah Deliniasi PCD
      leftMap.addLayer(imgDuringFireClean, { bands: ['B4', 'B3', 'B2'], min: 150, max: 1800 }, 'RGB Hitam Gosong');
      labelLeft.setValue('👁️ KIRI: RGB Alami (Hitam Gosong Arang Nyata)');

      rightMap.addLayer(imgDuringFireClean, { bands: ['B4', 'B3', 'B2'], min: 150, max: 1800 }, 'RGB Background');
      rightMap.addLayer(cleanBurn2019.selfMask(), { palette: ['#FF0000'] }, 'Luka Bakar dNBR (Merah)');
      labelRight.setValue('🎯 KANAN: Highlight Merah (Deliniasi dNBR + Morfologi PCD)');
    } else if (mode === 5) {
      // 5. RGB Alami vs False Color SWIR B12-B8-B4
      leftMap.addLayer(imgDuringFireClean, { bands: ['B4', 'B3', 'B2'], min: 150, max: 1800 }, 'RGB Alami');
      labelLeft.setValue('👁️ KIRI: Spektrum Tampak Mata Manusia (B4-B3-B2)');

      rightMap.addLayer(imgDuringFireClean, { bands: ['B12', 'B8', 'B4'], min: 200, max: 2800 }, 'SWIR B12-B8-B4');
      labelRight.setValue('🔬 KANAN: False Color SWIR Penetrasi Inframerah (B12-B8-B4)');
    }
  };

  // Panel navigasi fase di bagian atas tengah layar tirai
  var navBar = ui.Panel({
    style: {
      position: 'top-center',
      padding: '6px 12px',
      backgroundColor: 'rgba(255, 255, 255, 0.96)',
      border: '1px solid #222'
    }
  });

  var row1 = ui.Panel({ layout: ui.Panel.Layout.Flow('horizontal') });
  row1.add(ui.Label({ value: '1. PILIH FASE:', style: { fontWeight: 'bold', fontSize: '11px', margin: '4px 6px 4px 0' } }));
  row1.add(ui.Button({ label: '🔥 1. Before vs Pas Bakar', style: { fontSize: '10px', margin: '0 2px' }, onClick: function () { setMode(1); } }));
  row1.add(ui.Button({ label: '🌱 2. Pas Bakar vs After', style: { fontSize: '10px', margin: '0 2px' }, onClick: function () { setMode(2); } }));
  row1.add(ui.Button({ label: '⏳ 3. Before vs After', style: { fontSize: '10px', margin: '0 2px' }, onClick: function () { setMode(3); } }));
  row1.add(ui.Button({
    label: '✖️ Kembali ke Menu Utama',
    style: { fontSize: '10px', fontWeight: 'bold', color: '#B71C1C', margin: '0 0 0 6px' },
    onClick: function () {
      ui.root.clear();
      ui.root.add(Map);
      Map.add(mainPanel);
    }
  }));

  var row2 = ui.Panel({ layout: ui.Panel.Layout.Flow('horizontal'), style: { margin: '4px 0 0 0' } });
  row2.add(ui.Label({ value: '2. PEMBUKTIAN KHUSUS:', style: { fontWeight: 'bold', fontSize: '11px', margin: '4px 6px 4px 0' } }));
  row2.add(ui.Button({ label: '🎯 4. RGB vs Highlight Merah', style: { fontSize: '10px', margin: '0 3px', color: '#C62828' }, onClick: function () { setMode(4); } }));
  row2.add(ui.Button({ label: '🔬 5. RGB vs False Color SWIR', style: { fontSize: '10px', margin: '0 3px', color: '#6A1B9A' }, onClick: function () { setMode(5); } }));

  navBar.add(row1);
  navBar.add(row2);

  // Inisialisasi default ke Mode 1 (Before vs Pas Bakar)
  setMode(1);

  leftMap.add(navBar);
  ui.root.clear();
  ui.root.add(split);
};

// Tombol Tunggal Buka Tirai Geser di Menu Utama (Clean & Rapi)
mainPanel.add(ui.Button({
  label: '🎚️ Buka Tirai Geser Interaktif (Master Swipe Suite)',
  style: { fontSize: '11px', fontWeight: 'bold', color: '#0D47A1', margin: '2px 0 6px 0' },
  onClick: openMasterSwipe
}));

// C. Inspektor Piksel Otomatis
mainPanel.add(ui.Label({
  value: '🎯 3. Inspektor Interaktif (Klik Peta Di Mana Saja):',
  style: { fontWeight: 'bold', fontSize: '11px', color: '#222', margin: '6px 0 2px 0' }
}));

var inspectorBox = ui.Panel({
  style: {
    backgroundColor: '#F3F4F6',
    border: '1px solid #D1D5DB',
    padding: '8px',
    margin: '4px 0'
  }
});
var inspectorLabel = ui.Label({
  value: 'Klik salah satu piksel di peta untuk melihat diagnosis 3 fase spektral otomatis...',
  style: { fontSize: '10px', color: '#4B5563' }
});
inspectorBox.add(inspectorLabel);
mainPanel.add(inspectorBox);

Map.onClick(function (coords) {
  inspectorLabel.setValue('Sedang mengekstraksi spektral piksel (' + coords.lon.toFixed(3) + ', ' + coords.lat.toFixed(3) + ')...');

  var pt = ee.Geometry.Point([coords.lon, coords.lat]);
  var samplePoint = rawIndicesNow.addBands([dNBR, ndwi2019, mapClassNow, cleanBurn2019])
    .reduceRegion({
      reducer: ee.Reducer.first(),
      geometry: pt,
      scale: 20
    });

  samplePoint.evaluate(function (val) {
    if (!val || val.NDVI === undefined || val.NDVI === null) {
      inspectorLabel.setValue('Titik berada di luar area daratan atau bernilai masked/kosong.');
      return;
    }

    var ndvi = val.NDVI.toFixed(2);
    var ndmi = val.NDMI.toFixed(2);
    var bsi = val.BSI.toFixed(2);
    var ndbi = val.NDBI.toFixed(2);
    var dnbr = val.dNBR ? val.dNBR.toFixed(2) : '-';
    var isBurned = val.Clean_Burn === 1;
    var cls = val.Class_3_Now;

    var diagnosis = '';
    if (val.NDWI > 0.05) {
      diagnosis = '🌊 BADAN AIR / SUNGAI GAMBUT HITAM: Tereliminasi oleh NDWI (>0.05). Bukan luka bakar!';
    } else if (isBurned) {
      if (cls === 0) {
        diagnosis = '🌲 BEKAS TERBAKAR (dNBR ' + dnbr + ') -> PULIH JADI LAHAN HIJAU: Kanopi lembab berair (NDMI ' + ndmi + '), NDVI ' + ndvi + '.';
      } else if (cls === 1) {
        diagnosis = '🍂 BEKAS TERBAKAR (dNBR ' + dnbr + ') -> SEMAK TERBENGKALAI / GAMBUT COKLAT: Walau tampak hijau di RGB biasa, terbukti KERING secara biofisik (NDMI ' + ndmi + ', BSI ' + bsi + '). Rawan terbakar ulang!';
      } else {
        diagnosis = '🏙️ BEKAS TERBAKAR (dNBR ' + dnbr + ') -> ALIH FUNGSI / KUPASAN MATI: Dominasi pantulan SWIR & tanah keras (BSI ' + bsi + ', NDBI ' + ndbi + ').';
      }
    } else {
      if (cls === 0) {
        diagnosis = '🌿 VEGETASI ALAMI TIDAK TERBAKAR: Kanopi stabil (dNBR ' + dnbr + ' rendah).';
      } else if (cls === 1) {
        diagnosis = '🌾 SEMAK / LAHAN TERBUKA TIDAK TERBAKAR: NDMI (' + ndmi + '), BSI (' + bsi + ').';
      } else {
        diagnosis = '🏢 KAWASAN TERBANGUN / TANAH MATI: NDBI (' + ndbi + ').';
      }
    }

    inspectorBox.clear();
    inspectorBox.add(ui.Label({
      value: '📍 Koordinat: ' + coords.lon.toFixed(4) + ', ' + coords.lat.toFixed(4),
      style: { fontSize: '10px', fontWeight: 'bold', color: '#111' }
    }));
    inspectorBox.add(ui.Label({
      value: '• dNBR (2019): ' + dnbr + ' | NDVI: ' + ndvi + ' | NDMI: ' + ndmi + ' | BSI: ' + bsi,
      style: { fontSize: '10px', color: '#333' }
    }));
    inspectorBox.add(ui.Label({
      value: diagnosis,
      style: { fontSize: '10px', fontWeight: 'bold', color: '#004D40', margin: '4px 0 0 0' }
    }));
  });
});

// Legenda
var makeRow = function (color, text) {
  var box = ui.Label({
    style: { backgroundColor: color, padding: '5px', margin: '0 6px 3px 0', border: '1px solid #222' }
  });
  var lbl = ui.Label({ value: text, style: { margin: '0', fontSize: '10px', color: '#222' } });
  return ui.Panel({ widgets: [box, lbl], layout: ui.Panel.Layout.Flow('horizontal') });
};

mainPanel.add(ui.Label({
  value: '📋 4. Legenda Nasib Bekas Karhutla (Layer 3B):',
  style: { fontWeight: 'bold', fontSize: '11px', color: '#222', margin: '6px 0 2px 0' }
}));
mainPanel.add(makeRow('#00E676', '1. Pulih Jadi Lahan Hijau (NDVI & NDMI Tinggi)'));
mainPanel.add(makeRow('#FF9100', '2. Semak Gambut Kritis (Kering, BSI Tinggi)'));
mainPanel.add(makeRow('#FF1744', '3. Alih Fungsi Perkotaan / Kupasan Tanah'));

Map.add(mainPanel);