// Pratinjau cepat 3 ROI kandidat (2023 Pre, 2023 Fire, 2026) di GEE Code Editor.
// Salin seluruh isi file ini ke https://code.earthengine.google.com lalu klik Run.
// Ganti nilai ROI_AKTIF untuk berpindah wilayah.

var ROIS = {
  'ROI1_Pulang_Pisau':       [114.28, -2.75, 114.42, -2.62],
  'ROI2_Kotawaringin_Timur': [112.78, -2.32, 112.92, -2.19],
  'ROI3_Seruyan':            [112.38, -2.66, 112.52, -2.53]
};
var ROI_AKTIF = 'ROI2_Kotawaringin_Timur';

function maskS2(img) {
  var scl = img.select('SCL');
  var ok = scl.neq(3).and(scl.neq(8)).and(scl.neq(9)).and(scl.neq(10));
  return img.updateMask(ok).divide(10000);
}

function komposit(geom, mulai, akhir) {
  return ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterBounds(geom).filterDate(mulai, akhir)
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 40))
    .map(maskS2).median().clip(geom);
}

var swir = {bands: ['B12', 'B8', 'B4'], min: 0, max: 0.4};
var rgb = {bands: ['B4', 'B3', 'B2'], min: 0, max: 0.15};

Object.keys(ROIS).forEach(function (nama) {
  var geom = ee.Geometry.Rectangle(ROIS[nama]);
  var tampil = (nama === ROI_AKTIF);
  var pre = komposit(geom, '2023-05-01', '2023-07-31');
  var fire = komposit(geom, '2023-09-01', '2023-11-30');
  var now = komposit(geom, '2026-06-01', '2026-09-30');
  var nbr = function (i) { return i.normalizedDifference(['B8', 'B12']); };
  var dnbr = nbr(pre).subtract(nbr(fire));

  Map.addLayer(pre, rgb, nama + ' | 2023 Pre RGB', false);
  Map.addLayer(fire, swir, nama + ' | 2023 Fire SWIR', tampil);
  Map.addLayer(dnbr.updateMask(dnbr.gt(0.2)),
               {min: 0.2, max: 0.6, palette: ['yellow', 'red']}, nama + ' | dNBR > 0.20', tampil);
  Map.addLayer(now, rgb, nama + ' | 2026 RGB (cari petak/grid rapi)', false);
  Map.addLayer(ee.Image().paint(geom, 0, 2), {palette: ['cyan']}, nama + ' | batas');

  var luas = dnbr.gt(0.2).multiply(ee.Image.pixelArea()).divide(10000)
    .reduceRegion({reducer: ee.Reducer.sum(), geometry: geom, scale: 30, maxPixels: 1e9});
  print(nama + ' - luas dNBR > 0.20 (Ha):', luas.get('nd'));
});

Map.centerObject(ee.Geometry.Rectangle(ROIS[ROI_AKTIF]), 12);
Map.setOptions('SATELLITE');

