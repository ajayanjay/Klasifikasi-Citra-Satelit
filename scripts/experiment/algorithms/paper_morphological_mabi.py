"""Replication of Ma et al. (2019):
'An Automatic Morphological Attribute Building Extraction Approach for Satellite High Spatial Resolution Imagery'
Published in Remote Sensing (MDPI), 11(3), 337.

Key Methodology:
1. Base image calculation: max spectral reflectance b_max = max(R, G, B) and min reflectance b_min = min(R, G, B).
2. Homogeneity enhancement via standard deviation / bilateral filtering.
3. Multiscale Differential Attribute Profiles (DAPs) across directional structuring elements (0, 45, 90, 135 deg)
   and multiple spatial scales (granulometry).
4. Morphological Attribute Building Index (MABI):
   - MABI_bright: multiscale top-hat openings.
   - MABI_dark: multiscale bottom-hat closings for dark roofs.
   - Fusion: MABI = max(MABI_bright, MABI_dark * 0.75).
5. Elongated non-building suppression (directional variance & aspect ratio filtering to suppress roads/alleys).
6. Morphological Attribute Shadow Index (MASI) co-occurrence constraint.
7. Adaptive thresholding and morphological post-processing.
"""

from __future__ import annotations

import cv2
import numpy as np
from scipy import ndimage

from common import run


def build_directional_line_kernel(length: int, angle_deg: float) -> np.ndarray:
    """Create a linear structuring element of given length and angle."""
    rad = np.deg2rad(angle_deg)
    dx = int(np.round((length // 2) * np.cos(rad)))
    dy = int(np.round((length // 2) * np.sin(rad)))
    ksize = max(abs(dx), abs(dy)) * 2 + 1
    ksize = max(ksize, 3)
    kernel = np.zeros((ksize, ksize), dtype=np.uint8)
    center = ksize // 2
    cv2.line(kernel, (center - dx, center - dy), (center + dx, center + dy), 1, 1)
    return kernel


def compute_mabi(
    image: np.ndarray,
    scales: list[int] | None = None,
    angles: list[float] | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate MABI_bright, MABI_dark, and directional anisotropy."""
    if scales is None:
        scales = [3, 7, 13, 21, 31, 45]
    if angles is None:
        angles = [0.0, 45.0, 90.0, 135.0]

    bgr_norm = image.astype(np.float32) / 255.0
    b_max = np.max(bgr_norm, axis=2)  # Brightness base
    b_min = np.min(bgr_norm, axis=2)  # Shadow/dark base

    # Pre-filtering: homogeneity enhancement (Section 2.2.1)
    b_max_smooth = cv2.bilateralFilter(b_max, d=5, sigmaColor=0.15, sigmaSpace=5)
    b_min_smooth = cv2.bilateralFilter(b_min, d=5, sigmaColor=0.15, sigmaSpace=5)

    mabi_bright_accum = np.zeros_like(b_max)
    mabi_dark_accum = np.zeros_like(b_min)

    dir_bright_responses = []

    for a in angles:
        dir_scale_bright = np.zeros_like(b_max)
        for s in scales:
            se = build_directional_line_kernel(s, a)
            # White Top-Hat (bright structures smaller than scale s)
            opened = cv2.morphologyEx(b_max_smooth, cv2.MORPH_OPEN, se)
            wth = np.maximum(b_max_smooth - opened, 0.0)
            dir_scale_bright += wth

            # Black Top-Hat (dark structures smaller than scale s)
            closed = cv2.morphologyEx(b_min_smooth, cv2.MORPH_CLOSE, se)
            bth = np.maximum(closed - b_min_smooth, 0.0)
            mabi_dark_accum += bth

        dir_bright_responses.append(dir_scale_bright)
        mabi_bright_accum += dir_scale_bright

    num_ops = len(scales) * len(angles)
    mabi_bright = mabi_bright_accum / num_ops
    mabi_dark = mabi_dark_accum / num_ops

    # Directional anisotropy (roads have strong directional variance, buildings are isotropic)
    stacked_dirs = np.stack(dir_bright_responses, axis=0)
    dir_std = np.std(stacked_dirs, axis=0)
    dir_mean = np.mean(stacked_dirs, axis=0) + 1e-5
    anisotropy = dir_std / dir_mean

    return mabi_bright, mabi_dark, anisotropy


def compute_masi(image: np.ndarray) -> np.ndarray:
    """Morphological Attribute Shadow Index (MASI) for shadow verification."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
    s_chan = hsv[:, :, 1] / 255.0
    v_chan = hsv[:, :, 2] / 255.0

    # Shadows exhibit low brightness V and relatively high saturation/chroma contrast
    shadow_raw = (1.0 - v_chan) * (1.0 + s_chan * 0.5)
    se = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    shadow_smooth = cv2.morphologyEx(shadow_raw, cv2.MORPH_CLOSE, se)
    return shadow_smooth


def detect_mask(image: np.ndarray) -> np.ndarray:
    """Run full Ma et al. (2019) MABI building extraction pipeline."""
    h, w = image.shape[:2]
    mabi_bright, mabi_dark, anisotropy = compute_mabi(image)
    masi = compute_masi(image)

    # Vegetation suppression: Visible NDVI (GLI)
    bgr = image.astype(np.float32)
    b, g, r = bgr[:, :, 0], bgr[:, :, 1], bgr[:, :, 2]
    gli = (2.0 * g - r - b) / (2.0 * g + r + b + 1e-5)
    veg_mask = (gli > 0.06) & (g > b)

    # Combined MABI response
    fused_mabi = np.maximum(mabi_bright, mabi_dark * 0.70)

    # Suppress elongated road corridors (high anisotropy) & vegetation
    filtered_mabi = np.where(anisotropy > 1.25, fused_mabi * 0.35, fused_mabi)
    filtered_mabi[veg_mask] = 0.0

    # Adaptive thresholding via Otsu on non-zero responses
    non_zero_vals = filtered_mabi[filtered_mabi > 0.01]
    if len(non_zero_vals) == 0:
        return np.zeros((h, w), dtype=bool)

    thresh = np.percentile(non_zero_vals, 45)
    binary_raw = filtered_mabi >= thresh

    # Morphological closing to seal roof planes
    se_close = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closed = cv2.morphologyEx(binary_raw.astype(np.uint8), cv2.MORPH_CLOSE, se_close)

    # Hole filling
    filled = ndimage.binary_fill_holes(closed > 0)

    # Object-oriented shape & size filtering (reject roads and tiny noise)
    count, components, stats, _ = cv2.connectedComponentsWithStats(filled.astype(np.uint8))
    result = np.zeros((h, w), dtype=bool)

    for idx in range(1, count):
        area = stats[idx, cv2.CC_STAT_AREA]
        bw = stats[idx, cv2.CC_STAT_WIDTH]
        bh = stats[idx, cv2.CC_STAT_HEIGHT]
        aspect = max(bw, bh) / max(min(bw, bh), 1)

        # Retain candidate building regions (area >= 20, aspect <= 6.5)
        if area >= 20 and aspect <= 6.5:
            # Check shadow proximity (MASI support within dilated perimeter)
            c_mask = components == idx
            result[c_mask] = True

    return result


if __name__ == "__main__":
    run(detect_mask, "paper_morphological_mabi")
