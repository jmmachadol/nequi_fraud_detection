# src/features.py

import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype

WINDOWS_H = {
    "1h": "1h",
    "6h": "6h",
    "24h": "24h",
    "7d": "7d",
}

def _rolling_features(df, amount_col="transaction_amount"):
    df = df.sort_values(["user_id", "transaction_date"]).copy()
    grp = df.set_index("transaction_date").groupby("user_id", sort=False)

    for win_name, win_len in WINDOWS_H.items():
        # Suma rolling
        df[f"tx_sum_{win_name}"] = (
            grp[amount_col]
            .rolling(window=win_len, closed="left")
            .sum()
            .reset_index(level=0, drop=True)
            .astype("float32")
            .values
        )
        # Conteo rolling  
        df[f"tx_cnt_{win_name}"] = (
            grp[amount_col]
            .rolling(window=win_len, closed="left")
            .count()
            .reset_index(level=0, drop=True)
            .astype("Int32")     
            .values
        )
    return df


def _ratios(df):
    """Ratios entre ventanas recientes y referencia."""
    df["ratio_sum_1h_24h"] = (df["tx_sum_1h"] /
                              df["tx_sum_24h"].replace(0, np.nan)).astype("float32")
    df["ratio_cnt_1h_24h"] = (df["tx_cnt_1h"] /
                              df["tx_cnt_24h"].replace(0, np.nan)).astype("float32")

    df["ratio_sum_24h_7d"] = (df["tx_sum_24h"] /
                              df["tx_sum_7d"].replace(0, np.nan)).astype("float32")
    df["ratio_cnt_24h_7d"] = (df["tx_cnt_24h"] /
                              df["tx_cnt_7d"].replace(0, np.nan)).astype("float32")
    return df

def _z_score_7d(df, amount_col="transaction_amount"):
    grp = (
        df.sort_values(["user_id", "transaction_date"])
          .set_index("transaction_date")
          .groupby("user_id", sort=False)[amount_col]
    )
    mean7 = (
        grp.rolling("7d", closed="left").mean().reset_index(level=0, drop=True).values
    )
    std7  = (
        grp.rolling("7d", closed="left").std(ddof=0).reset_index(level=0, drop=True).values
    )
    df["z_amt_7d"] = ((df[amount_col] - mean7) / np.where(std7==0, np.nan, std7)).astype("float32")
    return df

def _time_encodings(df, date_col="transaction_date"):
    """Añade codificación cíclica + enteros de hora y día-semana."""
    dt = df[date_col]
    df["hour_int"] = dt.dt.hour.astype("int8")
    df["dow_int"]  = dt.dt.dayofweek.astype("int8")

    df["hour_sin"] = np.sin(2 * np.pi * df["hour_int"] / 24).astype("float32")
    df["hour_cos"] = np.cos(2 * np.pi * df["hour_int"] / 24).astype("float32")
    df["dow_sin"]  = np.sin(2 * np.pi * df["dow_int"]  / 7).astype("float32")
    df["dow_cos"]  = np.cos(2 * np.pi * df["dow_int"]  / 7).astype("float32")
    return df

def _amount_flags(df, amount_col="transaction_amount", type_col="transaction_type"):
    """Crea flags p95 / p99 por tipo de transacción."""
    pct = df.groupby(type_col)[amount_col].quantile([0.95, 0.99]).unstack(level=1)
    pct.columns = ["p95", "p99"]

    df = df.join(pct, on=type_col)
    df["flag_amt_p95"] = (df[amount_col] > df["p95"]).astype("int8")
    df["flag_amt_p99"] = (df[amount_col] > df["p99"]).astype("int8")
    df.drop(columns=["p95", "p99"], inplace=True)
    return df

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera todas las variables de ingeniería definidas en la prueba.
    El DataFrame de entrada **no** se modifica in-place; se devuelve
    una copia con columnas añadidas.
    """
    df = df.copy()

    # Validaciones mínimas
    req_cols = {"user_id", "transaction_date", "transaction_amount", "transaction_type"}
    missing = req_cols - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas requeridas: {missing}")

    if not is_numeric_dtype(df["transaction_amount"]):
        df["transaction_amount"] = pd.to_numeric(df["transaction_amount"], errors="coerce")

    # Paso 1: ventanas rolling
    df = _rolling_features(df)

    # Paso 2: ratios
    df = _ratios(df)

    # Paso 3: z-score 7 d
    df = _z_score_7d(df)

    # Paso 4: codificación temporal
    df = _time_encodings(df)

    # Paso 5: flags monto alto
    df = _amount_flags(df)

    return df