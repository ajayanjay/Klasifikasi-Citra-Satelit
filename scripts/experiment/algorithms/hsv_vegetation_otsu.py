"""Support candidate: HSV vegetation suppression followed by Otsu segmentation."""

import cv2
import numpy as np

from common import run


def detect_mask(image: np.ndarray) -> np.ndarray:
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    vegetation = cv2.inRange(hsv, (25, 35, 20), (95, 255, 255)) > 0
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, bright = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    mask = (bright > 0) & ~vegetation
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return mask > 0


if __name__ == "__main__":
    run(detect_mask, "hsv_vegetation_otsu")
