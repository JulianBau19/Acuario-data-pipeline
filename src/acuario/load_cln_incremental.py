# MOVER DATOS DE STG A CLN SIN DUPLICAR NADA
#


from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple
from sqlalchemy import text
from acuario.business_keys import BUSINESS_KEYS


@dataclass
class TableLoadResult:
    table: str
    inserted_rows: int


def _table_exists(conn, schema: str, table: str) -> bool:
    return conn.execute(
        text(
            """
            SELECT 1
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = :schema
              AND TABLE_NAME = :table
            """
        ),
        {"schema": schema, "table": table},
    ).scalar() is not None


def _get_table_columns(conn, schema: str, table: str) -> List[str]:
    rows = conn.execute(
        text(
            """
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = :schema
              AND TABLE_NAME = :table
            ORDER BY ORDINAL_POSITION
            """
        ),
        {"schema": schema, "table": table},
    ).fetchall()
    return [r[0] for r in rows]


def _ensure_schema_exists(conn, schema: str) -> None:
    # SQL Server: crear schema si no existe
    conn.execute(
        text(
            f"""
            IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = :schema)
            BEGIN
                EXEC('CREATE SCHEMA {schema}')
            END
            """
        ),
        {"schema": schema},
    )


def load_cln_incremental(engine, stg_schema: str = "stg", cln_schema: str = "cln") -> Dict[str, TableLoadResult]:
    """
    Carga incremental STG -> CLN sin duplicados (solo inserts nuevos).
    NO borra tablas.
    Usa BUSINESS_KEYS (acuario.business_keys).
    """
    results: Dict[str, TableLoadResult] = {}

    with engine.begin() as conn:
        _ensure_schema_exists(conn, cln_schema)

        for table, cfg in BUSINESS_KEYS.items():
            used = bool(cfg.get("used", False))
            keys: List[str] = list(cfg.get("keys", []))

            if not used:
                continue

            if not keys:
                print(f"[WARN] Saltando {table}: used=True pero keys está vacío.")
                continue

            # 1) STG debe existir
            if not _table_exists(conn, stg_schema, table):
                print(f"[WARN] Saltando {table}: no existe {stg_schema}.{table}.")
                continue

            # 2) Si CLN no existe, crearla vacía con mismas columnas + fecha_carga_cln
            if not _table_exists(conn, cln_schema, table):
                # Nota: aquí creamos la estructura con SELECT TOP 0
                conn.execute(
                    text(
                        f"""
                        SELECT TOP 0
                            s.*,
                            SYSUTCDATETIME() AS [fecha_carga_cln]
                        INTO {cln_schema}.{table}
                        FROM {stg_schema}.{table} s;
                        """
                    )
                )
                print(f"[INFO] Creada tabla {cln_schema}.{table} (vacía).")

            # 3) Insertar solo nuevos (deduplicación por business key)
            stg_cols = _get_table_columns(conn, stg_schema, table)

            # columnas destino = todas las de stg + fecha_carga_cln
            insert_cols_sql = ", ".join([f"[{c}]" for c in stg_cols] + ["[fecha_carga_cln]"])

            select_cols_sql = ", ".join([f"s.[{c}]" for c in stg_cols] + ["SYSUTCDATETIME()"])

            # condición de "ya existe" por business key (soporta compuesta)
            exists_pred = " AND ".join([f"c.[{k}] = s.[{k}]" for k in keys])

            res = conn.execute(
                text(
                    f"""
                    INSERT INTO {cln_schema}.{table} ({insert_cols_sql})
                    SELECT {select_cols_sql}
                    FROM {stg_schema}.{table} s
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM {cln_schema}.{table} c
                        WHERE {exists_pred}
                    );
                    """
                )
            )

            inserted = int(res.rowcount) if res.rowcount and res.rowcount > 0 else 0
            results[table] = TableLoadResult(table=table, inserted_rows=inserted)

            print(f"[OK] {cln_schema}.{table}: insertadas {inserted} filas nuevas.")

    return results


if __name__ == "__main__":
    # ejecución manual
    from acuario.db import get_engine

    engine = get_engine()
    out = load_cln_incremental(engine)
    total = sum(r.inserted_rows for r in out.values())
    print(f"\n CLN incremental finalizado. Total filas nuevas: {total}")
