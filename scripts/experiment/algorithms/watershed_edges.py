"""Support candidate: Canny edges, morphological regions, distance watershed."""

import cv2
import numpy as np

from common import run


def detect_mask(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 40, 120)
    regions = cv2.morphologyEx(
        cv2.bitwise_not(edges),
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)),
    )
    _, regions = cv2.threshold(regions, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    distance = cv2.distanceTransform(regions, cv2.DIST_L2, 5)
    _, foreground = cv2.threshold(distance, 0.35 * distance.max(), 255, 0)
    markers = cv2.connectedComponents(foreground.astype(np.uint8))[1] + 1
    markers[regions == 0] = 0
    markers = cv2.watershed(image, markers)
    return markers > 1


if __name__ == "__main__":
    run(detect_mask, "watershed_edges")
