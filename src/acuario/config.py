from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
## Carpeta raiz del proyecto (2 niveles por encima de este archivo)


# Carpeta de datos
DATA = ROOT / "data"
RAW = DATA / "raw"
INTERIM = DATA / "interim"
PROCESSED = DATA / "processed"
# Carpeta de informes
REPORTS = ROOT / "reports"
LOGS = REPORTS / "logs"

for p in (RAW, INTERIM, PROCESSED, LOGS):
    p.mkdir(parents=True, exist_ok=True)


