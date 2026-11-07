# Evaluasi mask bangunan

Jalankan evaluator dari root project:

```powershell
python scripts\metric_eval\evaluate_masks.py --predictions output_results\paper_lab_kmeans
```

Evaluator mencocokkan `location_XX_detection_mask.png` dengan nama file sama di
`dataset\eval`. Hasil tersimpan di `scripts\metric_eval\metrics.csv` atau path
yang diberikan lewat `--output`.

Metric utama adalah macro mean IoU. Dice, precision, recall, pixel accuracy,
balanced accuracy, dan object-F1 (matching IoU 0.5) ikut disimpan.
