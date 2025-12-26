
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List
from sqlalchemy import text
from acuario.business_keys import BUSINESS_KEYS


@dataclass
class ConstraintResult:
    table: str
    created: bool
    index_name: str


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


def _unique_index_exists(conn, schema: str, table: str, index_name: str) -> bool:
    return conn.execute(
        text(
            """
            SELECT 1
            FROM sys.indexes i
            JOIN sys.objects o ON o.object_id = i.object_id
            JOIN sys.schemas s ON s.schema_id = o.schema_id
            WHERE s.name = :schema
              AND o.name = :table
              AND i.name = :index_name
            """
        ),
        {"schema": schema, "table": table, "index_name": index_name},
    ).scalar() is not None


def _safe_index_name(schema: str, table: str, keys: List[str]) -> str:
    # Nombre estable y legible (sin espacios, ni símbolos raros)
    keys_part = "_".join([k.lower() for k in keys])
    return f"UQ_{schema}_{table}_{keys_part}"


def ensure_cln_unique_constraints(engine, cln_schema: str = "cln") -> Dict[str, ConstraintResult]:
    """
    Crea índices UNIQUE en CLN según BUSINESS_KEYS.
    - No falla si ya existen.
    - Salta tablas no usadas o sin keys.
    - Salta tablas CLN inexistentes.
    """
    results: Dict[str, ConstraintResult] = {}

    with engine.begin() as conn:
        for table, cfg in BUSINESS_KEYS.items():
            used = bool(cfg.get("used", False))
            keys: List[str] = list(cfg.get("keys", []))

            if not used:
                continue

            if not keys:
                print(f"[WARN] Saltando {table}: used=True pero keys vacío.")
                continue

            if not _table_exists(conn, cln_schema, table):
                print(f"[WARN] Saltando {cln_schema}.{table}: tabla no existe (aún).")
                continue

            index_name = _safe_index_name(cln_schema, table, keys)

            if _unique_index_exists(conn, cln_schema, table, index_name):
                results[table] = ConstraintResult(table=table, created=False, index_name=index_name)
                print(f"[OK] {cln_schema}.{table}: UNIQUE ya existe ({index_name}).")
                continue

            cols_sql = ", ".join([f"[{k}]" for k in keys])

            # Creamos UNIQUE INDEX
            conn.execute(
                text(
                    f"""
                    CREATE UNIQUE INDEX [{index_name}]
                    ON {cln_schema}.{table} ({cols_sql});
                    """
                )
            )

            results[table] = ConstraintResult(table=table, created=True, index_name=index_name)
            print(f"[OK] {cln_schema}.{table}: UNIQUE creado ({index_name}).")

    return results


if __name__ == "__main__":
    from acuario.db import get_engine

    engine = get_engine()
    out = ensure_cln_unique_constraints(engine)
    created = sum(1 for r in out.values() if r.created)
    print(f"\n✅ Constraints UNIQUE revisados. Creados nuevos: {created}")
