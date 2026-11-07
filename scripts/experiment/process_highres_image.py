"""
==============================================================================
REPLIKASI PAPER PENGOLAHAN CITRA DIGITAL (PCD) - HIGH RES & WATERSHED k-NN
==============================================================================
Paper: Deteksi dan Klasifikasi Tipe Bangunan pada Citra Satelit (k-NN)
Penulis: Adam Jaelani (2020), Teknik Informatika UIN Maliki Malang
File: dataset/data_701m.jpg

Alur Komputasi:
1. Konversi RGB -> CIE L*a*b*
2. Eliminasi Vegetasi (HSV) & Bayangan Jalan (L* < 45)
3. Segmentasi Tepi Morfologis + Distance Transform Peak Finding
4. Marker-controlled Watershed (Pemisah atap rapat antar gang)
5. Ekstraksi Fitur 4D: Luas (A), Keliling (P), Metric (M), Eccentricity (e)
6. Klasifikasi Terawasi k-NN (k=5) ke Tipe A, B, C
==============================================================================
"""

import os
import cv2
import numpy as np
import pandas as pd
from scipy.ndimage import maximum_filter
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

INPUT_PATH = os.path.join("dataset", "data_1.jpg")
OUTPUT_DIR = "output_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Load Citra
img_bgr = cv2.imread(INPUT_PATH)
if img_bgr is None:
    raise FileNotFoundError(f"Citra tidak ditemukan di {INPUT_PATH}")

h_orig, w_orig = img_bgr.shape[:2]
TARGET_WIDTH = 2048
scale_ratio = TARGET_WIDTH / w_orig
target_height = int(h_orig * scale_ratio)

img_resized = cv2.resize(img_bgr, (TARGET_WIDTH, target_height), interpolation=cv2.INTER_AREA)
img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

# 2. Ruang Warna CIE L*a*b* (Sesuai Bab 3 Paper)
img_lab = cv2.cvtColor(img_resized, cv2.COLOR_BGR2LAB)
L_chan, a_chan, b_chan = cv2.split(img_lab)

cv2.imwrite(os.path.join(OUTPUT_DIR, "step1_input_rgb.jpg"), cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR))
cv2.imwrite(os.path.join(OUTPUT_DIR, "step2_lab_image.jpg"), img_lab)

# 3. Masking Vegetasi & Bayangan Jalan (Penghalang Bukan Atap)
hsv = cv2.cvtColor(img_resized, cv2.COLOR_BGR2HSV)
veg_mask = cv2.inRange(hsv, np.array([28, 30, 25]), np.array([85, 255, 255]))
shadow_mask = cv2.inRange(L_chan, 0, 45)

# Tepi batas bangunan / gang (Bilateral + Canny)
blur = cv2.bilateralFilter(gray, 7, 50, 50)
edge_mask = cv2.Canny(blur, 40, 120)

barrier = veg_mask | shadow_mask | edge_mask
roof_candidate = cv2.bitwise_not(barrier)

# 4. Morfologi Biner (Opening & Clean)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
roof_clean = cv2.morphologyEx(roof_candidate, cv2.MORPH_OPEN, kernel, iterations=1)
cv2.imwrite(os.path.join(OUTPUT_DIR, "step3_roof_candidate_mask.jpg"), roof_clean)

# 5. Marker-Controlled Watershed (Pemisah Atap Rapat)
dist = cv2.distanceTransform(roof_clean, cv2.DIST_L2, 5)
local_max = maximum_filter(dist, size=21) == dist
peaks = local_max & (dist > 7)

num_markers, markers = cv2.connectedComponents(peaks.astype(np.uint8))
sure_bg = cv2.dilate(roof_clean, kernel, iterations=3)
unknown = cv2.subtract(sure_bg, peaks.astype(np.uint8) * 255)

markers = markers + 1
markers[unknown == 255] = 0

ws = cv2.watershed(img_resized, markers)

# 6. Ekstraksi Vektor Fitur 4D (Luas A, Keliling P, Metric M, Eccentricity e)
houses = []
valid_contours = []

for m_id in range(2, num_markers + 1):
    mask_i = (ws == m_id).astype(np.uint8)
    area = float(np.sum(mask_i))
    if not (200 <= area <= 18000):
        continue

    cnts, _ = cv2.findContours(mask_i, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts:
        continue

    cnt = cnts[0]
    perimeter = float(cv2.arcLength(cnt, True))
    if perimeter == 0:
        continue

    # Metric = 4 * PI * Area / Perimeter^2
    metric = float((4.0 * np.pi * area) / (perimeter ** 2))

    # Eccentricity = sqrt(1 - (b/a)^2)
    x, y, bw, bh = cv2.boundingRect(cnt)
    aspect = min(bw, bh) / max(1, max(bw, bh))

    # Filter artefak jalan / garis sempit
    if aspect < 0.20 or metric < 0.12:
        continue

    if len(cnt) >= 5:
        (cx, cy), (MA, ma), angle = cv2.fitEllipse(cnt)
        minor_ax = min(MA, ma)
        major_ax = max(MA, ma)
        eccentricity = float(np.sqrt(max(0.0, 1.0 - (minor_ax / max(1e-6, major_ax)) ** 2)))
    else:
        eccentricity = float(np.sqrt(max(0.0, 1.0 - aspect ** 2)))

    houses.append({
        'Luas': area,
        'Keliling': perimeter,
        'Metric': metric,
        'Eccentricity': eccentricity
    })
    valid_contours.append((cnt, x, y, bw, bh))

features_df = pd.DataFrame(houses)
print(f"Total Bangunan Terdeteksi & Tervalidasi: {len(features_df)}")

# 7. Dataset Latih & Klasifikasi k-NN (k=5)
train_data = [
    # Tipe A (Bangunan Besar / Luas > 4000 px): Label 1
    {'Luas': 6500, 'Keliling': 550, 'Metric': 0.32, 'Eccentricity': 0.97, 'Tipe': 1},
    {'Luas': 8500, 'Keliling': 620, 'Metric': 0.28, 'Eccentricity': 0.97, 'Tipe': 1},
    {'Luas': 5200, 'Keliling': 480, 'Metric': 0.35, 'Eccentricity': 0.96, 'Tipe': 1},
    {'Luas': 7500, 'Keliling': 580, 'Metric': 0.30, 'Eccentricity': 0.97, 'Tipe': 1},
    {'Luas': 4500, 'Keliling': 410, 'Metric': 0.38, 'Eccentricity': 0.94, 'Tipe': 1},

    # Tipe B (Bangunan Sedang / Luas 1500 - 4000 px): Label 2
    {'Luas': 2200, 'Keliling': 240, 'Metric': 0.55, 'Eccentricity': 0.72, 'Tipe': 2},
    {'Luas': 2800, 'Keliling': 270, 'Metric': 0.60, 'Eccentricity': 0.68, 'Tipe': 2},
    {'Luas': 1800, 'Keliling': 210, 'Metric': 0.65, 'Eccentricity': 0.65, 'Tipe': 2},
    {'Luas': 3200, 'Keliling': 300, 'Metric': 0.48, 'Eccentricity': 0.75, 'Tipe': 2},
    {'Luas': 2500, 'Keliling': 250, 'Metric': 0.58, 'Eccentricity': 0.70, 'Tipe': 2},

    # Tipe C (Bangunan Kecil / Luas < 1500 px): Label 3
    {'Luas': 500,  'Keliling': 100, 'Metric': 0.68, 'Eccentricity': 0.62, 'Tipe': 3},
    {'Luas': 800,  'Keliling': 130, 'Metric': 0.65, 'Eccentricity': 0.68, 'Tipe': 3},
    {'Luas': 1100, 'Keliling': 155, 'Metric': 0.60, 'Eccentricity': 0.72, 'Tipe': 3},
    {'Luas': 400,  'Keliling': 85,  'Metric': 0.70, 'Eccentricity': 0.60, 'Tipe': 3},
    {'Luas': 950,  'Keliling': 140, 'Metric': 0.62, 'Eccentricity': 0.65, 'Tipe': 3}
]

train_df = pd.DataFrame(train_data)
scaler = StandardScaler()
X_train = scaler.fit_transform(train_df[['Luas', 'Keliling', 'Metric', 'Eccentricity']])
y_train = train_df['Tipe'].values

knn = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
knn.fit(X_train, y_train)

X_test = scaler.transform(features_df[['Luas', 'Keliling', 'Metric', 'Eccentricity']])
predicted_types = knn.predict(X_test)
features_df['Prediksi_Tipe'] = predicted_types
features_df['Nama_Tipe'] = features_df['Prediksi_Tipe'].map({
    1: 'Tipe A (Besar)',
    2: 'Tipe B (Sedang)',
    3: 'Tipe C (Kecil)'
})

csv_output = os.path.join(OUTPUT_DIR, "tabel_fitur_dan_klasifikasi.csv")
features_df.to_csv(csv_output, index=False)

count_A = int(np.sum(predicted_types == 1))
count_B = int(np.sum(predicted_types == 2))
count_C = int(np.sum(predicted_types == 3))
total = len(predicted_types)

print("=" * 60)
print(f"Total: {total} rumah")
print(f"Tipe A (Besar  - Merah) : {count_A} ({count_A/total*100:.1f}%)")
print(f"Tipe B (Sedang - Kuning): {count_B} ({count_B/total*100:.1f}%)")
print(f"Tipe C (Kecil  - Cyan)  : {count_C} ({count_C/total*100:.1f}%)")
print("=" * 60)

# 8. Visualisasi Bounding Box & Poligon per Rumah
canvas = img_rgb.copy()
COLOR_MAP = {
    1: (255, 30, 30),   # Merah (Tipe A)
    2: (255, 220, 0),   # Kuning (Tipe B)
    3: (0, 225, 255)    # Cyan (Tipe C)
}

for i, (cnt, x, y, bw, bh) in enumerate(valid_contours):
    p_type = predicted_types[i]
    color = COLOR_MAP[p_type]
    cv2.drawContours(canvas, [cnt], -1, color, 1)
    cv2.rectangle(canvas, (x, y), (x + bw, y + bh), color, 1)

final_path = os.path.join(OUTPUT_DIR, "step5_final_detected_buildings.jpg")
cv2.imwrite(final_path, cv2.cvtColor(canvas, cv2.COLOR_RGB2BGR))

fig, ax = plt.subplots(1, 2, figsize=(18, 9))
ax[0].imshow(img_rgb)
ax[0].set_title("Input (701m Google Earth)", fontsize=13)
ax[0].axis('off')

ax[1].imshow(canvas)
ax[1].set_title(f"Hasil Deteksi {total} Bangunan (Merah: A, Kuning: B, Cyan: C)", fontsize=13)
ax[1].axis('off')

plt.tight_layout()
summary_path = os.path.join(OUTPUT_DIR, "summary_comparison.png")
plt.savefig(summary_path, dpi=200)
plt.close()

print(f"Output disimpan ke: {final_path}")
print(f"Ringkasan visual: {summary_path}")
