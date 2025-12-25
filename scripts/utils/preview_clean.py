# scripts/preview_clean.py
from pathlib import Path
from acuario.config import PROCESSED
import pandas as pd

def main():
    archivos = list(PROCESSED.glob("*.parquet"))
    if not archivos:
        print(f"No hay .parquet en {PROCESSED}. ¿Corriste run_pipeline.py?")
        return

    for p in archivos:
        print(f"\n=== {p.name} ===")
        df = pd.read_parquet(p)
        print("Dtypes:")
        print(df.dtypes)
        print("\nHead():")
        print(df.head())

if __name__ == "__main__":
    main()
