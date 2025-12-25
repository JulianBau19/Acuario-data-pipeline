
from __future__ import annotations
from sqlalchemy import text


def sync_dbo_to_stg(engine) -> int:
    """
    Para cada tabla en dbo, crear espejo en stg y copiar registros.
    Devuelve total de filas copiadas (suma de todas las tablas).
    """
    total_rows = 0

    with engine.begin() as conn:
        tables = conn.execute(text("""
    SELECT TABLE_NAME
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = 'dbo'
      AND TABLE_TYPE = 'BASE TABLE'
      AND TABLE_NAME <> 'sysdiagrams';
""")).fetchall()


        table_names = [row[0] for row in tables]

        for table in table_names:
            stg_table = f"stg.{table}"
            dbo_table = f"dbo.{table}"

            # 1) Eliminar STG si ya existe
            conn.execute(text(f"""
                IF OBJECT_ID('{stg_table}', 'U') IS NOT NULL
                    DROP TABLE {stg_table};
            """))

            # 2) Crear nueva STG con la estructura de DBO
            conn.execute(text(f"""
                SELECT TOP 0 *
                INTO {stg_table}
                FROM {dbo_table};
            """))

            # 3) Insertar datos
            result = conn.execute(text(f"""
                INSERT INTO {stg_table}
                SELECT * FROM {dbo_table};
            """))

            # rowcount a veces no es fiable en algunos drivers,
            # pero suele funcionar con INSERT SELECT en SQL Server.
            if result.rowcount is not None and result.rowcount >= 0:
                total_rows += result.rowcount

    return total_rows
