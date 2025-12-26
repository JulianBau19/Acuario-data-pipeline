# Acuario Data Project (Python + SQL Server DWH)
# Pipeline de data engineering end to end

Pipeline end-to-end de Ingeniería de Datos para transformar datos operativos (Excel / XLSX) en un Data Warehouse en SQL Server, con logging de ejecución y trazabilidad completa por pasos.

## IMPORTANTE: Datos
Los datos utilizados en este proyecto no se incluyen por motivos de confidencialidad.
El pipeline es completamente reproducible utilizando datos de ejemplo que respeten la misma estructura y esquemas.


## Stack ##
- Python (pandas) + SQLAlchemy
- SQL Server
- Parquet (capa intermedia)
- Configuración por ficheros (mappings / schemas desacoplados del código)

## Arquitectura ( alto nivel ) ##
**RAW (Excel) → PROCESSED (Parquet) → DBO (SQL) → STG (SQL) → CLN (SQL) → GOLD (SQL)**
Arquitectura por capas inspirada en entornos productivos de Data Engineering, separando ingesta, limpieza, estandarización y modelado analítico.


Actualmente el entrypoint (`run_pipeline.py`) ejecuta:
- RAW → PROCESSED (Parquet)
- DBO → STG
- STG → CLN
y registra cada paso en tablas de logging (`clt.etl_*...`).
La arquitectura está preparada para extenderse a cargas incrementales, capa GOLD y orquestación automática.


## Estructura del proyecto

scripts/
  run_pipeline.py          # Entry point único del pipeline
  load_to_sql.py           # utilidad: carga a SQL
  preview_clean.py         # utilidad: preview CLN
  preview_processed.py     # utilidad: preview Parquet
  listar_cabeceras.py      # utilidad: inspección columnas
sql/
  ...                      # scripts SQL (tables, constraints, views)
src/
  acuario/
    config.py
    db.py
    etl_logger.py
    io_load.py
    transform_clean.py
    export.py
    create_stg_from_dbo.py
    create_cln_from_stg.py


## Requisitos para correrlo

Python 3.10+ (recomendado)
SQL Server local (o accesible)
ODBC Driver 17 for SQL Server


## Instalación

python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

## EJECUCION DEL PIPELINE: Desde la raiz del proyecto : python scripts/run_pipeline.py


## Carga a SQL Server (dbo)

La carga de datos a SQL Server se realiza a partir de los ficheros Parquet generados por el pipeline Python.

El script `scripts/load_to_sql.py`:
- lee todos los `.parquet` desde `data/processed/`
- crea (o reemplaza) tablas en el esquema `dbo`
- usa el nombre del archivo como nombre de tabla

## Logging y control de ejecuciones

El pipeline registra todas las ejecuciones y pasos en el esquema `clt` de SQL Server.

### Tablas

- `clt.etl_runs`: información general de cada ejecución
- `clt.etl_steps`: detalle por paso (estado, timestamps, filas procesadas, errores)

### Ejemplo de pasos registrados
- `read_raw`
- `clean_batch`
- `write_processed`
- `dbo_to_stg`
- `stg_to_cln`

Esto permite trazabilidad completa y facilita el debugging y monitoreo del pipeline.



## Estado del proyecto

✔ Ingesta y procesamiento funcional  
✔ Capas DBO, STG y CLN implementadas  
✔ Logging y trazabilidad completos  

PROXIMO: Implementación de capa GOLD e integración con orquestador (Airflow / cron)

