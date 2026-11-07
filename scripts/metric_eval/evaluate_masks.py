"""Evaluate predicted building masks against dataset/eval masks.

Usage:
    python scripts/metric_eval/evaluate_masks.py --predictions output_results
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import cv2
import numpy as np


def binary(path: Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(path)
    return image > 0


def scores(pred: np.ndarray, truth: np.ndarray) -> dict[str, float]:
    tp = np.count_nonzero(pred & truth)
    tn = np.count_nonzero(~pred & ~truth)
    fp = np.count_nonzero(pred & ~truth)
    fn = np.count_nonzero(~pred & truth)
    total = pred.size
    return {
        "pixel_accuracy": (tp + tn) / total,
        "balanced_accuracy": ((tp / (tp + fn) if tp + fn else 0.0)
                              + (tn / (tn + fp) if tn + fp else 0.0)) / 2,
        "precision": tp / (tp + fp) if tp + fp else 0.0,
        "recall": tp / (tp + fn) if tp + fn else 0.0,
        "iou": tp / (tp + fp + fn) if tp + fp + fn else 1.0,
        "dice": 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 1.0,
    }


def object_f1(pred: np.ndarray, truth: np.ndarray, threshold: float = 0.5) -> float:
    def components(mask: np.ndarray) -> list[np.ndarray]:
        count, labels, _, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8))
        return [labels == index for index in range(1, count)]

    predicted = components(pred)
    expected = components(truth)
    matched = set()
    true_positives = 0
    for candidate in predicted:
        best_index, best_iou = -1, 0.0
        for index, target in enumerate(expected):
            if index in matched:
                continue
            intersection = np.count_nonzero(candidate & target)
            union = np.count_nonzero(candidate | target)
            iou = intersection / union if union else 0.0
            if iou > best_iou:
                best_index, best_iou = index, iou
        if best_iou >= threshold:
            matched.add(best_index)
            true_positives += 1
    false_positives = len(predicted) - true_positives
    false_negatives = len(expected) - true_positives
    return (2 * true_positives / (2 * true_positives + false_positives + false_negatives)
            if true_positives or false_positives or false_negatives else 1.0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--truth", type=Path, default=Path("dataset/eval"))
    parser.add_argument("--output", type=Path, default=Path("scripts/metric_eval/metrics.csv"))
    args = parser.parse_args()

    rows = []
    for truth_path in sorted(args.truth.glob("*_detection_mask.png")):
        prediction_path = args.predictions / truth_path.name
        if not prediction_path.exists():
            raise FileNotFoundError(f"Missing prediction: {prediction_path}")
        truth, prediction = binary(truth_path), binary(prediction_path)
        if truth.shape != prediction.shape:
            raise ValueError(f"Shape mismatch: {truth_path.name}: {truth.shape} != {prediction.shape}")
        row = {"location": truth_path.stem.replace("_detection_mask", "")}
        row.update(scores(prediction, truth))
        row["object_f1"] = object_f1(prediction, truth)
        rows.append(row)

    if not rows:
        raise ValueError(f"No *_detection_mask.png files found in {args.truth}")
    fields = list(rows[0])
    macro = {"location": "macro_mean"}
    for field in fields[1:]:
        macro[field] = float(np.mean([row[field] for row in rows]))
    rows.append(macro)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {args.output} ({len(rows) - 1} locations)")


if __name__ == "__main__":
    main()
