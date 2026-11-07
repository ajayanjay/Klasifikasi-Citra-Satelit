/**
 * Dense-settlement building segmentation without machine learning.
 *
 * Novelty prototype:
 *   local adaptive multi-cue fusion + morphological reconstruction.
 *
 * Important limitation:
 *   Sentinel-2 resolution is 10 m. This script targets a semantic building
 *   mask. Individual houses cannot be separated when no boundary cue exists.
 */

var CONFIG = {
  startDate: '2023-06-01',
  endDate: '2024-06-01',
  maxCloud: 35,
  scale: 10,
  minConnectedPixels: 3,
  exportResult: false
};

// Dense kampung area near Kampung Melayu, East Jakarta.
// Replace geometry with a drawn polygon for another settlement.
var roi = ee.Geometry.Rectangle([106.8615, -6.2285, 106.8705, -6.2195]);
Map.centerObject(roi, 16);
Map.setOptions('HYBRID');

function maskSentinel2(image) {
  var scl = image.select('SCL');
  var clear = scl.neq(3)       // cloud shadow
    .and(scl.neq(8))            // cloud medium probability
    .and(scl.neq(9))            // cloud high probability
    .and(scl.neq(10))           // cirrus
    .and(scl.neq(11));          // snow/ice
  return image.updateMask(clear).divide(10000);
}

var image = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(roi)
  .filterDate(CONFIG.startDate, CONFIG.endDate)
  .filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE', CONFIG.maxCloud))
  .map(maskSentinel2)
  .median()
  .clip(roi);

var red = image.select('B4');
var green = image.select('B3');
var nir = image.select('B8');
var swir = image.select('B11');
var rgb = image.select(['B4', 'B3', 'B2']);

// Spectral cues.
var ndvi = image.normalizedDifference(['B8', 'B4']);
var ndbi = image.normalizedDifference(['B11', 'B8']);
var brightness = rgb.reduce(ee.Reducer.mean()).rename('brightness');
var nonVegetation = ndvi.lt(0.35);

// Local texture and local adaptive contrast.
var localKernel = ee.Kernel.circle({radius: 2, units: 'pixels'});
var ndbiMean = ndbi.reduceNeighborhood({
  reducer: ee.Reducer.mean(),
  kernel: localKernel
});
var ndbiStd = ndbi.reduceNeighborhood({
  reducer: ee.Reducer.stdDev(),
  kernel: localKernel
}).max(0.01);
var localUrbanContrast = ndbi.subtract(ndbiMean)
  .divide(ndbiStd)
  .add(1).divide(3).clamp(0, 1);

var texture = nir.reduceNeighborhood({
  reducer: ee.Reducer.stdDev(),
  kernel: localKernel
}).unitScale(0.01, 0.16).clamp(0, 1);

// Boundary cue. Canny is used as evidence, not as the building mask.
var edges = ee.Algorithms.CannyEdgeDetector({
  image: brightness,
  threshold: 0.08,
  sigma: 1
}).rename('edges');
var edgeDensity = edges.reduceNeighborhood({
  reducer: ee.Reducer.mean(),
  kernel: localKernel
}).unitScale(0.02, 0.35).clamp(0, 1);

// Fixed, interpretable fusion. No training data or learned parameters.
var urbanSpectral = ndbi.add(0.05).divide(0.30).clamp(0, 1);
var brightRoof = brightness.unitScale(0.08, 0.38).clamp(0, 1);
var evidence = urbanSpectral.multiply(0.30)
  .add(brightRoof.multiply(0.15))
  .add(localUrbanContrast.multiply(0.25))
  .add(texture.multiply(0.15))
  .add(edgeDensity.multiply(0.15))
  .rename('evidence');

// Adaptive threshold from local evidence distribution.
var evidenceMean = evidence.reduceNeighborhood({
  reducer: ee.Reducer.mean(),
  kernel: ee.Kernel.circle({radius: 7, units: 'pixels'})
});
var evidenceStd = evidence.reduceNeighborhood({
  reducer: ee.Reducer.stdDev(),
  kernel: ee.Kernel.circle({radius: 7, units: 'pixels'})
}).max(0.03);
var adaptiveThreshold = evidenceMean.add(evidenceStd.multiply(0.15));
var rawMask = evidence.gt(adaptiveThreshold)
  .and(nonVegetation)
  .rename('raw_mask');

// Morphological reconstruction-like cleanup:
// close narrow roof gaps, then open isolated speckle.
var morphKernel = ee.Kernel.circle({radius: 1, units: 'pixels'});
var closed = rawMask.focal_max({kernel: morphKernel, iterations: 2})
  .focal_min({kernel: morphKernel, iterations: 2});
var opened = closed.focal_min({kernel: morphKernel, iterations: 1})
  .focal_max({kernel: morphKernel, iterations: 1});

// Keep connected regions large enough to represent building groups.
var connected = opened.selfMask().connectedPixelCount(100, true);
var buildingMask = opened.select([0]).updateMask(
  connected.gte(CONFIG.minConnectedPixels)
).selfMask().rename('building_mask');

// Boundary-aware region products. Strong boundaries identify possible
// separate roofs; weak boundaries intentionally remain merged.
var boundaryProduct = edges.select([0]).updateMask(buildingMask).rename('boundary');
var buildingGroups = buildingMask.toByte().reduceToVectors({
  geometry: roi,
  scale: CONFIG.scale,
  geometryType: 'polygon',
  eightConnected: true,
  labelProperty: 'building_group',
  maxPixels: 1e8,
  tileScale: 4
});

Map.addLayer(rgb, {min: 0.03, max: 0.35}, '1. Sentinel-2 RGB');
Map.addLayer(ndvi, {min: -0.2, max: 0.8, palette: ['white', 'green']}, '2. NDVI', false);
Map.addLayer(ndbi, {min: -0.5, max: 0.5, palette: ['blue', 'white', 'red']}, '3. NDBI', false);
Map.addLayer(evidence, {min: 0, max: 1, palette: ['black', 'yellow', 'red']}, '4. Fused evidence', false);
Map.addLayer(rawMask.selfMask(), {palette: ['orange']}, '5. Raw adaptive mask', false);
Map.addLayer(buildingMask, {palette: ['cyan']}, '6. Dense-settlement building mask');
Map.addLayer(boundaryProduct, {palette: ['white']}, '7. Boundary cues', false);
Map.addLayer(
  buildingGroups.style({color: '00FFFF', fillColor: '00000000', width: 1}),
  {},
  '8. Building groups'
);
Map.addLayer(ee.FeatureCollection([ee.Feature(roi)]).style({
  color: 'FFFFFF',
  fillColor: '00000000',
  width: 2
}), {}, 'ROI');

print('Input image count', ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(roi)
  .filterDate(CONFIG.startDate, CONFIG.endDate)
  .size());
print('Semantic building groups', buildingGroups.size());
print('Method', 'Adaptive multi-cue fusion + morphological reconstruction');

if (CONFIG.exportResult) {
  Export.image.toDrive({
    image: buildingMask.unmask(0).rename('building_mask'),
    description: 'jakarta_dense_settlement_dip_mask',
    folder: 'gee_building_detection',
    region: roi,
    scale: CONFIG.scale,
    maxPixels: 1e8
  });
}
