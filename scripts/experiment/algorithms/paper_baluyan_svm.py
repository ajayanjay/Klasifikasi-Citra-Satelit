"""Replication of Baluyan et al. (2013):
'Novel Approach for Rooftop Detection Using Support Vector Machine'
Published in ISRN Machine Vision.

Key Methodology:
1. Bilateral filtering for edge-preserving noise smoothing.
2. K-means clustering (k=4) in RGB color space to produce candidate roof segments.
3. Connected-component labeling for discrete candidate region extraction.
4. 8-dimensional geometric and spectral feature vector per candidate:
   - Area (A)
   - Perimeter (P)
   - Visible Vegetation Index (VVI)
   - Solidity (S = Area / ConvexHullArea)
   - Mean Grayscale Intensity
   - Variance of Grayscale Intensity
   - Extent (Area / BoundingBoxArea)
   - Eccentricity (from fitted ellipse or central moments)
5. Pass 1: Support Vector Machine (SVM with RBF kernel) classification.
6. Pass 2: Histogram Method (rooftop intensity distribution refinement to recover
   misclassified rooftop candidates with building-like geometry).
"""

from __future__ import annotations

import cv2
import numpy as np
from scipy import ndimage
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from common import run


def compute_vvi(bgr: np.ndarray) -> float:
    """Visible Vegetation Index (Eq. 1 in Baluyan 2013).
    Reference green: R0=30, G0=150, B0=30, weight W=1.
    """
    b = float(bgr[0])
    g = float(bgr[1])
    r = float(bgr[2])
    v_r = max(0.0, 1.0 - abs(r - 30.0) / (r + 30.0 + 1e-4))
    v_g = max(0.0, 1.0 - abs(g - 150.0) / (g + 150.0 + 1e-4))
    v_b = max(0.0, 1.0 - abs(b - 30.0) / (b + 30.0 + 1e-4))
    return float(v_r * v_g * v_b)


def extract_segment_features(
    image: np.ndarray, gray: np.ndarray, label_mask: np.ndarray, min_area: int = 15
) -> tuple[list[list[float]], list[np.ndarray], list[int]]:
    """Extract 8 features for each connected component in label_mask."""
    count, labels, stats, _ = cv2.connectedComponentsWithStats(label_mask.astype(np.uint8))
    h, w = label_mask.shape
    max_area = int(h * w * 0.75)

    features = []
    masks = []
    indices = []

    for idx in range(1, count):
        area = int(stats[idx, cv2.CC_STAT_AREA])
        if area < min_area or area > max_area:
            continue

        c_mask = (labels == idx).astype(np.uint8)
        cnts, _ = cv2.findContours(c_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not cnts:
            continue
        cnt = cnts[0]

        perimeter = float(cv2.arcLength(cnt, True))
        if perimeter <= 0:
            continue

        hull = cv2.convexHull(cnt)
        hull_area = max(cv2.contourArea(hull), 1.0)
        solidity = float(area / hull_area)

        bw = stats[idx, cv2.CC_STAT_WIDTH]
        bh = stats[idx, cv2.CC_STAT_HEIGHT]
        extent = float(area / max(bw * bh, 1.0))

        # Pixel intensities
        pix_gray = gray[labels == idx]
        mean_int = float(np.mean(pix_gray))
        var_int = float(np.var(pix_gray))

        # Visible Vegetation Index
        mean_bgr = np.mean(image[labels == idx], axis=0)
        vvi = compute_vvi(mean_bgr)

        # Eccentricity
        if len(cnt) >= 5:
            try:
                ellipse = cv2.fitEllipse(cnt)
                (_, _), (d1, d2), _ = ellipse
                minor = min(d1, d2)
                major = max(d1, d2)
                ecc = float(np.sqrt(max(0.0, 1.0 - (minor / max(major, 1e-4)) ** 2)))
            except Exception:
                ecc = 0.5
        else:
            ecc = 0.5

        features.append([
            float(area),
            float(perimeter),
            float(vvi),
            float(solidity),
            float(mean_int),
            float(var_int),
            float(extent),
            float(ecc),
        ])
        masks.append(c_mask > 0)
        indices.append(idx)

    return features, masks, indices


def train_reference_svm() -> tuple[SVC, StandardScaler] | None:
    """Train reference SVM classifier on high-confidence structural building rules."""
    # Synthetic / representative reference patterns covering standard rooftop vs background
    # Features: [area, perimeter, vvi, solidity, mean_int, var_int, extent, ecc]
    pos_samples = [
        [150.0, 50.0, 0.05, 0.85, 140.0, 15.0, 0.70, 0.50],
        [350.0, 80.0, 0.08, 0.90, 160.0, 20.0, 0.75, 0.40],
        [800.0, 120.0, 0.02, 0.88, 110.0, 25.0, 0.65, 0.60],
        [220.0, 65.0, 0.12, 0.80, 180.0, 18.0, 0.60, 0.70],
        [500.0, 95.0, 0.04, 0.92, 130.0, 12.0, 0.78, 0.45],
        [120.0, 45.0, 0.06, 0.82, 155.0, 22.0, 0.68, 0.55],
        [600.0, 105.0, 0.03, 0.86, 125.0, 30.0, 0.62, 0.65],
    ]
    neg_samples = [
        # Vegetation / tree
        [400.0, 150.0, 0.65, 0.45, 75.0, 80.0, 0.35, 0.75],
        [180.0, 90.0, 0.72, 0.40, 60.0, 95.0, 0.30, 0.80],
        # Long narrow road / alley
        [1200.0, 500.0, 0.15, 0.25, 95.0, 40.0, 0.18, 0.98],
        [800.0, 420.0, 0.10, 0.30, 105.0, 35.0, 0.22, 0.96],
        # Tiny noisy artifacts / soil
        [20.0, 25.0, 0.20, 0.55, 80.0, 65.0, 0.40, 0.85],
        [1500.0, 650.0, 0.05, 0.22, 115.0, 55.0, 0.15, 0.99],
    ]
    X = np.array(pos_samples + neg_samples, dtype=np.float32)
    y = np.array([1] * len(pos_samples) + [0] * len(neg_samples), dtype=int)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    svm = SVC(kernel="rbf", C=5.0, gamma="scale", probability=True, random_state=42)
    svm.fit(X_scaled, y)
    return svm, scaler


_GLOBAL_SVM, _GLOBAL_SCALER = train_reference_svm()


def detect_mask(image: np.ndarray) -> np.ndarray:
    """Execute Baluyan et al. (2013) 2-pass detection pipeline."""
    h, w = image.shape[:2]
    # 1. Bilateral filter for noise reduction while maintaining edges
    smoothed = cv2.bilateralFilter(image, d=5, sigmaColor=40, sigmaSpace=40)
    gray = cv2.cvtColor(smoothed, cv2.COLOR_BGR2GRAY)

    # 2. K-means clustering (k=4) in RGB space
    pixels = smoothed.reshape(-1, 3).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 25, 0.5)
    _, labels_flat, _ = cv2.kmeans(pixels, 4, None, criteria, 5, cv2.KMEANS_PP_CENTERS)
    cluster_labels = labels_flat.reshape(h, w)

    # 3. Extract candidate segments and features
    all_features: list[list[float]] = []
    all_masks: list[np.ndarray] = []

    for c in range(4):
        c_mask = cluster_labels == c
        feats, masks, _ = extract_segment_features(smoothed, gray, c_mask, min_area=15)
        all_features.extend(feats)
        all_masks.extend(masks)

    if not all_features:
        return np.zeros((h, w), dtype=bool)

    X = np.array(all_features, dtype=np.float32)

    # 4. Pass 1: SVM Classification
    X_scaled = _GLOBAL_SCALER.transform(X)
    probs = _GLOBAL_SVM.predict_proba(X_scaled)[:, 1]
    pass1_pred = probs >= 0.5

    # Also apply direct heuristic guard: reject strong vegetation or extreme elongation
    for i, f in enumerate(all_features):
        vvi, solidity, extent, ecc = f[2], f[3], f[6], f[7]
        if vvi > 0.35 or solidity < 0.40 or extent < 0.20 or ecc > 0.95:
            pass1_pred[i] = False
        elif solidity > 0.75 and extent > 0.50 and vvi < 0.15 and ecc < 0.88:
            pass1_pred[i] = True

    # 5. Pass 2: Histogram Method (intensity distribution refinement)
    # Collect intensities of rooftops detected in Pass 1
    detected_intensities = [
        all_features[i][4] for i in range(len(all_features)) if pass1_pred[i]
    ]

    pass2_pred = np.array(pass1_pred, copy=True)
    if detected_intensities:
        hist_min = np.percentile(detected_intensities, 5)
        hist_max = np.percentile(detected_intensities, 95)

        for i, f in enumerate(all_features):
            if pass2_pred[i]:
                continue
            mean_int = f[4]
            vvi, solidity, extent, ecc = f[2], f[3], f[6], f[7]
            # Check if intensity falls within true rooftop histogram bounds
            # AND geometry matches compact rectangular shape
            if hist_min <= mean_int <= hist_max:
                if solidity >= 0.65 and extent >= 0.35 and vvi < 0.20 and ecc <= 0.88:
                    pass2_pred[i] = True

    # 6. Assemble final binary mask
    building_mask = np.zeros((h, w), dtype=bool)
    for i in range(len(all_masks)):
        if pass2_pred[i]:
            building_mask |= all_masks[i]

    # Fill small interior holes and clean
    building_mask = ndimage.binary_fill_holes(building_mask)
    count, components, stats, _ = cv2.connectedComponentsWithStats(
        building_mask.astype(np.uint8)
    )
    result = np.zeros((h, w), dtype=bool)
    for index in range(1, count):
        area = stats[index, cv2.CC_STAT_AREA]
        if area >= 20:
            result[components == index] = True

    return result


if __name__ == "__main__":
    run(detect_mask, "paper_baluyan_svm")
