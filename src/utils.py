# src/utils.py
import logging, numpy as np

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def log_step(msg: str):
    logging.info(msg)

SEED = 42
np.random.seed(SEED)