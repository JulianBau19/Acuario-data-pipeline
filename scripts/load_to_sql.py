from pathlib import Path
import pandas as pd
from acuario.db import get_engine


def get_processed_folder() -> Path:
    """
    Devuelve la ruta a la carpeta data/processed
    tomando como base la raíz del proyecto.
    """
    project_root = Path(__file__).resolve().parents[1]
    return project_root / "data" / "processed"


def load_parquet_files(folder: Path) -> dict:
    """
    Lee todos los .parquet de la carpeta indicada y
    devuelve un diccionario {nombre_tabla: dataframe}.
    """
    dataframes = {}

    for file in folder.glob("*.parquet"):
        table_name = file.stem.lower()   # ventas.parquet -> 'ventas'
        df = pd.read_parquet(file)
        dataframes[table_name] = df

    return dataframes


def upload_to_sql(if_exists: str = "replace") -> None:
    """
    Carga cada dataframe a SQL Server usando el nombre del archivo
    como nombre de tabla.

    if_exists:
        - 'replace' -> borra y crea la tabla de cero
        - 'append'  -> agrega filas a la tabla existente
    """
    engine = get_engine()
    folder = get_processed_folder()
    tables = load_parquet_files(folder)

    print(f"Encontrados {len(tables)} archivos .parquet en {folder}")

    for table_name, df in tables.items():
        print(f"Cargando tabla '{table_name}' ({len(df)} filas)...")

        df.to_sql(
            name=table_name,
            con=engine,
            if_exists=if_exists,
            index=False
        )

    print("Carga a SQL completada.")


if __name__ == "__main__":
    upload_to_sql(if_exists="replace")
