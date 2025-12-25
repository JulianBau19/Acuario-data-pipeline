# src/acuario/create_cln_from_stg.py

from __future__ import annotations

from sqlalchemy import text


# =====================================================
# FUNCIONES DE LIMPIEZA (igual que antes)
# =====================================================
def proper_case_sql(col: str) -> str:
    col_quoted = f"[{col}]"
    return f"""
        CASE
            WHEN {col_quoted} IS NULL THEN NULL
            ELSE CONCAT(
                UPPER(LEFT({col_quoted}, 1)),
                LOWER(SUBSTRING({col_quoted}, 2, LEN({col_quoted})))
            )
        END AS {col_quoted}
    """


def limpiar_texto_sql(col: str) -> str:
    col_quoted = f"[{col}]"
    return f"""
        CASE
            WHEN LTRIM(RTRIM({col_quoted})) IN ('', 'NULL', 'null', 'None', 'none',
                                                'N/A', 'n/a', 'NA', 'na', 'nan', 'NaN')
                THEN NULL
            ELSE LTRIM(RTRIM({col_quoted}))
        END AS {col_quoted}
    """


def limpiar_fecha_sql(col: str) -> str:
    col_quoted = f"[{col}]"
    return f"""
        CASE
            WHEN ISDATE({col_quoted}) = 1
                THEN CAST({col_quoted} AS DATETIME2)
            ELSE NULL
        END AS {col_quoted}
    """


def limpiar_num_sql(col: str) -> str:
    col_quoted = f"[{col}]"
    return f"""
        CASE
            WHEN ISNUMERIC({col_quoted}) = 1
                THEN {col_quoted}
            ELSE NULL
        END AS {col_quoted}
    """


# =====================================================
# GENERADOR DINÁMICO DEL SELECT LIMPIO
# =====================================================
def generar_select_limpio(conn, table_name: str) -> str:
    cols = conn.execute(text(f"""
        SELECT COLUMN_NAME, DATA_TYPE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = 'stg'
          AND TABLE_NAME = :table_name
        ORDER BY ORDINAL_POSITION;
    """), {"table_name": table_name}).fetchall()

    select_parts: list[str] = []

    for col_name, data_type in cols:
        col_lower = col_name.lower()

        if col_lower == "almacen":
            select_parts.append("""
        CASE
            WHEN [almacen] IS NULL THEN 'ACT'
            ELSE [almacen]
        END AS [almacen]
    """)
        elif col_lower in (
            "nombre", "nombre_cliente", "cliente", "apellido",
            "razon_social", "nombre_proveedor"
        ):
            select_parts.append(proper_case_sql(col_name))

        elif data_type in ("nvarchar", "varchar", "char", "nchar", "text"):
            select_parts.append(limpiar_texto_sql(col_name))

        elif data_type in ("date", "datetime", "datetime2", "smalldatetime"):
            select_parts.append(limpiar_fecha_sql(col_name))

        elif data_type in ("int", "bigint", "smallint", "tinyint", "float",
                           "numeric", "decimal", "money"):
            select_parts.append(limpiar_num_sql(col_name))

        else:
            select_parts.append(f"[{col_name}]")

    select_parts.append("SYSUTCDATETIME() AS fecha_carga_cln")
    return ",\n    ".join(select_parts)


# =====================================================
# PROCESO PRINCIPAL
# =====================================================
def create_cln_tables(engine) -> int:
    """
    Crea tablas cln.* a partir de stg.* aplicando reglas de limpieza.
    Devuelve total de filas creadas (suma de todas las tablas).
    """
    total_rows = 0

    with engine.begin() as conn:
        result = conn.execute(text("""
            SELECT TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = 'stg'
              AND TABLE_TYPE = 'BASE TABLE';
        """)).fetchall()

        stg_tables = [row[0] for row in result]

        for table in stg_tables:
            # drop cln
            conn.execute(text(f"""
                IF OBJECT_ID('cln.{table}', 'U') IS NOT NULL
                    DROP TABLE cln.{table};
            """))

            select_sql = generar_select_limpio(conn, table)

            create_sql = f"""
                SELECT
                    {select_sql}
                INTO cln.{table}
                FROM stg.{table};
            """
            conn.execute(text(create_sql))

            # contar filas creadas para logging
            cnt = conn.execute(text(f"SELECT COUNT(1) FROM cln.{table};")).scalar()
            if cnt is not None:
                total_rows += int(cnt)

    return total_rows


if __name__ == "__main__":
    # Ejecución manual (útil para debug). Mantiene compatibilidad.
    from acuario.db import get_engine
    engine = get_engine()
    rows = create_cln_tables(engine)
    print(f"✅ CLN creado. Total filas: {rows}")
