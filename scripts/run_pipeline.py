from __future__ import annotations
from pathlib import Path
from typing import Callable, Any, Dict
from acuario.load_cln_incremental import load_cln_incremental
from acuario.ensure_cln_unique_constraints import ensure_cln_unique_constraints
from acuario.config import RAW, PROCESSED, ROOT
from acuario.io_load import leer_excels
from acuario.export import guardar_parquet
from acuario.transform_clean import limpiar_lote
from acuario.db import get_engine
from acuario.etl_logger import (
    etl_log_start,
    etl_log_end_ok,
    etl_log_end_error,
    etl_step_start,
    etl_step_end,
)
from acuario.create_stg_from_dbo import sync_dbo_to_stg
from acuario.create_cln_from_stg import create_cln_tables



# ─────────────────────────────
# CONFIG (por ahora aquí; luego lo pasamos a YAML/ENV)
# ─────────────────────────────
PIPELINE_NAME = "processed_pipeline"
LAYER_NAME = "cln"
TARGET_OBJECT = "data/processed (parquet)"

MAPPINGS_DIR = ROOT / "config" / "mappings"
SCHEMAS_DIR = ROOT / "config" / "schemas"

COD_COLS_POR_TABLA = {
    "almacenes": ["cod_almacen"],
    "articulos": ["cod_articulo"],
    "clientes": ["cod_cliente"],
    "proveedores": ["cod_proveedor"],
    "entradas": ["cod_proveedor", "cod_almacen"],
    "entradas_linea": ["num_documento", "cod_articulo"],
    "facturas": ["num_factura", "cod_cliente"],
    "facturas_linea": ["num_factura", "cod_articulo"],
    "stock": ["cod_articulo", "cod_almacen"],
}


def run_step(engine, control_id: int, step_name: str, fn):
    step_id = etl_step_start(engine, control_id, step_name)

    try:
        # IMPORTANTE: aquí se ejecuta fn(), NO run_step()
        result = fn()

        row_count = None
        if isinstance(result, int):
            row_count = result
        elif isinstance(result, dict):
            try:
                row_count = sum(len(df) for df in result.values())
            except Exception:
                row_count = None

        etl_step_end(engine, step_id, status="OK", row_count=row_count)
        return result

    except Exception as e:
        etl_step_end(engine, step_id, status="ERROR", message=str(e))
        raise




def main() -> None:
    engine = get_engine()
    control_id = None

    try:
        # START RUN
        _, control_id = etl_log_start(
            engine=engine,
            pipeline_name=PIPELINE_NAME,
            layer_name=LAYER_NAME,
            target_object=TARGET_OBJECT,
        )
        print(f"[LOG_START] control_id={control_id}")

        # STEP 1: READ RAW
        dfs = run_step(
            engine,
            control_id,
            "read_raw",
            lambda: leer_excels(RAW),
        )

        # STEP 2: CLEAN BATCH
        dfs_limpios = run_step(
            engine,
            control_id,
            "clean_batch",
            lambda: limpiar_lote(
                dfs,
                MAPPINGS_DIR,
                SCHEMAS_DIR,
                cod_cols_por_tabla=COD_COLS_POR_TABLA,
            ),
        )

        # STEP 3: WRITE PROCESSED
        run_step(
            engine,
            control_id,
            "write_processed",
            lambda: guardar_parquet(dfs_limpios, PROCESSED),
        )
        # STEP 4: DBO → STG
        run_step(
            engine,
            control_id,
            "dbo_to_stg",
            lambda: sync_dbo_to_stg(engine),
        )

        # STEP 5: STG → CLN incremental (solo nuevos, deduplicado)
        run_step(
            engine,
            control_id,
            "stg_to_cln_incremental",
            lambda: load_cln_incremental(engine),
        )

        # # STEP 6: asegurar UNIQUE en CLN (blindaje anti-duplicados)
        # run_step(
        #     engine,
        #     control_id,
        #     "cln_unique_constraints",
        #     lambda: ensure_cln_unique_constraints(engine),
        # )



        # END RUN OK
        etl_log_end_ok(engine, control_id=control_id, rows_inserted=None)
        print("\nOK. Archivos limpios en data/processed/")

    except Exception as e:
        if control_id is not None:
            try:
                etl_log_end_error(engine, control_id=control_id, error_message=str(e))
            except Exception as log_err:
                print(f"[LOGGER ERROR] {log_err}")
        raise


if __name__ == "__main__":
    main()
