from sqlalchemy import create_engine
from urllib.parse import quote_plus


def get_engine():
    """
    Crea y devuelve un SQLAlchemy Engine para SQL Server (SSMS).

    - Usa el driver ODBC 17.
    - Usa autenticación integrada de Windows (Trusted_Connection).
    - Cambia SERVER y DATABASE si lo necesitas.
    """

    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"      # nombre del servidor
        "DATABASE=acuario_dwh;"      # nombre de tu BD
        "Trusted_Connection=yes;"
    )

    params = quote_plus(conn_str)

    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    return engine
