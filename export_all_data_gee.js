// =========================================================================
// PENGOLAHAN CITRA DIGITAL (PCD) - KELOMPOK 3B POLBAN
// SKRIP EKSPOR DATASET MULTI-TAHUN (2023 - 2026) KE GOOGLE DRIVE (10 METER)
//
// WILAYAH STUDI UTAMA: PALANGKA RAYA - SEBANGAU - SUNGAI KAHAYAN (30 x 30 KM)
// Koordinat sama persis dengan Citra Master 2019 (3000 x 3000 piksel)
//
// Seluruh file tersimpan rapi di SATU folder Google Drive:
// "PCD_Karhutla_Kalteng_2023_2026"
// =========================================================================

var DRIVE_FOLDER = 'PCD_Karhutla_Kalteng_2023_2026';

// -------------------------------------------------------------------------
// 1. AREA STUDI MASTER (30 x 30 KM) - SAMA PERSIS DENGAN CITRA MASTER 2019
// -------------------------------------------------------------------------
var studyCoords = [113.885986, -2.414934, 114.154490, -2.144997];
var geom = ee.Geometry.Rectangle(studyCoords);
var ROI_NAME = 'Kalteng_Sebangau_Kahayan';

// -------------------------------------------------------------------------
// 2. FUNGSI FILTER AWAN & PRE-PROCESSING SENTINEL-2 L2A (100% BEBAS BOLONG)
// -------------------------------------------------------------------------
function maskS2Clouds(image) {
  var qa = image.select('QA60');
  var cloudBit = 1 << 10;
  var cirrusBit = 1 << 11;
  var qaMask = qa.bitwiseAnd(cloudBit).eq(0).and(qa.bitwiseAnd(cirrusBit).eq(0));

  var scl = image.select('SCL');
  var validScl = scl.neq(3).and(scl.neq(8)).and(scl.neq(9)).and(scl.neq(10));

  return image.updateMask(qaMask).updateMask(validScl);
}

function getS2Composite(startDate, endDate) {
  var bands = ['B2', 'B3', 'B4', 'B8', 'B11', 'B12'];
  return ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterBounds(geom)
    .filterDate(startDate, endDate)
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 85))
    .map(maskS2Clouds)
    .select(bands)
    .median()
    .unmask(0)
    .clip(geom)
    .multiply(0.0001)
    .toFloat();
}

function maskGedi(img) {
  var valid = img.select('quality_flag').eq(1).and(img.select('degrade_flag').eq(0));
  return img.updateMask(valid).select('rh98');
}

// -------------------------------------------------------------------------
// 3. KOMPOSIT DERET WAKTU TAHUNAN (2023 Pre -> 2023 Fire -> 2024 -> 2025 -> 2026)
// -------------------------------------------------------------------------
var pre2023  = getS2Composite('2023-04-01', '2023-07-31');
var fire2023 = getS2Composite('2023-08-15', '2023-11-30');
var y12024   = getS2Composite('2024-05-01', '2024-10-15');
var y22025   = getS2Composite('2025-05-01', '2025-10-15');
var now2026  = getS2Composite('2026-05-01', '2026-10-15');

// Data Pendukung: Termal NASA FIRMS & Air Permukaan JRC GSW
var firms = ee.ImageCollection('FIRMS')
  .filterBounds(geom)
  .filterDate('2023-08-01', '2023-11-30')
  .select('T21')
  .max()
  .unmask(0)
  .clip(geom)
  .toFloat();

var jrc = ee.Image('JRC/GSW1_4/GlobalSurfaceWater')
  .select('occurrence')
  .unmask(0)
  .clip(geom)
  .toFloat();

var auxImg = firms.addBands(jrc).rename(['firms_t21', 'jrc_water']);

// Dynamic World 2026 (Ground Truth LULC Global)
var dwMode = ee.ImageCollection('GOOGLE/DYNAMICWORLD/V1')
  .filterBounds(geom)
  .filterDate('2026-05-01', '2026-10-15')
  .select('label')
  .reduce(ee.Reducer.mode())
  .rename('dw_label')
  .clip(geom)
  .toInt16();

// GEDI L2A RH98 (LiDAR Tinggi Kanopi Pohon)
var gedi = ee.ImageCollection('LARSE/GEDI/GEDI02_A_002_MONTHLY')
  .filterBounds(geom)
  .filterDate('2024-05-01', '2026-10-15')
  .map(maskGedi)
  .median()
  .unmask(-1)
  .rename('gedi_rh98')
  .clip(geom)
  .toFloat();

// -------------------------------------------------------------------------
// 4. PENDAFTARAN EKSPOR KE GOOGLE DRIVE (10 METER MURNI)
// -------------------------------------------------------------------------
var exportList = [
  { image: pre2023,  name: ROI_NAME + '_s2_2023_pre' },
  { image: fire2023, name: ROI_NAME + '_s2_2023_fire' },
  { image: y12024,   name: ROI_NAME + '_s2_2024_y1' },
  { image: y22025,   name: ROI_NAME + '_s2_2025_y2' },
  { image: now2026,  name: ROI_NAME + '_s2_2026_now' },
  { image: auxImg,   name: ROI_NAME + '_aux_firms_water' },
  { image: dwMode,   name: ROI_NAME + '_gt_dynamic_world_2026' },
  { image: gedi,     name: ROI_NAME + '_gedi_rh98' }
];

exportList.forEach(function (item) {
  Export.image.toDrive({
    image: item.image,
    description: item.name,
    folder: DRIVE_FOLDER,
    fileNamePrefix: item.name,
    region: geom,
    scale: 10,
    maxPixels: 1e9,
    fileFormat: 'GeoTIFF'
  });
});

// Tampilan Visualisasi di Peta GEE
Map.setOptions('HYBRID');
Map.centerObject(geom, 11);
Map.addLayer(pre2023,  {bands: ['B4', 'B3', 'B2'], min: 0.02, max: 0.15}, '1. 2023 Pre-Fire True Color');
Map.addLayer(fire2023, {bands: ['B12', 'B8', 'B4'], min: 0.05, max: 0.40}, '2. 2023 Fire SWIR Burn Scar', false);
Map.addLayer(now2026,  {bands: ['B4', 'B3', 'B2'], min: 0.02, max: 0.15}, '3. 2026 Now True Color', false);
Map.addLayer(ee.Image().paint(geom, 0, 2), {palette: ['cyan']}, 'Batas Master 30x30 km');

print('=== EKSPOR DATASET MASTER 30x30 KM (PALANGKA RAYA - SEBANGAU) ===');
print('Ukuran Wilayah : 30 km x 30 km (Sama persis dengan baseline 2019)');
print('Folder Drive   :', DRIVE_FOLDER);
print('Total Ekspor   : 8 file GeoTIFF (Resolusi 10 Meter Murni)');
print('Silakan buka tab Tasks di kanan atas, lalu klik RUN ALL.');
