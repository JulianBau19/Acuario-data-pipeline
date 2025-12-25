from pathlib import Path

# export.py
def guardar_parquet(dfs: dict, dir_destino):
    for nombre, df in dfs.items():
        # Hacemos una copia para no tocar el original
        df = df.copy()

        # Convertir todas las columnas object a string legible
        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].astype("string")

        destino = dir_destino / f"{nombre}.parquet"
        print(f"Guardando: {nombre}.parquet")
        df.to_parquet(destino, index=False)

## usamos .parquet porque ocupa menos espacio que CVS