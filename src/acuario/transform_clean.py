# src/acuario/transform_clean.py
from pathlib import Path
import pandas as pd
import yaml
import re

# ===============================
# Funcion para cargar el YAML 
# ===============================


def _cargar_yaml(ruta: Path) -> dict:
    """
    Abre un YAML y devuelve un dict. Si no existe, devuelve {}.
    """
    if not ruta or not ruta.exists():
        return {}
    with ruta.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


# ===============================
# ESTANDARIZACIÓN INICIAL
# ===============================
def estandarizar_headers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza los nombres de columnas para compararlos sin errores:
    - Quita espacios al inicio/fin
    - Convierte a UPPERCASE (porque Factusol suele venir en mayúsculas)
    """
    df = df.copy()
    df.columns = [c.strip().upper() for c in df.columns]
    return df

def aplicar_mapping(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    if not mapping:
        return df

    # 1. Separar renombres de 'keep'
    renombres = {k: v for k, v in mapping.items() if k != "keep"}

    # 2. Renombrar columnas originales
    df_clean = df.rename(columns=renombres)

    # 3. Eliminación automática de columnas NO mapeadas
    df_clean = df_clean[list(renombres.values())]

    # 4. Si keep está definido, filtrar aún más
    if "keep" in mapping:
        df_clean = df_clean[mapping["keep"]]

    return df_clean

 ##Renombra columnas usando el mapping {ORIGINAL -> limpio}.
    ##Si alguna columna no está en el mapping, la deja tal cual.


# ===============================
# LIMPIEZAS DE TEXTO / ESPACIOS
# ===============================
def trim_strings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica strip() a todas las columnas de texto para eliminar espacios
    al inicio y al final. No toca columnas numéricas.
    """
    df = df.copy()
    for col in df.columns:
        if pd.api.types.is_string_dtype(df[col]):
            df[col] = df[col].astype(str).str.strip()
    return df


def normalizar_codigos(df: pd.DataFrame, columnas: list[str]) -> pd.DataFrame:
    """
    Convierte a mayúsculas y sin espacios dobles ciertos campos 'código'.
    Útil para códigos de artículo, cliente, etc.
    """
    df = df.copy()
    for col in columnas:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.upper()
                .str.replace(r"\s+", " ", regex=True)
            )
    return df


# ===============================
# CONVERSIÓN DE TIPOS
# ===============================
def _to_number_robusto(serie: pd.Series) -> pd.Series:
    """
    Convierte una serie a número de forma 'robusta':
    - Quita separadores de miles . o espacio
    - Cambia coma decimal por punto
    - Si no puede convertir, deja NaN
    """
    return (
        serie.astype(str)
        .str.replace(r"[.\s]", "", regex=True)
        .str.replace(",", ".", regex=False)
        .replace({"": None, "None": None})
        .astype(float)
    )


def aplicar_dtypes(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    """
    Aplica los dtypes definidos en el schema YAML.
    Soporta: string, int, float, date (y formateo de fecha).
    """
    df = df.copy()
    dtypes = (schema.get("dtypes") or {}) if schema else {}
    date_formats = (schema.get("date_formats") or {}) if schema else {}

    for col, tipo in dtypes.items():
        if col not in df.columns:
            continue

        if tipo == "string":
            df[col] = df[col].astype("string")

        elif tipo == "int":
            # Pasamos por float robusto primero (por si viene con comas)
            df[col] = _to_number_robusto(df[col]).round().astype("Int64")

        elif tipo == "float":
    # Usamos el normalizador de precios (soporta formato europeo con coma)
            df[col] = normalizar_precio(df[col])
 
        elif tipo == "date":
            # Intentamos parsear con los formatos definidos; si no hay, probamos automático
            formatos = date_formats.get(col, [])
            if formatos:
                ok = pd.NaT
                for fmt in formatos:
                    try:
                        ok = pd.to_datetime(df[col], format=fmt, errors="coerce")
                        # Si al menos hay algún valor no nulo, nos quedamos con este parse
                        if ok.notna().any():
                            break
                    except Exception:
                        pass
                df[col] = ok
            else:
                df[col] = pd.to_datetime(df[col], errors="coerce")
        else:
            # Si el tipo no se reconoce, lo dejamos como está
            pass

    return df


# ===============================
# PIPELINE DE LIMPIEZA POR ARCHIVO
# ===============================
def limpiar_df_basico(
    df: pd.DataFrame,
    mapping_path: Path | None,
    schema_path: Path | None,
    cod_cols_mayus: list[str] | None = None,
) -> pd.DataFrame:
    """
    Limpieza básica en orden lógico:
    1) Estandariza headers (UPPER para 'enganchar' mapping)
    2) Aplica mapping de columnas (renombrar)
    3) Trimea strings
    4) Normaliza códigos (opcional: columnas pasadas en cod_cols_mayus)
    5) Aplica dtypes (incluye parseo de fechas)
    """
    mapping = _cargar_yaml(mapping_path) if mapping_path else {}
    schema = _cargar_yaml(schema_path) if schema_path else {}

    df = estandarizar_headers(df)
    df = aplicar_mapping(df, mapping)
    df = trim_strings(df)

    if cod_cols_mayus:
        df = normalizar_codigos(df, cod_cols_mayus)

    df = aplicar_dtypes(df, schema)


    return df


def limpiar_lote(
    dfs: dict,
    mappings_dir: Path,
    schemas_dir: Path,
    cod_cols_por_tabla: dict[str, list[str]] | None = None,
) -> dict:
    """
    Aplica 'limpiar_df_basico' a todos los dataframes de un lote.
    - dfs: {nombre_tabla: DataFrame} (ej.: 'almacenes': df)
    - mappings_dir: carpeta de YAML de mappings
    - schemas_dir: carpeta de YAML de schemas
    - cod_cols_por_tabla: {'articulos': ['cod_articulo'], ...}
    """
    salida = {}
    cod_cols_por_tabla = cod_cols_por_tabla or {}

    for nombre, df in dfs.items():
        mapping_path = mappings_dir / f"{nombre}.yaml"
        schema_path = schemas_dir / f"{nombre}.schema.yaml"
        cod_cols = cod_cols_por_tabla.get(nombre, [])

        print(f"[CLEAN] {nombre} (mapping: {mapping_path.name if mapping_path.exists() else '—'}, schema: {schema_path.name if schema_path.exists() else '—'})")
        limpio = limpiar_df_basico(df, mapping_path, schema_path, cod_cols_mayus=cod_cols)
        salida[nombre] = limpio

    return salida


# ===============================
# NORMALIZACION DE COLUMNAS DE PRECIO
# ===============================

def normalizar_precio(col: pd.Series) -> pd.Series:
    """
    Normaliza una columna de precios:
    - Si ya es numérica, solo redondea a 2 decimales.
    - Si viene como texto tipo '471,72000 €', la convierte a 471.72
    """

    # 1) Si ya es numérica, no la liamos: solo redondeamos
    if pd.api.types.is_numeric_dtype(col):
        return col.astype(float).round(2)

    # 2) Si viene como texto, la limpiamos
    s = col.astype(str).str.strip()
    s = s.str.replace("€", "", regex=False)
    s = s.str.replace("$", "", regex=False)

    # Nos interesan sobre todo los valores con coma (formato europeo)
    mask_coma = s.str.contains(",")

    # Parte con coma: tratamos '.' como separador de miles y ',' como decimal
    s_coma = s[mask_coma]
    s_coma = s_coma.str.replace(".", "", regex=False)   # '1.234,56' -> '1234,56'
    s_coma = s_coma.str.replace(",", ".", regex=False)  # '1234,56'  -> '1234.56'

    # Parte sin coma: la dejamos tal cual (puede ser '37.45' o '3745')
    s_sin_coma = s[~mask_coma]

    # Unimos de nuevo manteniendo el índice original
    s_limpia = pd.concat([s_coma, s_sin_coma]).sort_index()

    # Convertimos a número y redondeamos
    s_num = pd.to_numeric(s_limpia, errors="coerce").round(2)
    return s_num


