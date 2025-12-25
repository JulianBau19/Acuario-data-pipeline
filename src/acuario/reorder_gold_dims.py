# src/acuario/reorder_gold_dims.py

from sqlalchemy import create_engine, text

SERVER = "localhost"
DATABASE = "acuario_dwh"
DRIVER = "ODBC Driver 17 for SQL Server"

connection_string = (
    f"mssql+pyodbc://@{SERVER}/{DATABASE}"
    f"?driver={DRIVER}&trusted_connection=yes"
)

engine = create_engine(connection_string)


def get_dim_tables(conn):
    result = conn.execute(text("""
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = 'gold'
          AND TABLE_NAME LIKE 'dim_%';
    """)).fetchall()
    return [r[0] for r in result]


def get_columns(conn, table_name):
    result = conn.execute(text(f"""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = 'gold'
          AND TABLE_NAME = '{table_name}'
        ORDER BY ORDINAL_POSITION;
    """)).fetchall()
    return [r[0] for r in result]


def reorder_columns(cols):
    cols_lower = [c.lower() for c in cols]

    # 1) surrogate keys (terminan en _key)
    sk = [c for c in cols if c.lower().endswith("_key")]

    # 2) business keys (empiezan por cod_ o id_)
    bk = [c for c in cols
          if (c.lower().startswith("cod_") or c.lower().startswith("id_"))
          and c not in sk]

    # 3) auditoría
    audit = [c for c in cols if c.lower() in ("fecha_carga_gold", "fecha_carga_cln")]

    # 4) resto de columnas
    others = [c for c in cols if c not in sk + bk + audit]

    # Orden final
    return sk + bk + others + audit


def main():
    with engine.begin() as conn:
        dim_tables = get_dim_tables(conn)
        print("Dimensiones encontradas en GOLD:", dim_tables)

        for table in dim_tables:
            cols = get_columns(conn, table)
            ordered = reorder_columns(cols)

            select_list = ",\n    ".join(f"[{c}]" for c in ordered)

            sql = f"""
-- Reordenar columnas de gold.{table}
SELECT
    {select_list}
INTO gold.{table}_new
FROM gold.{table};

-- Cuando verifiques que está OK:
-- DROP TABLE gold.{table};
-- EXEC sp_rename 'gold.{table}_new', '{table}';
"""
            print(sql)


if __name__ == "__main__":
    main()
