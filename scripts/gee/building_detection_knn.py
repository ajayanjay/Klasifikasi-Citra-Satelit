"""
==============================================================================
PRAKTIKUM PENGOLAHAN CITRA DIGITAL (PCD) - SEMESTER 5 D4/D3 TEKNIK INFORMATIKA
==============================================================================
JUDUL PAPER:
Deteksi dan Klasifikasi Tipe Bangunan pada Citra Satelit Menggunakan
Metode K-Nearest Neighbor (k-NN)
(Studi Replikasi Berdasarkan Adam Jaelani, UIN Maulana Malik Ibrahim Malang)

DESKRIPSI:
Script Python Google Earth Engine (menggunakan `ee` dan `geemap`) untuk
dijalankan pada Google Colab atau Jupyter Notebook lokal.

Pipeline Komputasi Visual:
1. Akuisisi Citra Sentinel-2 SR Bebas Awan
2. Konversi Ruang Warna RGB -> CIE L*a*b* (via XYZ D65)
3. Segmentasi Warna K-Means (k=3) pada bidang kromatik a*b*
4. Morfologi Biner (Opening, Closing/Filling Holes, Bwareaopen)
5. Ekstraksi Vektor Fitur Geometris 4D (Luas, Keliling, Metric, Eccentricity)
6. Klasifikasi Terawasi k-Nearest Neighbor (k-NN k=5)
7. Visualisasi Interaktif dengan Peta geemap
==============================================================================
"""

import math
import ee
import geemap

# ------------------------------------------------------------------------------
# 1. INISIALISASI GOOGLE EARTH ENGINE
# ------------------------------------------------------------------------------
try:
    ee.Initialize()
    print("[INFO] Google Earth Engine berhasil diinisialisasi.")
except Exception as e:
    print("[INFO] Melakukan autentikasi GEE...")
    ee.Authenticate()
    ee.Initialize()

# ------------------------------------------------------------------------------
# 2. PARAMETER DAN WILAYAH KAJIAN (ROI)
# ------------------------------------------------------------------------------
CONFIG = {
    'mode': 'HIGH_RES_INDIVIDUAL',  # 'HIGH_RES_INDIVIDUAL' (presisi per rumah) atau 'PIXEL_SEGMENTATION'
    'study_area': 'MALANG_SAWOJAJAR', # 'MALANG_SAWOJAJAR' atau 'BANDUNG_POLBAN'
    'start_date': '2023-06-01',
    'end_date': '2023-09-30',
    'scale': 10,
    'k_means_clusters': 3,
    'knn_neighbors': 5,
    'min_pixel_noise': 2
}

if CONFIG['study_area'] == 'MALANG_SAWOJAJAR':
    # Perumahan Sawojajar, Malang (~750m x 750m)
    roi = ee.Geometry.Polygon([
        [[112.6530, -7.9700],
         [112.6610, -7.9700],
         [112.6610, -7.9770],
         [112.6530, -7.9770],
         [112.6530, -7.9700]]
    ])
    center_coords = [-7.9735, 112.6570]
else:
    # Kampus Polban & Perumahan Ciwaruga, Bandung (~750m x 750m)
    roi = ee.Geometry.Polygon([
        [[107.5680, -6.8680],
         [107.5780, -6.8680],
         [107.5780, -6.8760],
         [107.5680, -6.8760],
         [107.5680, -6.8680]]
    ])
    center_coords = [-6.8720, 107.5730]

# ------------------------------------------------------------------------------
# 3. AKUISISI CITRA SATELIT (SENTINEL-2 SR)
# ------------------------------------------------------------------------------
s2 = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
      .filterBounds(roi)
      .filterDate(CONFIG['start_date'], CONFIG['end_date'])
      .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
      .median()
      .clip(roi))

# Normalisasi kanal B4 (R), B3 (G), B2 (B) ke rentang [0.0, 1.0]
rgb_image = s2.select(['B4', 'B3', 'B2'], ['R', 'G', 'B']).divide(10000.0).clamp(0.0, 1.0)

# ------------------------------------------------------------------------------
# 4. KONVERSI RUANG WARNA RGB -> CIE L*a*b*
# ------------------------------------------------------------------------------
def rgb_to_cie_lab(img_rgb):
    r = img_rgb.select('R')
    g = img_rgb.select('G')
    b = img_rgb.select('B')

    # Matriks transformasi linier ke XYZ (D65)
    X = r.multiply(0.412453).add(g.multiply(0.357580)).add(b.multiply(0.180423))
    Y = r.multiply(0.212671).add(g.multiply(0.715160)).add(b.multiply(0.072169))
    Z = r.multiply(0.019334).add(g.multiply(0.119193)).add(b.multiply(0.950227))

    xr = X.divide(0.950456)
    yr = Y.divide(1.000000)
    zr = Z.divide(1.088754)

    def f_nonlin(t):
        t_pow = t.pow(1.0 / 3.0)
        t_lin = t.multiply(7.787).add(16.0 / 116.0)
        return t_pow.where(t.lte(0.008856), t_lin)

    fx = f_nonlin(xr)
    fy = f_nonlin(yr)
    fz = f_nonlin(zr)

    L = fy.multiply(116.0).subtract(16.0).rename('L')
    a = fx.subtract(fy).multiply(500.0).rename('a')
    b_chan = fy.subtract(fz).multiply(200.0).rename('b')

    return ee.Image.cat([L, a, b_chan])

lab_image = rgb_to_cie_lab(rgb_image)

# ------------------------------------------------------------------------------
# 5. SEGMENTASI K-MEANS CLUSTERING (k=3)
# ------------------------------------------------------------------------------
cluster_input = lab_image.select(['a', 'b'])

training_sample = cluster_input.sample(
    region=roi,
    scale=CONFIG['scale'],
    numPixels=3000,
    seed=42
)

clusterer = ee.Clusterer.wekaKMeans(
    nClusters=CONFIG['k_means_clusters'],
    seed=42
).train(training_sample)

clustered = cluster_input.cluster(clusterer).rename('cluster')

# Deteksi otomatis kluster atap bangunan berdasarkan rata-rata kromatik a*
mean_a_0 = lab_image.select('a').updateMask(clustered.eq(0)).reduceRegion(
    reducer=ee.Reducer.mean(), geometry=roi, scale=CONFIG['scale'], maxPixels=1e6
).get('a')
mean_a_1 = lab_image.select('a').updateMask(clustered.eq(1)).reduceRegion(
    reducer=ee.Reducer.mean(), geometry=roi, scale=CONFIG['scale'], maxPixels=1e6
).get('a')
mean_a_2 = lab_image.select('a').updateMask(clustered.eq(2)).reduceRegion(
    reducer=ee.Reducer.mean(), geometry=roi, scale=CONFIG['scale'], maxPixels=1e6
).get('a')

a_scores = ee.List([mean_a_0, mean_a_1, mean_a_2])
max_cluster = a_scores.indexOf(a_scores.reduce(ee.Reducer.max()))
raw_building_mask = clustered.eq(ee.Number(max_cluster)).rename('raw_building')

# ------------------------------------------------------------------------------
# 6. PEMROSESAN MORFOLOGI BINER & BWAREAOPEN
# ------------------------------------------------------------------------------
kernel = ee.Kernel.square(radius=1, units='pixels')

# Opening (Erosi -> Dilasi)
eroded = raw_building_mask.focal_min(kernel=kernel, iterations=1)
opened = eroded.focal_max(kernel=kernel, iterations=1)

# Closing (Dilasi -> Erosi) untuk mengisi celah/rongga interior atap
dilated = opened.focal_max(kernel=kernel, iterations=1)
closed = dilated.focal_min(kernel=kernel, iterations=1)

# Bwareaopen (hapus komponen noise terhubung yang sangat kecil)
connected_count = closed.connectedPixelCount(maxSize=100, eightConnected=True)
clean_building_mask = closed.updateMask(connected_count.gte(CONFIG['min_pixel_noise']))

# ------------------------------------------------------------------------------
# 7. VEKTORISASI DAN EKSTRAKSI VEKTOR FITUR 4D (A, P, M, e)
# ------------------------------------------------------------------------------
if CONFIG['mode'] == 'HIGH_RES_INDIVIDUAL':
    building_polygons = (ee.FeatureCollection('GOOGLE/Research/open-buildings/v3/polygons')
                         .filterBounds(roi)
                         .filter(ee.Filter.gte('confidence', 0.65)))
else:
    building_polygons = clean_building_mask.toInt().reduceToVectors(
        geometry=roi,
        crs=rgb_image.projection(),
        scale=CONFIG['scale'],
        geometryType='polygon',
        eightConnected=True,
        labelProperty='building_id',
        maxPixels=1e8,
        tileScale=4
    )

def extract_features(feat):
    geom = feat.geometry().buffer(0, 1)
    area = geom.area(1)
    perimeter = geom.perimeter(1)
    metric = ee.Number(4 * math.pi).multiply(area).divide(perimeter.pow(2).max(1e-6))

    bounds = geom.bounds(1)
    coords = ee.List(bounds.coordinates().get(0))
    p0 = ee.List(coords.get(0))
    p1 = ee.List(coords.get(1))
    p2 = ee.List(coords.get(2))

    dx = ee.Number(p1.get(0)).subtract(ee.Number(p0.get(0))).abs()
    dy = ee.Number(p2.get(1)).subtract(ee.Number(p1.get(1))).abs()
    min_dim = dx.min(dy)
    max_dim = dx.max(dy).max(1e-6)
    ratio = min_dim.divide(max_dim).min(1.0)
    eccentricity = ee.Number(1).subtract(ratio.pow(2)).sqrt()

    return feat.set({
        'Area': area,
        'Perimeter': perimeter,
        'Metric': metric,
        'Eccentricity': eccentricity
    })

building_features = building_polygons.map(extract_features)
valid_buildings = building_features.filter(
    ee.Filter.And(
        ee.Filter.gt('Area', 40),
        ee.Filter.lt('Area', 50000)
    )
)

# ------------------------------------------------------------------------------
# 8. KLASIFIKASI K-NEAREST NEIGHBOR (k-NN, k=5)
# ------------------------------------------------------------------------------
# Data latih referensi dari Tabel 3.4 Skripsi (Adam Jaelani, 2020)
training_list = [
    {'Area': 650, 'Perimeter': 125, 'Metric': 0.32, 'Eccentricity': 0.97, 'class_code': 1},
    {'Area': 850, 'Perimeter': 145, 'Metric': 0.30, 'Eccentricity': 0.97, 'class_code': 1},
    {'Area': 520, 'Perimeter': 105, 'Metric': 0.35, 'Eccentricity': 0.96, 'class_code': 1},
    {'Area': 720, 'Perimeter': 132, 'Metric': 0.37, 'Eccentricity': 0.96, 'class_code': 1},
    {'Area': 950, 'Perimeter': 160, 'Metric': 0.28, 'Eccentricity': 0.97, 'class_code': 1},

    {'Area': 240, 'Perimeter': 68,  'Metric': 0.56, 'Eccentricity': 0.69, 'class_code': 2},
    {'Area': 280, 'Perimeter': 74,  'Metric': 0.71, 'Eccentricity': 0.65, 'class_code': 2},
    {'Area': 190, 'Perimeter': 62,  'Metric': 0.71, 'Eccentricity': 0.77, 'class_code': 2},
    {'Area': 310, 'Perimeter': 82,  'Metric': 0.46, 'Eccentricity': 0.73, 'class_code': 2},
    {'Area': 170, 'Perimeter': 58,  'Metric': 0.57, 'Eccentricity': 0.80, 'class_code': 2},

    {'Area': 75,  'Perimeter': 38,  'Metric': 0.65, 'Eccentricity': 0.77, 'class_code': 3},
    {'Area': 110, 'Perimeter': 48,  'Metric': 0.62, 'Eccentricity': 0.61, 'class_code': 3},
    {'Area': 90,  'Perimeter': 42,  'Metric': 0.56, 'Eccentricity': 0.68, 'class_code': 3},
    {'Area': 65,  'Perimeter': 35,  'Metric': 0.62, 'Eccentricity': 0.68, 'class_code': 3},
    {'Area': 120, 'Perimeter': 50,  'Metric': 0.60, 'Eccentricity': 0.51, 'class_code': 3}
]

training_fc = ee.FeatureCollection([ee.Feature(None, d) for d in training_list])

knn = ee.Classifier.smileKNN(
    k=CONFIG['knn_neighbors'],
    searchMethod='AUTO'
).train(
    features=training_fc,
    classProperty='class_code',
    inputProperties=['Area', 'Perimeter', 'Metric', 'Eccentricity']
)

classified = valid_buildings.classify(knn, 'predicted_type')

# ------------------------------------------------------------------------------
# 9. PEMISAHAN KELAS UNTUK STYLING VISUAL
# ------------------------------------------------------------------------------
tipe_A = classified.filter(ee.Filter.eq('predicted_type', 1))
tipe_B = classified.filter(ee.Filter.eq('predicted_type', 2))
tipe_C = classified.filter(ee.Filter.eq('predicted_type', 3))

open_buildings = ee.FeatureCollection('GOOGLE/Research/open-buildings/v3/polygons').filterBounds(roi)

print("=== STATISTIK HASIL DETEKSI BANGUNAN ===")
print(f"Area Studi: {CONFIG['study_area']}")
print(f"Jumlah Bangunan Tipe A (Besar): {tipe_A.size().getInfo()}")
print(f"Jumlah Bangunan Tipe B (Sedang): {tipe_B.size().getInfo()}")
print(f"Jumlah Bangunan Tipe C (Kecil): {tipe_C.size().getInfo()}")
print(f"Total Bangunan Terdeteksi: {classified.size().getInfo()}")
print(f"Total Pembanding (Google Open Buildings): {open_buildings.size().getInfo()}")

# ------------------------------------------------------------------------------
# 10. VISUALISASI INTERAKTIF DENGAN GEEMAP
# ------------------------------------------------------------------------------
m = geemap.Map(center=center_coords, zoom=17)
m.add_basemap('HYBRID')

# 1. Citra RGB
m.addLayer(rgb_image, {'bands': ['R', 'G', 'B'], 'min': 0.05, 'max': 0.35}, '1. Citra Asli (RGB Sentinel-2)')

# 2. Mask Bersih Morfologi
m.addLayer(clean_building_mask.selfMask(), {'palette': ['#FFFFFF']}, '2. Mask Bersih Morfologi', False)

# 3. Klasifikasi Poligon Bangunan
m.addLayer(tipe_A.draw(color='FF2222', strokeWidth=2), {}, '3a. Klasifikasi Tipe A (Besar - Merah)')
m.addLayer(tipe_B.draw(color='FFD700', strokeWidth=2), {}, '3b. Klasifikasi Tipe B (Sedang - Kuning)')
m.addLayer(tipe_C.draw(color='00E5FF', strokeWidth=2), {}, '3c. Klasifikasi Tipe C (Kecil - Cyan)')

# 4. Google Open Buildings Ground Truth
m.addLayer(open_buildings.draw(color='76FF03', strokeWidth=1), {}, '4. Google Open Buildings AI (Hijau)', False)

# 5. Batas ROI
m.addLayer(ee.FeatureCollection([ee.Feature(roi)]).style(color='FFFFFF', fillColor='00000000', width=2), {}, 'Batas ROI')

# Simpan map ke file HTML untuk preview instan
output_html = "gee_scripts/map_preview.html"
m.to_html(output_html)
print(f"[INFO] Peta interaktif berhasil disimpan ke: {output_html}")
