from pathlib import Path
import pandas as pd

def leer_excels(carpeta: Path) -> dict:
    """
    Lee TODOS los Excel dentro de 'carpeta' y sus subcarpetas.
    Acepta .xlsx y .xls. Devuelve {nombre_archivo: DataFrame}.
    """
    salida = {}
    # rglob busca recursivamente
    patrones = ("*.xlsx", "*.xls")
    files = []
    for pat in patrones:
        files.extend(list(carpeta.rglob(pat)))

    if not files:
        print(f"[INFO] No se encontraron Excel en: {carpeta.resolve()}")
        return salida

    for archivo in files:
        # clave: nombre base sin extensión (en minúsculas)
        nombre = archivo.stem.lower()
        print(f"Leyendo: {archivo.relative_to(carpeta)}")
        df = pd.read_excel(archivo)
        salida[nombre] = df
    return salida

