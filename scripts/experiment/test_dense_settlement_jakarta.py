"""Comprehensive evaluation script testing all Key Paper algorithms on dense settlement Jakarta.

Algorithms tested:
1. Adam Jaelani (2020) - CIELab K-Means & Morphological Filtering
2. Baluyan et al. (2013) - Bilateral Filter + K-Means + 8D Geometric SVM + 2-Pass Histogram
3. Ma et al. (2019) - Multiscale Directional Morphological Attribute Building Index (MABI)
4. Turker & Koc-San (2010) - Multispectral + GLI + Texture Pixel SVM Classifier

Target dataset: dataset/temp/data_test_narrow_jakarta_1.jpg
Output directory: output_results/jakarta_dense_settlement_comparison/
"""

from __future__ import annotations

import csv
import sys
import time
from pathlib import Path

import cv2
import numpy as np

# Ensure algorithms package is importable
CURRENT_DIR = Path(__file__).resolve().parent
ALGORITHMS_DIR = CURRENT_DIR / "algorithms"
if str(ALGORITHMS_DIR) not in sys.path:
    sys.path.insert(0, str(ALGORITHMS_DIR))

from paper_baluyan_svm import detect_mask as detect_baluyan_svm  # noqa: E402
from paper_lab_kmeans import detect_mask as detect_lab_kmeans  # noqa: E402
from paper_morphological_mabi import detect_mask as detect_mabi  # noqa: E402
from paper_turker_svm_pca import detect_mask as detect_turker  # noqa: E402


def extract_building_stats(mask: np.ndarray) -> tuple[list[dict[str, float]], np.ndarray]:
    """Extract individual building bounding boxes and properties."""
    count, labels, stats, centroids = cv2.connectedComponentsWithStats(mask.astype(np.uint8))
    buildings = []
    contour_canvas = np.zeros((*mask.shape, 3), dtype=np.uint8)

    for idx in range(1, count):
        area = int(stats[idx, cv2.CC_STAT_AREA])
        if area < 15:
            continue
        x = int(stats[idx, cv2.CC_STAT_LEFT])
        y = int(stats[idx, cv2.CC_STAT_TOP])
        w = int(stats[idx, cv2.CC_STAT_WIDTH])
        h = int(stats[idx, cv2.CC_STAT_HEIGHT])
        cx, cy = float(centroids[idx][0]), float(centroids[idx][1])
        aspect = float(max(w, h) / max(min(w, h), 1))

        # Find contour for solidity
        c_mask = (labels == idx).astype(np.uint8)
        cnts, _ = cv2.findContours(c_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        solidity = 1.0
        if cnts:
            hull = cv2.convexHull(cnts[0])
            hull_area = max(cv2.contourArea(hull), 1.0)
            solidity = float(area / hull_area)
            cv2.drawContours(contour_canvas, cnts, -1, (0, 255, 255), 1)

        buildings.append({
            "id": idx,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "area_pixels": area,
            "center_x": round(cx, 2),
            "center_y": round(cy, 2),
            "aspect_ratio": round(aspect, 2),
            "solidity": round(solidity, 3),
        })

    return buildings, contour_canvas


def create_overlay(image: np.ndarray, mask: np.ndarray, color=(0, 215, 255), alpha=0.45) -> np.ndarray:
    """Create a semi-transparent color overlay of mask over original image."""
    overlay = image.copy()
    building_pixels = mask > 0
    if np.any(building_pixels):
        color_arr = np.array(color, dtype=np.float32)
        blended = (1.0 - alpha) * overlay[building_pixels].astype(np.float32) + alpha * color_arr
        overlay[building_pixels] = blended.astype(np.uint8)
    return overlay


def create_comparison_grid(
    original: np.ndarray,
    results: list[tuple[str, np.ndarray, np.ndarray]],
    title_prefix: str = "Dense Settlement Jakarta",
) -> np.ndarray:
    """Create an annotated side-by-side grid of all algorithm results."""
    # Resize components to uniform tile size
    tile_h, tile_w = 480, 480
    panels = []

    # Original panel
    orig_tile = cv2.resize(original, (tile_w, tile_h), interpolation=cv2.INTER_AREA)
    cv2.putText(
        orig_tile,
        "Original Satellite Image",
        (15, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )
    panels.append(orig_tile)

    # Result panels
    for name, mask, overlay in results:
        tile = cv2.resize(overlay, (tile_w, tile_h), interpolation=cv2.INTER_AREA)
        # Put black background banner for text
        cv2.rectangle(tile, (0, 0), (tile_w, 42), (20, 20, 20), -1)
        cv2.putText(
            tile,
            name,
            (12, 28),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 235, 255),
            2,
            cv2.LINE_AA,
        )
        panels.append(tile)

    # Arrange in 2 rows or 1 row
    # If 5 panels: 2 rows (top: 3, bottom: 2 + blank/legend)
    top_row = np.hstack(panels[:3])
    blank_tile = np.zeros_like(panels[0])
    cv2.putText(
        blank_tile,
        title_prefix,
        (20, 200),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (200, 200, 200),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        blank_tile,
        "PCD & Classical ML",
        (20, 240),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 215, 255),
        2,
        cv2.LINE_AA,
    )
    bottom_row = np.hstack([panels[3], panels[4], blank_tile])
    grid = np.vstack([top_row, bottom_row])
    return grid


def run_evaluation(input_path: Path, output_dir: Path) -> None:
    print(f"Loading test image from: {input_path}")
    image = cv2.imread(str(input_path), cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Cannot load image at {input_path}")

    h, w = image.shape[:2]
    print(f"Image dimensions: {w}x{h} (Total: {w * h / 1e6:.1f} Megapixels)")

    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. High-Resolution Dense Core Crop (1500 x 1500 at native 100% resolution)
    cy, cx = h // 2, w // 2
    crop_size = 1500
    crop_y1, crop_y2 = max(0, cy - crop_size // 2), min(h, cy + crop_size // 2)
    crop_x1, crop_x2 = max(0, cx - crop_size // 2), min(w, cx + crop_size // 2)
    dense_crop = image[crop_y1:crop_y2, crop_x1:crop_x2].copy()

    # 2. Scaled Overview for full scene mapping (width 2048)
    overview_w = 2048
    scale = overview_w / w
    overview_h = int(h * scale)
    overview_image = cv2.resize(image, (overview_w, overview_h), interpolation=cv2.INTER_AREA)

    targets = [
        ("dense_core_crop_1500px", dense_crop),
        ("full_scene_overview_2048px", overview_image),
    ]

    algorithms = [
        (
            "Adam Jaelani (2020) [CIELab K-Means]",
            "paper_lab_kmeans",
            "CIELab + K-Means + Morphology",
            detect_lab_kmeans,
            (0, 165, 255),  # Orange overlay
        ),
        (
            "Baluyan et al. (2013) [SVM 2-Pass]",
            "paper_baluyan_svm",
            "Bilateral + K-Means + 8D SVM + 2-Pass",
            detect_baluyan_svm,
            (0, 255, 128),  # Green-Cyan overlay
        ),
        (
            "Ma et al. (2019) [MABI Morphological]",
            "paper_morphological_mabi",
            "Multiscale Directional MABI + MASI",
            detect_mabi,
            (255, 191, 0),  # Sky blue overlay
        ),
        (
            "Turker & Koc-San (2010) [Multispectral SVM]",
            "paper_turker_svm_pca",
            "GLI + CIELAB + Texture + Pixel SVM",
            detect_turker,
            (180, 105, 255),  # Magenta overlay
        ),
    ]

    summary_rows = []

    for target_name, target_img in targets:
        print(f"\n=======================================================")
        print(f"Processing Target: {target_name} ({target_img.shape[1]}x{target_img.shape[0]})")
        print(f"=======================================================")
        target_dir = output_dir / target_name
        target_dir.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(target_dir / "original.png"), target_img)

        grid_results = []

        for display_name, folder_name, method_desc, detect_fn, overlay_color in algorithms:
            print(f"-> Running {display_name} ...")
            t0 = time.time()
            try:
                mask = detect_fn(target_img)
            except Exception as e:
                print(f"Error in {display_name}: {e}")
                mask = np.zeros(target_img.shape[:2], dtype=bool)
            elapsed = time.time() - t0

            # Statistics & extraction
            buildings, contour_canvas = extract_building_stats(mask)
            total_bldg_pixels = int(np.count_nonzero(mask))
            coverage_pct = (total_bldg_pixels / mask.size) * 100.0
            mean_bldg_area = (
                float(np.mean([b["area_pixels"] for b in buildings])) if buildings else 0.0
            )
            median_aspect = (
                float(np.median([b["aspect_ratio"] for b in buildings])) if buildings else 0.0
            )

            print(
                f"   Done in {elapsed:.2f}s | Detected Buildings: {len(buildings)} | Coverage: {coverage_pct:.2f}%"
            )

            # Visualizations
            mask_u8 = (mask.astype(np.uint8)) * 255
            overlay = create_overlay(target_img, mask, color=overlay_color)
            contour_overlay = target_img.copy()
            contour_overlay = cv2.addWeighted(contour_overlay, 0.85, contour_canvas, 1.0, 0)

            # Save individual algorithm results
            algo_dir = target_dir / folder_name
            algo_dir.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(algo_dir / "mask.png"), mask_u8)
            cv2.imwrite(str(algo_dir / "overlay.png"), overlay)
            cv2.imwrite(str(algo_dir / "contours_overlay.png"), contour_overlay)

            # Save building CSV
            with (algo_dir / "detected_buildings.csv").open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "id",
                        "x",
                        "y",
                        "width",
                        "height",
                        "area_pixels",
                        "center_x",
                        "center_y",
                        "aspect_ratio",
                        "solidity",
                    ],
                )
                writer.writeheader()
                writer.writerows(buildings)

            grid_results.append((display_name, mask_u8, overlay))

            summary_rows.append({
                "target_image": target_name,
                "algorithm": display_name,
                "folder_key": folder_name,
                "method_type": method_desc,
                "runtime_seconds": round(elapsed, 2),
                "buildings_count": len(buildings),
                "total_building_pixels": total_bldg_pixels,
                "coverage_percent": round(coverage_pct, 2),
                "mean_building_area_px": round(mean_bldg_area, 1),
                "median_aspect_ratio": round(median_aspect, 2),
            })

        # Save side-by-side comparison grid
        comparison_grid = create_comparison_grid(
            target_img, grid_results, title_prefix=f"{target_name} Comparison"
        )
        cv2.imwrite(str(target_dir / "comparison_grid.png"), comparison_grid)
        print(f"Saved comparison grid to {target_dir / 'comparison_grid.png'}")

    # Write overall summary CSV
    summary_path = output_dir / "summary_comparison.csv"
    with summary_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "target_image",
                "algorithm",
                "folder_key",
                "method_type",
                "runtime_seconds",
                "buildings_count",
                "total_building_pixels",
                "coverage_percent",
                "mean_building_area_px",
                "median_aspect_ratio",
            ],
        )
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"\n=======================================================")
    print(f"All experiments completed! Summary written to: {summary_path}")
    print(f"=======================================================\n")


if __name__ == "__main__":
    input_file = Path("dataset/temp/data_test_narrow_jakarta_1.jpg")
    output_folder = Path("output_results/jakarta_dense_settlement_comparison")
    run_evaluation(input_file, output_folder)
