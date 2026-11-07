"""Main paper candidate: CIE Lab a/b K-Means, hole filling, area filtering."""

import cv2
import numpy as np
from scipy import ndimage

from common import run


def detect_mask(image: np.ndarray) -> np.ndarray:
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    chroma = lab[:, :, 1:3].reshape(-1, 2).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.2)
    _, labels, centers = cv2.kmeans(chroma, 3, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
    labels = labels.reshape(image.shape[:2])
    mask = labels == int(np.argmax(centers[:, 0]))
    mask = ndimage.binary_fill_holes(mask)
    count, components, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8))
    result = np.zeros(mask.shape, dtype=bool)
    for index in range(1, count):
        if stats[index, cv2.CC_STAT_AREA] >= 25:
            result[components == index] = True
    return result


if __name__ == "__main__":
    run(detect_mask, "paper_lab_kmeans")
