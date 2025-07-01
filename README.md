# Detección de Fraccionamiento Transaccional  
**Prueba Técnica – Nequi**

Autor: **José Manuel Machado Loaiza**  
Fecha: junio 2025

---

## 1. Propósito

Construir un flujo reproducible que:

1. **Depure** el histórico de transacciones (1,29 GB Parquet).  
2. **Genere** variables de comportamiento en ventanas 1 h / 6 h / 24 h / 7 d.  
3. **Modele** anomalías para priorizar alertas de posible fraccionamiento.  
4. **Explique** cada alerta mediante valores SHAP.

---

## 2. Competencias demostradas

| Dimensión | Evidencia |
|-----------|-----------|
| **Comprensión de negocio** | definición de fraccionamiento y métrica *recall@k* (notebook 03). |
| **Ingeniería de datos** | ingesta Parquet, validación de esquema, casting óptimo, deduplicación. |
| **EDA** | estadísticos robustos, histogramas de monto, curvas hora-día (01_eda). |
| **Feature engineering** | rolling sums/counts, z-score 7 d, flags p95/p99, codificación seno/coseno (02_features). |
| **Modelado** | Isolation Forest (100 árboles) + PCA-error (10 comp.). |
| **Buenas prácticas** | código modular en `src/`, tipado estricto, logging estandarizado. |
| **Comunicación** | Markdown técnico, tablas de umbrales, diagrama de arquitectura. |

---

## 3. Requisitos rápidos

```bash
python -m venv .venv
source .venv/bin/activate                  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
````

---

## 4. Estructura del repositorio

```
artifacts/    ← modelos .joblib, ranking Top-N, architecture.png
cache/        ← parquets intermedios (clean, features)
notebooks/    ← 01_eda · 02_features · 03_modeling · 04_report
src/          ← data.py · features.py · utils.py
data/         ← sample_data_0006_part_00.parquet
requirements.txt
README.md
```

---

## 5. Resultados principales

| Modelo                     | Threshold Top 0.1 % | Tiempo de entrenamiento | Interpretabilidad     |
| -------------------------- | ------------------- | ----------------------- | --------------------- |
| **Isolation Forest (100)** | 0.59                | 14 min                  | SHAP Tree (500 casos) |
| PCA-10 (error reconstr.)   | 4.96                | 25 s                    | —                     |

*Las 15 variables con mayor impacto se concentran en sumas de monto y conteos
en 24 h/1 h, validando la hipótesis de fraccionamiento.*

© 2025 – MIT License
