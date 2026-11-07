"""Shared dataset runner. Algorithm files only define detect_mask()."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np


def run(detect_mask, name: str) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("dataset/raw"))
    parser.add_argument("--output", type=Path, default=Path("output_results") / name)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    for image_path in sorted(args.input.glob("location_*_image.png")):
        image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
        if image is None:
            raise FileNotFoundError(image_path)
        mask = detect_mask(image)
        if mask.shape != image.shape[:2]:
            raise ValueError(f"Algorithm returned wrong shape for {image_path.name}")
        mask = np.where(mask, 255, 0).astype(np.uint8)
        output_name = image_path.name.replace("_image.png", "_detection_mask.png")
        cv2.imwrite(str(args.output / output_name), mask)
    print(f"Wrote masks to {args.output}")
