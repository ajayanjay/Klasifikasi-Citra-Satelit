// =========================================================================
// INSPEKSI VISUAL INTERAKTIF: KEBAKARAN EL NINO 2023 VS KONDISI 2026
// PENGOLAHAN CITRA DIGITAL (PCD) - KELOMPOK 3B POLBAN
//
// Salin seluruh isi file ini ke https://code.earthengine.google.com/
// lalu klik "RUN".
//
// Fitur:
// 1. Membandingkan Before 2023 vs Saat Kebakaran 2023 vs Terkini 2026
// 2. Visualisasi Arang Hitam (True Color & SWIR False Color)
// 3. Lapisan Titik Api NASA FIRMS 2023 (Bukti Api Riil di Lapangan)
// 4. Poligon Luka Bakar dNBR > 0.20
// 5. Perhitungan Otomatis Luas Terbakar Riil (Hektar) di Konsol
// =========================================================================

// Koordinat Wilayah Master 30x30 km (Palangka Raya - Sungai Kahayan - Sebangau)
var studyCoords = [113.885986, -2.414934, 114.154490, -2.144997];
var geom = ee.Geometry.Rectangle(studyCoords);

// 1. Pre-Processing & Masking Awan
function maskS2(image) {
  var scl = image.select('SCL');
  var mask = scl.neq(3).and(scl.neq(8)).and(scl.neq(9)).and(scl.neq(10));
  return image.updateMask(mask);
}

function getComposite(start, end) {
  return ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterBounds(geom)
    .filterDate(start, end)
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 85))
    .map(maskS2)
    .median()
    .clip(geom)
    .divide(10000);
}

// 2. Pembuatan Komposit Tiap Fase
// a) Sebelum Terbakar (Mei - Juli 2023)
var imgPre = getComposite('2023-05-01', '2023-07-31');

// b) Puncak Kebakaran El Nino (September - November 2023)
var imgFire = getComposite('2023-09-01', '2023-11-30');

// c) Kondisi Terkini 3 Tahun Pasca-Bakar (Juni - September 2026)
var imgNow = getComposite('2026-06-01', '2026-09-30');

// 3. Perhitungan Indeks dNBR
var nbrPre = imgPre.normalizedDifference(['B8', 'B12']);
var nbrFire = imgFire.normalizedDifference(['B8', 'B12']);
var dnbr = nbrPre.subtract(nbrFire);
var burnScarMask = dnbr.gt(0.20);

// 4. Titik Api NASA FIRMS (Agustus - November 2023)
var firmsHotspots = ee.FeatureCollection('FIRMS')
  .filterBounds(geom)
  .filterDate('2023-08-01', '2023-11-30');

// 5. Parameter Visualisasi
var visRGB = { bands: ['B4', 'B3', 'B2'], min: 0.02, max: 0.16 };
var visSWIR = { bands: ['B12', 'B8', 'B4'], min: 0.05, max: 0.40 }; // SWIR: Luka bakar = Coklat Kemerahan/Oranye
var visDNBR = { min: 0.20, max: 0.60, palette: ['#FFFF00', '#FF7F00', '#FF0000', '#7F0000'] };

// 6. Tampilkan ke Peta
Map.setOptions('HYBRID');
Map.centerObject(geom, 11);

// Layer-layer yang bisa dinyalakan / dimatikan di panel kanan atas peta:
Map.addLayer(imgPre, visRGB, '1. [BEFORE] Mei-Juli 2023 True Color (Hijau Alami)', false);
Map.addLayer(imgFire, visRGB, '2. [SAAT BAKAR] Sep-Nov 2023 True Color (Arang Hitam)', true);
Map.addLayer(imgFire, visSWIR, '3. [SAAT BAKAR] Sep-Nov 2023 SWIR Penetrating (Merah = Bekas Terbakar)', true);
Map.addLayer(burnScarMask.updateMask(burnScarMask), visDNBR, '4. [DELINIASI] Poligon dNBR > 0.20 (Luka Bakar Valid)', false);
Map.addLayer(firmsHotspots, { color: 'red' }, '5. [TITIK API] NASA FIRMS Hotspots 2023', false);
Map.addLayer(imgNow, visRGB, '6. [TERKINI] Juni-Sept 2026 True Color (Kondisi 3 Thn Pasca-Bakar)', false);
Map.addLayer(ee.Image().paint(geom, 0, 2), { palette: ['cyan'] }, 'Batas Area Studi 30x30 km');

// 7. Hitung Kuantifikasi Luas Terbakar Riil di Konsol
var areaTerbakarHa = burnScarMask.multiply(ee.Image.pixelArea()).divide(10000)
  .reduceRegion({
    reducer: ee.Reducer.sum(),
    geometry: geom,
    scale: 30,
    maxPixels: 1e9
  });

print('=== HASIL INSPEKSI WILAYAH 30x30 KM (PALANGKA RAYA - SEBANGAU) ===');
print('Jumlah Deteksi Titik Api NASA FIRMS (Sep-Nov 2023) :', firmsHotspots.size());
print('Luas Estimasi Poligon Terbakar dNBR > 0.20 (Hektar)  :', areaTerbakarHa.get('nd'));
print('Petunjuk: Centang/Uncentang layer di panel kanan atas untuk membandingkan!');

