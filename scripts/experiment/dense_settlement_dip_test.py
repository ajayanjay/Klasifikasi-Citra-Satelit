"""Dense-settlement building segmentation using classical image processing.

Pipeline:
1. CLAHE + unsharp masking to recover roof boundaries.
2. Canny edges and morphological contour closing.
3. Fill closed roof-like contours.
4. Fuse contour evidence with local roof texture and colour evidence.
5. Reject vegetation, water, long road-like components, and tiny noise.

No labels, machine learning, or sklearn are used. Output is a semantic roof
mask. Completely invisible boundaries cannot be recovered from one image.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import cv2
import numpy as np


def enhance(image: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    lightness, a_channel, b_channel = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(8, 8))
    enhanced_l = clahe.apply(lightness)
    blurred = cv2.GaussianBlur(enhanced_l, (0, 0), 1.15)
    sharpened_l = cv2.addWeighted(enhanced_l, 1.65, blurred, -0.65, 0)
    enhanced_lab = cv2.merge((sharpened_l, a_channel, b_channel))
    enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    return enhanced, sharpened_l


def percentile_scale(values: np.ndarray, low: float = 2, high: float = 98) -> np.ndarray:
    lo, hi = np.percentile(values, (low, high))
    return np.clip((values - lo) / max(float(hi - lo), 1e-6), 0, 1)


def local_std(gray: np.ndarray, size: int = 9) -> np.ndarray:
    mean = cv2.boxFilter(gray, -1, (size, size), normalize=True)
    squared_mean = cv2.boxFilter(gray * gray, -1, (size, size), normalize=True)
    return np.sqrt(np.maximum(squared_mean - mean * mean, 0))


def roof_contours(edges: np.ndarray, shape: tuple[int, int]) -> np.ndarray:
    # Close short roof gaps while avoiding long road corridors.
    closed = cv2.morphologyEx(
        edges,
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)),
        iterations=2,
    )
    contours, _ = cv2.findContours(closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    result = np.zeros(shape, dtype=np.uint8)
    height, width = shape
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 25 or area > 12000:
            continue
        x, y, box_width, box_height = cv2.boundingRect(contour)
        if box_width < 4 or box_height < 4:
            continue
        aspect = max(box_width, box_height) / min(box_width, box_height)
        perimeter = cv2.arcLength(contour, True)
        if perimeter <= 0:
            continue
        compactness = 4 * np.pi * area / (perimeter * perimeter)
        hull_area = cv2.contourArea(cv2.convexHull(contour))
        solidity = area / max(hull_area, 1)
        extent = area / (box_width * box_height)
        # Reject road-like strips and irregular river banks.
        if aspect > 6.0 or compactness < 0.08 or solidity < 0.35 or extent < 0.16:
            continue
        cv2.drawContours(result, [contour], -1, 255, cv2.FILLED)
        if x <= 2 or y <= 2 or x + box_width >= width - 2 or y + box_height >= height - 2:
            continue
    return result > 0


def remove_bad_components(mask: np.ndarray) -> np.ndarray:
    count, labels, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8))
    result = np.zeros(mask.shape, dtype=np.uint8)
    for index in range(1, count):
        area = stats[index, cv2.CC_STAT_AREA]
        width = stats[index, cv2.CC_STAT_WIDTH]
        height = stats[index, cv2.CC_STAT_HEIGHT]
        aspect = max(width, height) / max(min(width, height), 1)
        if area < 20 or (aspect > 9 and area < 6000):
            continue
        result[labels == index] = 255
    return result


def detect_boxes(mask: np.ndarray) -> tuple[np.ndarray, list[dict[str, float]]]:
    count, labels, stats, centroids = cv2.connectedComponentsWithStats(
        (mask > 0).astype(np.uint8)
    )
    boxes = []
    for index in range(1, count):
        x = int(stats[index, cv2.CC_STAT_LEFT])
        y = int(stats[index, cv2.CC_STAT_TOP])
        width = int(stats[index, cv2.CC_STAT_WIDTH])
        height = int(stats[index, cv2.CC_STAT_HEIGHT])
        area = int(stats[index, cv2.CC_STAT_AREA])
        touches_border = x == 0 or y == 0 or x + width >= mask.shape[1] or y + height >= mask.shape[0]
        if (
            area < 50
            or area > 8000
            or width > 180
            or height > 180
            or touches_border
            or max(width, height) / max(min(width, height), 1) > 6
        ):
            continue
        boxes.append({
            "id": len(boxes) + 1,
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "area_pixels": area,
            "center_x": round(float(centroids[index][0]), 2),
            "center_y": round(float(centroids[index][1]), 2),
            "aspect_ratio": round(width / max(height, 1), 4),
        })

    visualization = np.zeros((*mask.shape, 3), dtype=np.uint8)
    for box in boxes:
        x, y = box["x"], box["y"]
        width = max(box["width"], box["height"])
        height = width
        # Cyan: forced square box. Red: original axis-aligned rectangle.
        cv2.rectangle(visualization, (x, y), (x + box["width"], y + box["height"]), (0, 0, 255), 1)
        cv2.rectangle(visualization, (x, y), (x + width, y + height), (255, 255, 0), 1)
        cv2.putText(
            visualization,
            str(box["id"]),
            (x, max(y - 2, 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.35,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )
    return visualization, boxes


def detect_buildings(image: np.ndarray) -> dict[str, np.ndarray]:
    enhanced, sharpened_l = enhance(image)
    hsv = cv2.cvtColor(enhanced, cv2.COLOR_BGR2HSV)
    lab = cv2.cvtColor(enhanced, cv2.COLOR_BGR2LAB)
    gray = sharpened_l.astype(np.float32) / 255
    hue, saturation, value = cv2.split(hsv)

    green = (
        ((hue >= 25) & (hue <= 95) & (saturation >= 35) & (value >= 30))
        | ((enhanced[:, :, 1].astype(np.int16)
            - (enhanced[:, :, 2].astype(np.int16) + enhanced[:, :, 0].astype(np.int16)) // 2) > 18)
    )
    green = cv2.morphologyEx(
        green.astype(np.uint8),
        cv2.MORPH_OPEN,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)),
    ) > 0

    # River/water is dark, smooth, and blue-green. Roads are handled later by
    # elongated-component rejection rather than a brittle colour threshold.
    water = (hue >= 80) & (hue <= 135) & (saturation < 155) & (value < 150)
    non_building_colour = cv2.GaussianBlur(
        (~(green | water)).astype(np.float32), (0, 0), 1.5
    )

    texture = percentile_scale(local_std(gray))
    edges = cv2.Canny(sharpened_l, 35, 105)
    edge_density = cv2.boxFilter(edges.astype(np.float32) / 255, -1, (7, 7), normalize=True)
    edge_score = percentile_scale(edge_density)
    contour_mask = roof_contours(edges, gray.shape)

    # Multiscale top-hat/black-hat responses recover roof interiors whose
    # boundaries are weak after image compression.
    roof_response = np.zeros(gray.shape, dtype=np.float32)
    for kernel_size in (9, 15, 25):
        kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, (kernel_size, kernel_size)
        )
        bright = cv2.morphologyEx(sharpened_l, cv2.MORPH_TOPHAT, kernel)
        dark = cv2.morphologyEx(sharpened_l, cv2.MORPH_BLACKHAT, kernel)
        roof_response = np.maximum(roof_response, (bright + dark) / 255.0)
    roof_response = percentile_scale(roof_response)

    roof_colour = (
        (non_building_colour > 0.50)
        & (value > 45)
        & ~((saturation < 25) & (value < 75))
    )
    local_roof = (roof_response > 0.10) | (texture > 0.16) | (edge_score > 0.10)

    # Roofs have local structure and non-vegetation colours. Contours act as
    # high-confidence support, not as the only source of building pixels.
    evidence = (
        0.35 * roof_response
        + 0.25 * contour_mask.astype(np.float32)
        + 0.20 * edge_score
        + 0.20 * non_building_colour
    )
    evidence = cv2.GaussianBlur(evidence, (0, 0), 0.8)
    local_mean = cv2.boxFilter(evidence, -1, (25, 25), normalize=True)
    adaptive = evidence > (local_mean - 0.02)

    candidate = (
        ((contour_mask & adaptive) | (roof_colour & local_roof & adaptive))
        & roof_colour
        & (gray > 0.12)
    )
    candidate = cv2.morphologyEx(
        candidate.astype(np.uint8),
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
        iterations=1,
    )
    mask = remove_bad_components(candidate > 0)

    return {
        "enhanced": enhanced,
        "mask": mask,
        "evidence": evidence,
        "roof_response": roof_response,
        "contours": contour_mask.astype(np.uint8) * 255,
        "edges": edges,
        "vegetation_water": ((green | water).astype(np.uint8) * 255),
        "adaptive_threshold": np.clip(local_mean + 0.04, 0, 1),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output_results") / "dense_settlement_dip_test",
    )
    args = parser.parse_args()
    image = cv2.imread(str(args.input), cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(args.input)
    args.output.mkdir(parents=True, exist_ok=True)

    products = detect_buildings(image)
    stem = args.input.stem
    box_visualization, boxes = detect_boxes(products["mask"])
    cv2.imwrite(str(args.output / f"{stem}_sharpened.png"), products["enhanced"])
    cv2.imwrite(str(args.output / f"{stem}_building_mask.png"), products["mask"])
    cv2.imwrite(str(args.output / f"{stem}_contour_mask.png"), products["contours"])
    cv2.imwrite(str(args.output / f"{stem}_edge_map.png"), products["edges"])
    cv2.imwrite(str(args.output / f"{stem}_vegetation_water_mask.png"), products["vegetation_water"])
    cv2.imwrite(str(args.output / f"{stem}_roof_response.png"),
                (products["roof_response"] * 255).astype(np.uint8))
    cv2.imwrite(str(args.output / f"{stem}_evidence.png"), (products["evidence"] * 255).astype(np.uint8))
    cv2.imwrite(
        str(args.output / f"{stem}_adaptive_threshold.png"),
        (products["adaptive_threshold"] * 255).astype(np.uint8),
    )
    cv2.imwrite(str(args.output / f"{stem}_boxes.png"), box_visualization)
    with (args.output / f"{stem}_boxes.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "id", "x", "y", "width", "height", "area_pixels",
            "center_x", "center_y", "aspect_ratio",
        ])
        writer.writeheader()
        writer.writerows(boxes)
    boxes_overlay = image.copy()
    boxes_overlay[products["mask"] > 0] = (
        0.65 * boxes_overlay[products["mask"] > 0] + 0.35 * np.array([0, 180, 255])
    ).astype(np.uint8)
    boxes_overlay = cv2.addWeighted(boxes_overlay, 0.78, box_visualization, 0.90, 0)
    cv2.imwrite(str(args.output / f"{stem}_boxes_overlay.png"), boxes_overlay)
    overlay = image.copy()
    selected = products["mask"] > 0
    overlay[selected] = (
        0.55 * overlay[selected] + 0.45 * np.array([0, 220, 255])
    ).astype(np.uint8)
    cv2.imwrite(str(args.output / f"{stem}_overlay.png"), overlay)
    print(f"Wrote products to {args.output}")


if __name__ == "__main__":
    main()
