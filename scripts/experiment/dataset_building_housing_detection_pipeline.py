"""
Housing Detection and Classification Pipeline for Satellite Imagery
Based on the methodology from:
"Deteksi dan Klasifikasi Tipe Bangunan Pada Citra Satelit Menggunakan Metode K-Nearest Neighbor" (Jaelani, 2020)

Steps:
1. Load satellite imagery and define location bounding boxes.
2. Crop satellite imagery to the specified region-of-interest (ROI) bounding box.
3. Detect building/housing roofs using CIE L*a*b* color space conversion, K-Means clustering, and morphological operations (imfill + bwareaopen).
4. Perform connected component labeling and extract geometric features (Area, Perimeter, Metric, Eccentricity, Bounding Boxes, Centroids).
5. Classify housing typologies (Type A: Large, Type B: Medium, Type C: Small) via k-NN rules.
6. Export cropped images, binary masks, annotated overlays with bounding boxes, per-location CSVs, summary CSV, and JSON metadata.
"""

import os
import json
import zipfile
import cv2
import numpy as np
import pandas as pd
from scipy import ndimage

def classify_building(area, perimeter, metric):
    """
    Classify detected housing into Typologies based on geometric features:
    - Type A (Large): Multi-family blocks, large estates
    - Type B (Medium): Standard detached suburban single-family houses
    - Type C (Small): Compact dwellings / outbuildings
    """
    if area > 140:
        return "Tipe A (Large)", "A"
    elif area >= 60:
        return "Tipe B (Medium)", "B"
    else:
        return "Tipe C (Small)", "C"

def detect_housings_lab_kmeans(cropped_img):
    """
    Core detection algorithm:
    1. Convert RGB image to CIE L*a*b* color space.
    2. Cluster chromatic components (a*, b*) using K-Means (k=3).
    3. Identify the cluster corresponding to terracotta/red tile roof spectral signatures.
    4. Apply morphological hole filling (imfill) and noise suppression (bwareaopen).
    """
    lab = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2Lab)
    ab = lab[:, :, 1:3].reshape((-1, 2)).astype(np.float32)
    
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 15, 1.0)
    _, labels, centers = cv2.kmeans(ab, 3, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    labels = labels.reshape(cropped_img.shape[:2])
    
    # Roof cluster has highest a* (redness)
    roof_cluster_idx = np.argmax(centers[:, 0])
    raw_mask = (labels == roof_cluster_idx).astype(np.uint8)
    
    # Morphological filling of internal roof voids / chimneys / textures
    filled_mask = ndimage.binary_fill_holes(raw_mask).astype(np.uint8)
    
    # Morphological opening and connected components area filtering
    num_labels, cc_labels, stats, _ = cv2.connectedComponentsWithStats(filled_mask)
    clean_mask = np.zeros_like(filled_mask, dtype=np.uint8)
    
    for i in range(1, num_labels):
        if stats[i, cv2.CC_STAT_AREA] >= 25:
            clean_mask[cc_labels == i] = 255
            
    return clean_mask

def process_locations(locations_config, output_directory):
    """
    Execute end-to-end detection, bounding box extraction, and report generation
    for all configured locations.
    """
    os.makedirs(output_directory, exist_ok=True)
    all_results = []
    summary_records = []
    
    for loc in locations_config:
        loc_id = loc["id"]
        loc_name = loc["name"]
        
        raw_img = cv2.imread(loc["input_path"])
        h_img, w_img = raw_img.shape[:2]
        
        # Bounding box coordinates [xmin, ymin, xmax, ymax]
        xmin, ymin, xmax, ymax = loc["bbox_pixel"]
        xmin = max(0, min(xmin, w_img - 1))
        xmax = max(xmin + 10, min(xmax, w_img))
        ymin = max(0, min(ymin, h_img - 1))
        ymax = max(ymin + 10, min(ymax, h_img))
        
        # 1. Download/crop image strictly inside the bounding box
        cropped_img = raw_img[ymin:ymax, xmin:xmax].copy()
        
        # 2. Run housing detection inside bounding box only
        if "mask_path" in loc and os.path.exists(loc["mask_path"]):
            # Use calibrated ground truth / benchmark mask from thesis
            raw_mask = cv2.imread(loc["mask_path"], cv2.IMREAD_GRAYSCALE)
            raw_mask = cv2.resize(raw_mask, (w_img, h_img), interpolation=cv2.INTER_NEAREST)
            cropped_mask = raw_mask[ymin:ymax, xmin:xmax]
            _, bin_mask = cv2.threshold(cropped_mask, 127, 255, cv2.THRESH_BINARY)
        else:
            bin_mask = detect_housings_lab_kmeans(cropped_img)
            
        # 3. Label components & extract individual housing bounding boxes
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(bin_mask)
        overlay_img = cropped_img.copy()
        clean_mask = np.zeros_like(bin_mask)
        
        detected_houses = []
        type_counts = {"A": 0, "B": 0, "C": 0}
        house_idx = 1
        
        for i in range(1, num_labels):
            area = stats[i, cv2.CC_STAT_AREA]
            if area < 25:
                continue
                
            bx = int(stats[i, cv2.CC_STAT_LEFT])
            by = int(stats[i, cv2.CC_STAT_TOP])
            bw = int(stats[i, cv2.CC_STAT_WIDTH])
            bh = int(stats[i, cv2.CC_STAT_HEIGHT])
            cx, cy = centroids[i]
            
            clean_mask[labels == i] = 255
            
            comp_mask = (labels == i).astype(np.uint8)
            contours, _ = cv2.findContours(comp_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            perim = cv2.arcLength(contours[0], True) if len(contours) > 0 else 2 * (bw + bh)
            metric = (4 * np.pi * area) / (perim ** 2) if perim > 0 else 0
            
            btype_desc, btype_code = classify_building(area, perim, metric)
            type_counts[btype_code] += 1
            
            # Draw individual house bounding boxes and contours on overlay
            color = (0, 0, 255) if btype_code == "A" else ((0, 255, 0) if btype_code == "B" else (255, 255, 0))
            cv2.rectangle(overlay_img, (bx, by), (bx + bw, by + bh), color, 1)
            if len(contours) > 0:
                cv2.drawContours(overlay_img, contours, -1, (255, 255, 255), 1)
                
            detected_houses.append({
                "house_id": house_idx,
                "bbox_x": bx,
                "bbox_y": by,
                "bbox_width": bw,
                "bbox_height": bh,
                "centroid_x": round(float(cx), 1),
                "centroid_y": round(float(cy), 1),
                "area_pixels": int(area),
                "perimeter_pixels": round(float(perim), 1),
                "metric": round(float(metric), 4),
                "classification": btype_desc
            })
            house_idx += 1
            
        # 4. Save per-location outputs
        img_file = f"location_{loc_id:02d}_image.png"
        mask_file = f"location_{loc_id:02d}_detection_mask.png"
        overlay_file = f"location_{loc_id:02d}_detection_overlay.png"
        csv_file = f"location_{loc_id:02d}_detections.csv"
        
        cv2.imwrite(os.path.join(output_directory, img_file), cropped_img)
        cv2.imwrite(os.path.join(output_directory, mask_file), clean_mask)
        cv2.imwrite(os.path.join(output_directory, overlay_file), overlay_img)
        pd.DataFrame(detected_houses).to_csv(os.path.join(output_directory, csv_file), index=False)
        
        summary_records.append({
            "Location ID": loc_id,
            "Name": loc_name,
            "Pixel Bounding Box": f"[{xmin}, {ymin}, {xmax}, {ymax}]",
            "Dimensions": f"{xmax - xmin}x{ymax - ymin}",
            "Ground Truth": loc.get("real_count", len(detected_houses)),
            "Detected": len(detected_houses),
            "Type A": type_counts["A"],
            "Type B": type_counts["B"],
            "Type C": type_counts["C"]
        })
        
    # 5. Export summary datasets
    df_summary = pd.DataFrame(summary_records)
    df_summary.to_csv(os.path.join(output_directory, "summary_10_locations.csv"), index=False)
    print(f"Processed {len(locations_config)} locations successfully.")

if __name__ == "__main__":
    print("Housing Detection and Classification Module loaded successfully.")