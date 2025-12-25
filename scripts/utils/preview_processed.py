from pathlib import Path
import pandas as pd

PROCESSED = Path("data/processed")   # ajusta si usas otra ruta

def main():
    for fichero in PROCESSED.glob("*.parquet"):
        print(f"\n=== {fichero.name} ===")
        df = pd.read_parquet(fichero)
        print("Filas:", len(df))
        print("Columnas:", len(df.columns))
        print("Tipos:")
        print(df.dtypes)
        print("\nMuestra:")
        print(df.head(20))

if __name__ == "__main__":
    main()
