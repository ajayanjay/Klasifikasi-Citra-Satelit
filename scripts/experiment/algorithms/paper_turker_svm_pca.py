"""Replication of Turker & Koc-San (2010):
'Building Detection from Pan-Sharpened IKONOS Imagery Through Support Vector Machines Classification'
Published in ISPRS Commission VIII / WG VIII/8.

Key Methodology:
1. Multi-feature pixel stack:
   - Spectral bands: Red, Green, Blue.
   - Vegetation band: GLI / Visible NDVI: (2G - R - B) / (2G + R + B).
   - Chromatic color channels: CIELAB (L*, a*, b*).
   - Spatial Texture: Local standard deviation / box filter variance.
2. Support Vector Machine (SVM with RBF kernel) pixel-level classification.
3. Morphological Post-Processing:
   - Morphological opening to eliminate isolated pixel classification noise.
   - Morphological closing to coalesce fragmented roof segments.
   - Hole filling for solid interior roof representation.
   - Connected component area & elongation filtering to reject road corridors.
"""

from __future__ import annotations

import cv2
import numpy as np
from scipy import ndimage
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from common import run


def compute_feature_stack(image: np.ndarray) -> np.ndarray:
    """Generate 7-channel multi-spectral, color, and texture feature stack."""
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]

    # 1. Vegetation Index: Green Leaf Index (GLI)
    gli = (2.0 * g - r - b) / (2.0 * g + r + b + 1e-5)

    # 2. CIE L*a*b* color representation
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2Lab).astype(np.float32)
    l_norm = lab[:, :, 0] / 255.0
    a_norm = lab[:, :, 1] / 255.0
    b_norm = lab[:, :, 2] / 255.0

    # 3. Local Texture: Standard deviation in 7x7 neighborhood
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
    mean_val = cv2.boxFilter(gray, -1, (7, 7))
    sq_mean = cv2.boxFilter(gray * gray, -1, (7, 7))
    tex = np.sqrt(np.maximum(sq_mean - mean_val * mean_val, 0.0))

    feature_stack = np.dstack([
        r,
        g,
        b,
        gli[:, :, None],
        a_norm[:, :, None],
        b_norm[:, :, None],
        tex[:, :, None],
    ])
    return feature_stack


def build_trained_turker_svm() -> tuple[SVC, StandardScaler]:
    """Train reference SVM classifier on characteristic satellite surface signatures."""
    # Representative samples for satellite roof vs background
    # Features: [r, g, b, gli, a_norm, b_norm, tex]
    roof_samples = [
        [0.65, 0.55, 0.50, -0.05, 0.52, 0.53, 0.04],  # terracotta / orange roof
        [0.80, 0.70, 0.65, -0.04, 0.51, 0.52, 0.03],  # bright ceramic roof
        [0.45, 0.45, 0.48, -0.01, 0.49, 0.48, 0.05],  # metal / zinc sheet roof
        [0.55, 0.52, 0.48,  0.01, 0.50, 0.51, 0.02],  # concrete flat roof
        [0.72, 0.62, 0.55, -0.06, 0.53, 0.54, 0.04],  # clay tile roof
        [0.38, 0.40, 0.42,  0.00, 0.49, 0.49, 0.06],  # gray weathered roof
        [0.58, 0.58, 0.56,  0.01, 0.50, 0.50, 0.02],  # uniform pale roof
    ]
    non_roof_samples = [
        [0.20, 0.45, 0.15,  0.35, 0.42, 0.58, 0.12],  # green vegetation / tree canopy
        [0.15, 0.35, 0.10,  0.40, 0.40, 0.60, 0.15],  # dense foliage
        [0.25, 0.25, 0.28, -0.03, 0.50, 0.48, 0.08],  # asphalt dark road
        [0.10, 0.10, 0.12, -0.05, 0.49, 0.48, 0.02],  # deep cast shadow
        [0.08, 0.12, 0.18,  0.02, 0.48, 0.42, 0.01],  # water / puddle
        [0.35, 0.35, 0.33,  0.01, 0.50, 0.50, 0.09],  # road shoulder / rough gravel
        [0.48, 0.45, 0.38,  0.02, 0.51, 0.55, 0.10],  # dry bare soil / sand
    ]
    X = np.array(roof_samples + non_roof_samples, dtype=np.float32)
    y = np.array([1] * len(roof_samples) + [0] * len(non_roof_samples), dtype=int)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    svm = SVC(kernel="rbf", C=10.0, gamma="scale", random_state=42)
    svm.fit(X_scaled, y)
    return svm, scaler


_GLOBAL_TURKER_SVM, _GLOBAL_TURKER_SCALER = build_trained_turker_svm()


def detect_mask(image: np.ndarray) -> np.ndarray:
    """Execute Turker & Koc-San (2010) SVM classification & morphology pipeline."""
    h, w = image.shape[:2]
    feats = compute_feature_stack(image)
    flat_feats = feats.reshape(-1, 7)

    # 1. Pixel-level SVM Classification
    flat_scaled = _GLOBAL_TURKER_SCALER.transform(flat_feats)
    pred_labels = _GLOBAL_TURKER_SVM.predict(flat_scaled)
    raw_mask = pred_labels.reshape(h, w).astype(np.uint8)

    # 2. Vegetation & Shadow exclusion
    rgb = feats[:, :, :3]
    gli = feats[:, :, 3]
    veg_mask = (gli > 0.07) & (rgb[:, :, 1] > rgb[:, :, 0])
    raw_mask[veg_mask] = 0

    # 3. Morphological Post-Processing (Section 2 & 5)
    # Opening to eliminate isolated single pixels
    se_open = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    cleaned = cv2.morphologyEx(raw_mask, cv2.MORPH_OPEN, se_open)

    # Closing to merge broken roof partitions
    se_close = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, se_close)

    # Hole filling for solid roof interiors
    filled = ndimage.binary_fill_holes(closed > 0)

    # Connected component filtering: reject small noise (< 25 px) and elongated linear roads
    count, components, stats, _ = cv2.connectedComponentsWithStats(filled.astype(np.uint8))
    result = np.zeros((h, w), dtype=bool)

    for idx in range(1, count):
        area = stats[idx, cv2.CC_STAT_AREA]
        bw = stats[idx, cv2.CC_STAT_WIDTH]
        bh = stats[idx, cv2.CC_STAT_HEIGHT]
        aspect = max(bw, bh) / max(min(bw, bh), 1)

        if area >= 25 and aspect <= 7.0:
            result[components == idx] = True

    return result


if __name__ == "__main__":
    run(detect_mask, "paper_turker_svm_pca")
