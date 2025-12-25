# Acuario Data Project (Python + SQL Server DWH)

Pipeline end-to-end para transformar datos operativos (Excel / Xlsx) en una base preparada para analítica (SQL Server), con logging de ejecución y trazabilidad por pasos.


## IMPORTANTE: Datos
Los datos utilizados en este proyecto no se incluyen por motivos de
confidencialidad. El pipeline es totalmente reproducible utilizando
datos de ejemplo con la misma estructura.

## Stack ##
- Python (pandas) + SQLAlchemy
- SQL Server
- Parquet (capa intermedia)
- Configuración por ficheros (mappings/schemas)

## Arquitectura ( alto nivel ) ##
**RAW (Excel) → PROCESSED (Parquet) → DBO (SQL) → STG (SQL) → CLN (SQL) → GOLD (SQL)**


Actualmente el entrypoint ejecuta:
- RAW → PROCESSED (Parquet)
- DBO → STG
- STG → CLN
y registra cada paso en tablas de logging (`clt.etl_*...`).

## Estructura del proyecto

scripts/
  run_pipeline.py          # Entry point único del pipeline
  load_to_sql.py           # (utilidad) carga a SQL
  preview_clean.py         # (utilidad) preview
  preview_processed.py     # (utilidad) preview
  listar_cabeceras.py      # (utilidad) inspección columnas
sql/
  ...                      # scripts SQL (Tables,constraints,views, etc.)
src/
  acuario/
    config.py              # rutas RAW/PROCESSED/ROOT
    db.py                  # get_engine() conexion a base de datos
    etl_logger.py          # logging de runs/steps
    io_load.py             # lectura Excel / XLSX
    transform_clean.py     # limpieza con mappings/schemas
    export.py              # guardar parquet
    create_stg_from_dbo.py # dbo → stg
    create_cln_from_stg.py # stg → cln

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
Proyecto en desarrollo continuo. La capa GOLD y automatización completa
forman parte del roadmap.

