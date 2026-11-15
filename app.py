import os
import sys
import warnings

os.environ["MPLCONFIGDIR"] = os.path.join(os.environ.get("TEMP", "C:/tmp"), "matplotlib")
warnings.filterwarnings("ignore")

import cv2
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import tifffile as tiff
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch

from analisis_karhutla import (
    CLASS_COLORS,
    CLASS_NAMES,
    DATA_DIR,
    EPOCHS,
    RESULTS_DIR,
    load_dataset,
    spectral_indices,
    stretch_composite,
    valid_mask,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVE_DIR = os.path.join(BASE_DIR, "archive_2019_baseline")
ARCHIVE_DATA_DIR = os.path.join(ARCHIVE_DIR, "data")
ARCHIVE_RESULTS_DIR = os.path.join(ARCHIVE_DIR, "results")

st.set_page_config(
    page_title="Dashboard PCD: Analisis Karhutla & Tutupan Lahan",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main-title {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 2px;
        color: #1a1a1a;
    }
    .sub-title {
        font-size: 13px;
        color: #555555;
        margin-bottom: 14px;
    }
    .kpi-card {
        background-color: #f8f9fa;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 10px 14px;
        margin-bottom: 10px;
    }
    .kpi-title {
        font-size: 11px;
        color: #64748b;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .kpi-number {
        font-size: 20px;
        font-weight: 700;
        color: #0f172a;
    }
    .academic-box {
        border-left: 4px solid #0284c7;
        background-color: #f0f9ff;
        padding: 10px 14px;
        margin-bottom: 12px;
        font-size: 13px;
        color: #0369a1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner="Memuat dataset master citra satelit 10 meter...")
def load_master_environment(roi_name="Kalteng_Sebangau_Kahayan"):
    images, firms_t21, jrc_water, gt_dw, gedi_h, pixel_size_m = load_dataset(roi_name)
    pre = images["2023 Pre"]
    fire = images["2023 Fire"]
    now = images["2026 Y3"]

    valid = {k: valid_mask(img) for k, img in images.items()}
    v_pre = valid["2023 Pre"]
    v_fire = valid["2023 Fire"]
    v_now = valid["2026 Y3"]
    both_valid = v_pre & v_fire

    spec_pre = spectral_indices(pre)
    spec_fire = spectral_indices(fire)
    spec_now = spectral_indices(now)

    dnbr = spec_pre["NBR"] - spec_fire["NBR"]
    dnbr[~both_valid] = 0.0

    land_mask = (jrc_water < 25.0) & (spec_pre["NDWI"] < 0.05)
    pixel_area_ha = (pixel_size_m * pixel_size_m) / 10000.0

    rgb_pre = stretch_composite(pre["b4"], pre["b3"], pre["b2"], v_pre)
    rgb_fire = stretch_composite(fire["b4"], fire["b3"], fire["b2"], v_fire)
    swir_fire = stretch_composite(fire["b12"], fire["b8"], fire["b4"], v_fire)
    rgb_now = stretch_composite(now["b4"], now["b3"], now["b2"], v_now)

    preview_dim = (1000, 1000)
    previews = {
        "rgb_pre": cv2.resize(rgb_pre, preview_dim, interpolation=cv2.INTER_AREA),
        "rgb_fire": cv2.resize(rgb_fire, preview_dim, interpolation=cv2.INTER_AREA),
        "swir_fire": cv2.resize(swir_fire, preview_dim, interpolation=cv2.INTER_AREA),
        "rgb_now": cv2.resize(rgb_now, preview_dim, interpolation=cv2.INTER_AREA),
        "dnbr": cv2.resize(dnbr, preview_dim, interpolation=cv2.INTER_AREA),
        "firms": cv2.resize(firms_t21, preview_dim, interpolation=cv2.INTER_NEAREST),
    }

    cluster_tif_path = os.path.join(DATA_DIR, "Hasil_Klaster_3Kelas_Karhutla.tif")
    if os.path.exists(cluster_tif_path):
        cluster_raster = tiff.imread(cluster_tif_path)
    else:
        cluster_raster = np.zeros(dnbr.shape, dtype=np.uint8)

    previews["cluster"] = cv2.resize(cluster_raster, preview_dim, interpolation=cv2.INTER_NEAREST)

    stats_csv = os.path.join(DATA_DIR, "statistik_klaster_2023_2026.csv")
    traj_csv = os.path.join(DATA_DIR, "trajektori_tahunan_2023_2026.csv")
    df_stats = pd.read_csv(stats_csv) if os.path.exists(stats_csv) else None
    df_traj = pd.read_csv(traj_csv) if os.path.exists(traj_csv) else None

    return {
        "images": images,
        "valid": valid,
        "dnbr": dnbr,
        "firms_t21": firms_t21,
        "land_mask": land_mask,
        "spec_pre": spec_pre,
        "spec_fire": spec_fire,
        "spec_now": spec_now,
        "both_valid": both_valid,
        "pixel_area_ha": pixel_area_ha,
        "cluster_raster": cluster_raster,
        "previews": previews,
        "df_stats": df_stats,
        "df_traj": df_traj,
        "gt_dw": gt_dw,
        "gedi_h": gedi_h,
    }


def compute_live_delineation(
    data,
    dnbr_th=0.20,
    open_size=5,
    close_size=7,
    struct_shape=cv2.MORPH_ELLIPSE,
    use_firms=True,
    firms_th=310.0,
    ndvi_pre_min=0.32,
    min_area_ha=1.0,
):
    pre_veg = (data["spec_pre"]["NDVI"] > ndvi_pre_min) & (data["spec_pre"]["NDBI"] < 0.05)
    raw_burn = data["dnbr"] > dnbr_th

    if use_firms:
        thermal_valid = (data["firms_t21"] > firms_th) | (data["dnbr"] > (dnbr_th + 0.08))
    else:
        thermal_valid = True

    cand = (raw_burn & data["land_mask"] & pre_veg & thermal_valid & data["both_valid"]).astype(np.uint8)

    # Opening (Erosi -> Dilasi) untuk hapus derau bintik
    if open_size > 1:
        k_open = cv2.getStructuringElement(struct_shape, (open_size, open_size))
        opened = cv2.morphologyEx(cand, cv2.MORPH_OPEN, k_open)
    else:
        opened = cand.copy()

    # Closing (Dilasi -> Erosi) untuk tambal rongga internal
    if close_size > 1:
        k_close = cv2.getStructuringElement(struct_shape, (close_size, close_size))
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, k_close)
    else:
        closed = opened.copy()

    pixel_area_ha = data["pixel_area_ha"]
    if min_area_ha > 0:
        min_px = int(round(min_area_ha / pixel_area_ha))
        num_cc, cc_labels, cc_stats, _ = cv2.connectedComponentsWithStats(closed, connectivity=8)
        clean = np.zeros_like(closed, dtype=bool)
        for idx in range(1, num_cc):
            if cc_stats[idx, cv2.CC_STAT_AREA] >= min_px:
                clean[cc_labels == idx] = True
    else:
        clean = closed.astype(bool)

    raw_ha = float(np.sum(cand) * pixel_area_ha)
    opened_ha = float(np.sum(opened) * pixel_area_ha)
    closed_ha = float(np.sum(closed) * pixel_area_ha)
    clean_ha = float(np.sum(clean) * pixel_area_ha)
    noise_ha = max(0.0, raw_ha - clean_ha)
    noise_pct = (noise_ha / raw_ha * 100.0) if raw_ha > 0 else 0.0

    return {
        "cand": cand,
        "opened": opened,
        "closed": closed,
        "clean": clean,
        "raw_ha": raw_ha,
        "opened_ha": opened_ha,
        "closed_ha": closed_ha,
        "clean_ha": clean_ha,
        "noise_ha": noise_ha,
        "noise_pct": noise_pct,
    }


def overlay_mask_contour(base_rgb, mask_full, color_bgr=(0, 255, 255), thickness=2):
    preview_dim = (base_rgb.shape[1], base_rgb.shape[0])
    mask_small = cv2.resize(mask_full.astype(np.uint8), preview_dim, interpolation=cv2.INTER_NEAREST)
    contours, _ = cv2.findContours(mask_small, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    out = (base_rgb * 255.0).astype(np.uint8).copy()
    cv2.drawContours(out, contours, -1, color_bgr, thickness)
    return out


# =============================================================================
# SIDEBAR: NAVIGATION MENU & LIVE PARAMETER TUNING
# =============================================================================
st.sidebar.title("PCD System Navigation")
st.sidebar.caption("Digital Image Processing - D4 Informatics Engineering POLBAN")
st.sidebar.markdown("---")

app_mode = st.sidebar.radio(
    "Select Navigation Mode:",
    [
        "1. Live Parameter Tuning Laboratory (PCD)",
        "2. Full Report & Publication Gallery (7 Figures)",
        "3. Archive Baseline Case Study (2019 - 2025)",
        "4. Cross-Period Comparison (2019 vs 2023)",
    ],
    index=0,
)

data = load_master_environment("Kalteng_Sebangau_Kahayan")

# =============================================================================
# MENU 1: LIVE PARAMETER TUNING LABORATORY (PCD)
# =============================================================================
if app_mode.startswith("1."):
    st.sidebar.markdown("---")
    st.sidebar.subheader("PCD Parameter Sensitivity Controls")

    st.sidebar.markdown("**A. Spectral & Thermal Thresholds:**")
    dnbr_th = st.sidebar.slider(
        "Burn Severity Threshold (dNBR):",
        min_value=0.10,
        max_value=0.35,
        value=0.20,
        step=0.01,
        help="Differenced Normalized Burn Ratio (NBR Pre - NBR Fire). Standard USGS threshold = 0.20.",
    )

    use_firms = st.sidebar.checkbox("NASA FIRMS Thermal Anomaly Filter", value=True)
    if use_firms:
        firms_th = st.sidebar.slider(
            "FIRMS Brightness Temperature T21 (K):",
            min_value=300,
            max_value=335,
            value=310,
            step=1,
            help="MODIS/VIIRS active fire brightness temperature threshold in Kelvin.",
        )
    else:
        firms_th = 300.0

    ndvi_pre_min = st.sidebar.slider(
        "Pre-Fire Baseline NDVI Threshold:",
        min_value=0.20,
        max_value=0.45,
        value=0.32,
        step=0.01,
        help="Ensures candidate burn pixels were vegetated prior to the fire event.",
    )

    st.sidebar.markdown("**B. Mathematical Morphology Parameters:**")
    struct_str = st.sidebar.selectbox(
        "Structuring Element Shape:",
        ["Ellipse (cv2.MORPH_ELLIPSE)", "Rectangle (cv2.MORPH_RECT)", "Cross (cv2.MORPH_CROSS)"],
    )
    if "RECT" in struct_str:
        struct_shape = cv2.MORPH_RECT
    elif "CROSS" in struct_str:
        struct_shape = cv2.MORPH_CROSS
    else:
        struct_shape = cv2.MORPH_ELLIPSE

    open_size = st.sidebar.select_slider(
        "Morphological Opening Kernel Size (Salt-and-Pepper Removal):",
        options=[0, 3, 5, 7, 9],
        value=5,
        help="0 = No Opening. Larger kernels erode isolated commission noise more aggressively.",
    )

    close_size = st.sidebar.select_slider(
        "Morphological Closing Kernel Size (Hole Filling):",
        options=[0, 3, 5, 7, 9, 11],
        value=7,
        help="0 = No Closing. Consolidates fragmented burn scar polygons and fills internal gaps.",
    )

    min_area_ha = st.sidebar.slider(
        "Connected Component Min Area Filter (Ha):",
        min_value=0.0,
        max_value=3.0,
        value=1.0,
        step=0.2,
        help="8-connected component filtering: Removes isolated polygons smaller than X hectares.",
    )

    st.sidebar.markdown("**C. Boundary Overlay Options:**")
    show_contour = st.sidebar.checkbox("Overlay Burn Scar Polygon Contour", value=True)
    color_choice = st.sidebar.selectbox("Contour Line Color:", ["Cyan", "Yellow", "Red"])
    if color_choice.startswith("Cyan"):
        contour_color = (0, 255, 255)
    elif color_choice.startswith("Yellow"):
        contour_color = (255, 255, 0)
    else:
        contour_color = (255, 0, 0)

    # Run live parameter computation
    live_res = compute_live_delineation(
        data,
        dnbr_th=dnbr_th,
        open_size=open_size,
        close_size=close_size,
        struct_shape=struct_shape,
        use_firms=use_firms,
        firms_th=firms_th,
        ndvi_pre_min=ndvi_pre_min,
        min_area_ha=min_area_ha,
    )

    st.markdown(
        "<div class='main-title'>Digital Image Processing (PCD) Live Parameter Tuning Laboratory</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='sub-title'>Interactive Exploration of Spectral Burn Severity (dNBR), NASA FIRMS T21 Thermal Filtering, and OpenCV Mathematical Morphology | 10m Master Grid</div>",
        unsafe_allow_html=True,
    )

    # KPI Metrics
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    with col_k1:
        st.markdown(
            f"<div class='kpi-card'><div class='kpi-title'>Raw Burn Candidate Mask</div><div class='kpi-number'>{live_res['raw_ha']:,.1f} Ha</div></div>",
            unsafe_allow_html=True,
        )
    with col_k2:
        st.markdown(
            f"<div class='kpi-card'><div class='kpi-title'>Clean Burn Scar Polygon</div><div class='kpi-number' style='color:#0284c7;'>{live_res['clean_ha']:,.1f} Ha</div></div>",
            unsafe_allow_html=True,
        )
    with col_k3:
        st.markdown(
            f"<div class='kpi-card'><div class='kpi-title'>Eliminated Salt-and-Pepper Noise</div><div class='kpi-number' style='color:#e11d48;'>{live_res['noise_ha']:,.1f} Ha ({live_res['noise_pct']:.1f}%)</div></div>",
            unsafe_allow_html=True,
        )
    with col_k4:
        st.markdown(
            f"<div class='kpi-card'><div class='kpi-title'>Active Configuration</div><div class='kpi-number' style='font-size:14px; color:#16a34a;'>dNBR > {dnbr_th:.2f} | Op:{open_size} | Cl:{close_size}</div></div>",
            unsafe_allow_html=True,
        )

    tab_live1, tab_live2, tab_live3 = st.tabs(
        [
            "Tab 1: Multi-Temporal RGB Comparison & Contour Overlay",
            "Tab 2: Step-by-Step Mathematical Morphology Inspector",
            "Tab 3: Burn Severity (dNBR) Parameter Sensitivity Curve",
        ]
    )

    with tab_live1:
        st.subheader("Side-by-Side Multi-Temporal Sentinel-2 Imagery with Dynamic Burn Scar Contour")
        st.markdown(
            "The burn scar boundary contour below **recomputes in real time** whenever the `dNBR Threshold`, `Morphological Opening/Closing Kernel`, or `Connected Component Filter` is adjusted."
        )

        img_pre_draw = data["previews"]["rgb_pre"]
        img_fire_draw = data["previews"]["rgb_fire"]
        img_now_draw = data["previews"]["rgb_now"]

        if show_contour:
            img_pre_draw = overlay_mask_contour(img_pre_draw, live_res["clean"], color_bgr=contour_color, thickness=2)
            img_fire_draw = overlay_mask_contour(img_fire_draw, live_res["clean"], color_bgr=contour_color, thickness=2)
            img_now_draw = overlay_mask_contour(img_now_draw, live_res["clean"], color_bgr=contour_color, thickness=2)
            tag = f" (Active Contour: dNBR > {dnbr_th:.2f})"
        else:
            tag = ""

        col_v1, col_v2, col_v3 = st.columns(3)
        with col_v1:
            st.image(
                img_pre_draw,
                caption=f"Pre-Fire Baseline (May - Jul 2023)\nTrue Color RGB (Intact Peat Swamp Forest){tag}",
                use_container_width=True,
            )
        with col_v2:
            st.image(
                img_fire_draw,
                caption=f"Active Fire Peak (Sep - Nov 2023)\nTrue Color RGB (Charcoal Burn Scar){tag}",
                use_container_width=True,
            )
        with col_v3:
            st.image(
                img_now_draw,
                caption=f"Post-Fire Recovery State (Jun - Sep 2026)\nTrue Color RGB (3 Years Post-Fire){tag}",
                use_container_width=True,
            )

        st.markdown(
            """
            <div class='academic-box'>
            <b>Interactive Demonstration Tip:</b> Set <i>Morphological Opening Kernel Size</i> to <b>0</b>. Notice how isolated salt-and-pepper commission errors appear across unburned forest due to cloud-shadow spectral noise (total area > 7,900 Ha). Setting Opening back to <b>5</b> cleanly erodes the noise while preserving the core burn scar polygon (~ 5,976 Ha).
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab_live2:
        st.subheader("Step-by-Step Binary Mathematical Morphology Inspector")
        st.markdown(
            r"""
            Sequential decomposition of Method 1 binary image processing:
            1. **Raw Burn Candidate Mask:** Thresholding $\Delta\text{NBR}$ and NASA FIRMS T21 thermal filtering.
            2. **Morphological Opening ($A \circ B$):** Erosion followed by dilation removes isolated salt-and-pepper noise.
            3. **Morphological Closing ($A \bullet B$):** Dilation followed by erosion bridges internal canopy gaps.
            4. **Eliminated Noise Map:** Highlights commission noise pixels removed by morphology and connected component filtering (Red).
            """
        )

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)

        preview_dim = (800, 800)
        cand_sm = cv2.resize(live_res["cand"], preview_dim, interpolation=cv2.INTER_NEAREST)
        opened_sm = cv2.resize(live_res["opened"], preview_dim, interpolation=cv2.INTER_NEAREST)
        closed_sm = cv2.resize(live_res["closed"], preview_dim, interpolation=cv2.INTER_NEAREST)
        clean_sm = cv2.resize(live_res["clean"].astype(np.uint8), preview_dim, interpolation=cv2.INTER_NEAREST)

        noise_sm = (cand_sm > 0) & (clean_sm == 0)

        with col_m1:
            st.markdown(f"**1. Raw Candidate Mask ({live_res['raw_ha']:,.1f} Ha)**")
            fig1, ax1 = plt.subplots(figsize=(5, 5), dpi=110)
            ax1.imshow(data["previews"]["rgb_fire"] * 0.45)
            ax1.imshow(np.ma.masked_equal(cand_sm, 0), cmap="autumn", alpha=0.9)
            ax1.axis("off")
            ax1.set_title("Pre-Morphology (Salt-and-Pepper Noise)", fontsize=8)
            st.pyplot(fig1)
            plt.close(fig1)

        with col_m2:
            st.markdown(f"**2. Morphological Opening ({live_res['opened_ha']:,.1f} Ha)**")
            fig2, ax2 = plt.subplots(figsize=(5, 5), dpi=110)
            ax2.imshow(data["previews"]["rgb_fire"] * 0.45)
            ax2.imshow(np.ma.masked_equal(opened_sm, 0), cmap="Wistia", alpha=0.9)
            ax2.axis("off")
            ax2.set_title(f"Opening Kernel: {open_size}x{open_size}", fontsize=8)
            st.pyplot(fig2)
            plt.close(fig2)

        with col_m3:
            st.markdown(f"**3. Morphological Closing ({live_res['closed_ha']:,.1f} Ha)**")
            fig3, ax3 = plt.subplots(figsize=(5, 5), dpi=110)
            ax3.imshow(data["previews"]["rgb_fire"] * 0.45)
            ax3.imshow(np.ma.masked_equal(closed_sm, 0), cmap="spring", alpha=0.9)
            ax3.axis("off")
            ax3.set_title(f"Closing Kernel: {close_size}x{close_size}", fontsize=8)
            st.pyplot(fig3)
            plt.close(fig3)

        with col_m4:
            st.markdown(f"**4. Eliminated Noise ({live_res['noise_ha']:,.1f} Ha)**")
            fig4, ax4 = plt.subplots(figsize=(5, 5), dpi=110)
            ax4.imshow(data["previews"]["rgb_fire"] * 0.45)
            ax4.imshow(np.ma.masked_equal(clean_sm, 0), cmap="Greens", alpha=0.8)
            ax4.imshow(np.ma.masked_equal(noise_sm.astype(np.uint8), 0), cmap="Reds", alpha=0.9)
            ax4.axis("off")
            ax4.set_title(f"Red = Eliminated Noise ({live_res['noise_pct']:.1f}%)", fontsize=8)
            st.pyplot(fig4)
            plt.close(fig4)

    with tab_live3:
        st.subheader("Burn Scar Area Sensitivity to Burn Severity Threshold (dNBR Sweep)")
        st.markdown(
            r"Parameter sweep evaluating how delineated burn scar area responds to variations in the $\Delta\text{NBR}$ threshold."
        )

        col_s1, col_s2 = st.columns([2, 1])

        ths_sweep = np.arange(0.10, 0.36, 0.02)
        areas_sweep = []
        for t_val in ths_sweep:
            r_b = data["dnbr"] > t_val
            c_b = r_b & data["land_mask"] & data["both_valid"]
            if use_firms:
                c_b = c_b & ((data["firms_t21"] > firms_th) | (data["dnbr"] > (t_val + 0.08)))
            areas_sweep.append(float(np.sum(c_b) * data["pixel_area_ha"]))

        with col_s1:
            fig_sw, ax_sw = plt.subplots(figsize=(8, 4.5), dpi=120)
            ax_sw.plot(ths_sweep, areas_sweep, marker="o", color="#0284c7", linewidth=2.2, label="Candidate Burn Area (Ha)")
            ax_sw.axvline(dnbr_th, color="#e11d48", linestyle="--", linewidth=1.5, label=f"Active Threshold: {dnbr_th:.2f}")
            ax_sw.axhline(live_res["raw_ha"], color="#ea580c", linestyle=":", linewidth=1.2, label=f"Raw Candidate: {live_res['raw_ha']:,.0f} Ha")
            ax_sw.set_xlabel("Burn Severity Threshold (dNBR)", fontweight="bold")
            ax_sw.set_ylabel("Delineated Area (Hectares)", fontweight="bold")
            ax_sw.set_title("dNBR Parameter Sensitivity Response Curve", fontweight="bold")
            ax_sw.grid(True, alpha=0.3)
            ax_sw.legend()
            st.pyplot(fig_sw)
            plt.close(fig_sw)

        with col_s2:
            st.markdown("**dNBR Sensitivity Lookup Table:**")
            df_sweep = pd.DataFrame(
                {"dNBR Threshold": [round(t, 2) for t in ths_sweep], "Estimated Area (Ha)": [round(a, 1) for a in areas_sweep]}
            )
            st.dataframe(df_sweep, height=300, use_container_width=True)

# =============================================================================
# MENU 2: FULL REPORT & PUBLICATION GALLERY (7 FIGURES)
# =============================================================================
elif app_mode.startswith("2."):
    st.markdown(
        "<div class='main-title'>Full Report & Publication Figure Gallery (7 Figures)</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='sub-title'>10-Meter Master Grid Scientific Output: Sebangau - Kahayan Landscape (2,990 x 3,006 Pixels)</div>",
        unsafe_allow_html=True,
    )

    tab_pub1, tab_pub2, tab_pub3, tab_pub4, tab_pub5, tab_pub6 = st.tabs(
        [
            "Executive Summary Map (Fig 5)",
            "Composites & 6 Features (Fig 1 & 3)",
            "Method 1 Delineation Pipeline (Fig 2)",
            "Pre-GLCM vs 2-Stage GLCM (Fig 4)",
            "Multi-Temporal Trajectory (Fig 6)",
            "Confusion Matrix & GEDI LiDAR (Fig 7)",
        ]
    )

    with tab_pub1:
        st.subheader("6-Panel Chronological Spatial & 2-Stage Hierarchical Classification Summary")
        st.image(
            os.path.join(RESULTS_DIR, "hasil_analisis_pcd_karhutla.png"),
            caption="Figure 5: 6-Panel Executive Summary (2023 Pre-Fire, 2023 Active Fire, dNBR & Morphology, GLCM Homogeneity, 2026 Recovery RGB, and 4-Class Hierarchical Map)",
            use_container_width=True,
        )

        if data["df_stats"] is not None:
            st.subheader("Quantitative Post-Fire Land Cover Statistics (2026 Y3 - 4 Classes)")
            st.dataframe(data["df_stats"], use_container_width=True)
            st.download_button(
                label="Download Cluster Statistics Table (CSV)",
                data=data["df_stats"].to_csv(index=False),
                file_name="statistik_klaster_2023_2026.csv",
                mime="text/csv",
            )

    with tab_pub2:
        st.subheader("Sentinel-2 Multi-Spectral Composites & 6 Extracted Input Features")
        st.image(
            os.path.join(RESULTS_DIR, "fig1_komposit_multispektral.png"),
            caption="Figure 1: Sentinel-2 Multi-Spectral Composites (True Color RGB, False Color CIR, False Color SWIR) and Biophysical Indices (NDVI, NDMI, BSI)",
            use_container_width=True,
        )
        st.image(
            os.path.join(RESULTS_DIR, "fig3_ekstraksi_fitur_spektral_glcm.png"),
            caption="Figure 3: 6 Extracted Feature Maps (NDVI, NDMI, BSI, GLCM Homogeneity, GLCM Contrast, and GLCM Shannon Entropy)",
            use_container_width=True,
        )

    with tab_pub3:
        st.subheader("Method 1 Burn Scar Delineation & Mathematical Morphology Pipeline (8 Panels)")
        st.image(
            os.path.join(RESULTS_DIR, "fig2_progres_workflow_morfologi.png"),
            caption="Figure 2: Step-by-Step Method 1 Pipeline (Pre-Fire RGB, Active Fire RGB, False Color SWIR, FIRMS T21, Burn Severity dNBR, Raw Candidate Mask, Morphological Opening & Closing, and 2026 Boundary Overlay)",
            use_container_width=True,
        )

    with tab_pub4:
        st.subheader("Pre-GLCM Macro Spectral Clustering vs 2-Stage Hierarchical Classification (Spectral + GLCM)")
        st.markdown(
            """
            Panel (c) demonstrates that **Exposed Bare Peat / Unrecovered Land (Red)** is preserved directly from Stage 1 spectral isolation without being forced through canopy GLCM texture, while vegetated pixels are separated in Stage 2 into **Structured Monoculture Vegetation (Yellow)**, **Degraded Shrubland (Orange)**, and **Natural Forest Succession (Green)**.
            """
        )
        st.image(
            os.path.join(RESULTS_DIR, "fig4_komparasi_sebelum_sesudah_glcm.png"),
            caption="Figure 4: Comparison of Pre-GLCM Macro Spectral Clustering and 2-Stage Hierarchical Classification (Spectral + Haralick GLCM)",
            use_container_width=True,
        )

    with tab_pub5:
        st.subheader("Multi-Temporal Post-Fire Recovery Trajectory Curves (2023 Pre - 2026 Y3)")
        st.image(
            os.path.join(RESULTS_DIR, "trajektori_tahunan_2023_2026.png"),
            caption="Figure 6: Annual Multi-Temporal Trajectory across 5 Epochs for NDVI, NDMI, BSI, GLCM Homogeneity, Contrast, and Entropy",
            use_container_width=True,
        )
        if data["df_traj"] is not None:
            st.download_button(
                label="Download Multi-Temporal Trajectory Data (CSV)",
                data=data["df_traj"].to_csv(index=False),
                file_name="trajektori_tahunan_2023_2026.csv",
                mime="text/csv",
            )

    with tab_pub6:
        st.subheader("Independent Validation: Dynamic World V1 Confusion Matrix & NASA GEDI L2A RH98")
        st.image(
            os.path.join(RESULTS_DIR, "evaluasi_confusion_matrix_gedi.png"),
            caption="Figure 7: 4-Class Confusion Matrix (Overall Accuracy: 58.37%, Cohen's Kappa: 0.4448) and NASA GEDI L2A RH98 Canopy Height Boxplot",
            use_container_width=True,
        )

# =============================================================================
# MENU 3: ARCHIVE BASELINE CASE STUDY (2019 - 2025)
# =============================================================================
elif app_mode.startswith("3."):
    st.markdown(
        "<div class='main-title'>Archive Baseline Case Study: 2019 - 2025 Post-Fire Recovery (>5 Years)</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='sub-title'>Sebangau - Pulang Pisau Peatland Chronological Analysis via Sentinel-2 Spectral K-Means (3 Classes)</div>",
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            "<div class='kpi-card'><div class='kpi-title'>Total Burn Scar (2019)</div><div class='kpi-number'>20,188.42 Ha</div></div>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            "<div class='kpi-card'><div class='kpi-title'>Class 1: Dense Vegetation</div><div class='kpi-number' style='color:#16a34a;'>3,520.17 Ha (17.4%)</div></div>",
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            "<div class='kpi-card'><div class='kpi-title'>Class 2: Degraded Shrubland</div><div class='kpi-number' style='color:#ea580c;'>9,268.21 Ha (45.9%)</div></div>",
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            "<div class='kpi-card'><div class='kpi-title'>Class 3: Bare Soil / Built-Up</div><div class='kpi-number' style='color:#e11d48;'>7,400.04 Ha (36.7%)</div></div>",
            unsafe_allow_html=True,
        )

    st.image(
        os.path.join(ARCHIVE_RESULTS_DIR, "komparasi_kronologis_dan_proporsi.png"),
        caption="Archive Baseline (2019-2025): Chronological Comparison (Pre-Fire 2019, Active Fire 2019, Post-Fire 2025, and Class Proportion)",
        use_container_width=True,
    )

    st.image(
        os.path.join(ARCHIVE_RESULTS_DIR, "hasil_analisis_pcd_karhutla.png"),
        caption="Archive Baseline (2019-2025): Multi-Panel Spatial Output",
        use_container_width=True,
    )

# =============================================================================
# MENU 4: CROSS-PERIOD COMPARISON (2019 vs 2023)
# =============================================================================
elif app_mode.startswith("4."):
    st.markdown(
        "<div class='main-title'>Cross-Period Comparison: 2019 Baseline vs 2023-2026 Hierarchical Pipeline</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='sub-title'>Methodological, Spatial, and Ecological Comparison Between the 2019 and 2023 El Nino Fire Events</div>",
        unsafe_allow_html=True,
    )

    comp_df = pd.DataFrame(
        [
            {
                "Evaluation Parameter": "Fire Event Period",
                "Archive Baseline (2019-2025)": "2019 (Moderate El Nino)",
                "Current Pipeline (2023-2026)": "2023 (Strong El Nino & Positive IOD)",
            },
            {
                "Evaluation Parameter": "Monitoring Horizon",
                "Archive Baseline (2019-2025)": "> 5 Years (2019 to 2025)",
                "Current Pipeline (2023-2026)": "3 Years (2023 to 2026, 5 Annual Epochs)",
            },
            {
                "Evaluation Parameter": "Clean Burn Scar Area",
                "Archive Baseline (2019-2025)": "20,188.42 Ha",
                "Current Pipeline (2023-2026)": "5,888.20 Ha (Fully Tracked Burn Scar Polygon)",
            },
            {
                "Evaluation Parameter": "Method 1: Burn Scar Delineation",
                "Archive Baseline (2019-2025)": "dNBR > 0.25 + Cloud Masking",
                "Current Pipeline (2023-2026)": "dNBR > 0.20 + FIRMS T21 + JRC Water + Opening 5x5 + Closing 7x7 + CC Filter",
            },
            {
                "Evaluation Parameter": "Method 2: Feature Extraction",
                "Archive Baseline (2019-2025)": "Spectral Indices Only (NDVI, NDMI, BSI)",
                "Current Pipeline (2023-2026)": "Spectral Indices + 4-Directional Haralick GLCM Texture (Homogeneity, Contrast, Entropy)",
            },
            {
                "Evaluation Parameter": "Method 3: Classification Scheme",
                "Archive Baseline (2019-2025)": "Single-Stage Spectral K-Means (3 Classes)",
                "Current Pipeline (2023-2026)": "2-Stage Hierarchical Classification (4 Classes: Bare Peat + 3 GLCM Vegetation Classes)",
            },
            {
                "Evaluation Parameter": "Structured Monoculture Separation",
                "Archive Baseline (2019-2025)": "Merged inside general green vegetation class",
                "Current Pipeline (2023-2026)": "Separated as Class 1: 1,344.57 Ha (22.83%) via GLCM Homogeneity = 0.7971",
            },
            {
                "Evaluation Parameter": "Independent Reference Validation",
                "Archive Baseline (2019-2025)": "Visual Sentinel-2 Inspection",
                "Current Pipeline (2023-2026)": "Dynamic World V1 Confusion Matrix (OA: 58.37%, Kappa: 0.4448) + NASA GEDI L2A RH98",
            },
        ]
    )

    st.table(comp_df)

    col_cp1, col_cp2 = st.columns(2)
    with col_cp1:
        st.markdown("**Archive Baseline (2019 - 2025):**")
        arch_img = os.path.join(ARCHIVE_RESULTS_DIR, "komparasi_kronologis_dan_proporsi.png")
        if os.path.exists(arch_img):
            st.image(arch_img, use_container_width=True)
    with col_cp2:
        st.markdown("**Current 2-Stage Hierarchical Pipeline (2023 - 2026):**")
        now_img = os.path.join(RESULTS_DIR, "hasil_analisis_pcd_karhutla.png")
        if os.path.exists(now_img):
            st.image(now_img, use_container_width=True)

st.markdown("---")
st.caption(
    "Digital Image Processing (PCD) Group 3B | D4 Informatics Engineering, Politeknik Negeri Bandung (POLBAN)"
)
