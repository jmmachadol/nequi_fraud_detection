# Detención de Fraccionamiento Transaccional • Prueba Técnica NEQUI

A cargo de: José Manuel Machado Loaiza

> Proyecto de analítica avanzada para identificar patrones de fraccionamiento
> (split payments) en transacciones financieras.

## 1. Propósito
Diseñar un *pipeline* reproducible que:
1. Limpie y valide datos transaccionales.
2. Genere atributos temporales y de comportamiento.
3. Modele anomalías para priorizar alertas de posible fraccionamiento.

## 2. Competencias evaluadas

| Dimensión | Evidencia en este repositorio |
|-----------|------------------------------|
| **Entendimiento del negocio** | Definición operativa de fraccionamiento y métricas. |
| **Ingeniería de datos** | Ingesta Parquet, validación de esquema, manejo de duplicados y tipos. |
| **Análisis exploratorio** | Estadísticos robustos, segmentaciones y visualizaciones en `01_eda.ipynb`. |
| **Feature Engineering** | Ventanas móviles 1 h / 6 h / 24 h, banderas de duplicado semántico. |
| **Modelado analítico** | *(Próximo notebook 03)* Isolation Forest y LOF con validación temporal. |
| **Buenas prácticas** | Código modular, tipado de datos, `.gitignore`, requisitos explícitos. |
| **Comunicación** | Markdown técnico y conclusiones cuantitativas. |

## 3. Requisitos

```bash
conda create -n nequi-fraud python=3.10
conda activate nequi-fraud
pip install -r requirements.txt
```

## 4. Ejecución

1. Colocar los Parquet originales en `data/`
2. Ejecutar `notebooks/01_eda.ipynb`.
3. Ejecutar `notebooks/02_feature_eng.ipynb`; se generarán artefactos en `artifacts/`.
4. (Próximo) Ejecutar `03_modelado.ipynb` para obtener el ranking de riesgo.

## 5. Estructura

```
notebooks/      análisis exploratorio y generación de features
artifacts/      datasets intermedios y matrices de features
src/            helpers reutilizables (carga, limpieza, ventanas)
data/           datasets originales
```

## 6. Roadmap

- Detección de drift semanal y ajuste dinámico de umbrales.
- Integrar CI con pre-commit y pruebas unitarias.

---

© 2025 — MIT License
