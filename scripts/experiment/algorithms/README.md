# Kandidat algoritma deteksi

Semua script membaca `dataset\raw\location_XX_image.png` dan menulis mask
seragam ke folder output. Dataset evaluasi tidak dibaca algoritma.

```powershell
python scripts\experiment\algorithms\paper_lab_kmeans.py --output output_results\paper_lab_kmeans
python scripts\experiment\algorithms\hsv_vegetation_otsu.py --output output_results\hsv_vegetation_otsu
python scripts\experiment\algorithms\watershed_edges.py --output output_results\watershed_edges
python scripts\metric_eval\evaluate_masks.py --predictions output_results\paper_lab_kmeans
```

`paper_lab_kmeans.py` mereplikasi inti segmentasi paper utama:
CIELab, K-Means pada kanal kromatik, hole filling, dan filter luas.
Script lain menjadi kandidat pembanding berbasis segmentasi warna dan
marker-controlled watershed dari paper pendukung.
