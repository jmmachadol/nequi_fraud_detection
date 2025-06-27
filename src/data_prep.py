"""Funciones utilitarias para carga y limpieza de datos NEQUI."""

import pandas as pd
from pathlib import Path
from typing import Dict, List

def load_parquet(path: Path, columns: List[str] | None = None) -> pd.DataFrame:
    """Carga un archivo Parquet con columnas opcionales."""
    return pd.read_parquet(path, columns=columns)