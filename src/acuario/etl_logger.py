import uuid
from sqlalchemy import text
from sqlalchemy.engine import Engine


def etl_log_start(engine: Engine, pipeline_name: str, layer_name: str, target_object: str):
    run_id = str(uuid.uuid4())

    sql = text("""
        INSERT INTO ctl.etl_control_cargas
            (pipeline_name, layer_name, target_object, run_id, start_time, status)
        OUTPUT INSERTED.control_id
        VALUES
            (:pipeline_name, :layer_name, :target_object, :run_id, SYSDATETIME(), 'RUNNING');
    """)

    with engine.begin() as conn:
        control_id = conn.execute(sql, {
            "pipeline_name": pipeline_name,
            "layer_name": layer_name,
            "target_object": target_object,
            "run_id": run_id
        }).scalar_one()

    return run_id, control_id

def etl_log_end_ok(engine: Engine, control_id: int, rows_inserted: int | None = None):
    sql = text("""
        UPDATE ctl.etl_control_cargas
        SET end_time = SYSDATETIME(),
            status = 'OK',
            rows_inserted = :rows_inserted,
            error_message = NULL
        WHERE control_id = :control_id;
    """)
    with engine.begin() as conn:
        conn.execute(sql, {"control_id": control_id, "rows_inserted": rows_inserted})


def etl_log_end_error(engine: Engine, control_id: int, error_message: str):
    sql = text("""
        UPDATE ctl.etl_control_cargas
        SET end_time = SYSDATETIME(),
            status = 'ERROR',
            error_message = :error_message
        WHERE control_id = :control_id;
    """)
    with engine.begin() as conn:
        conn.execute(sql, {"control_id": control_id, "error_message": error_message[:4000]})



def etl_step_start(engine: Engine, control_id: int, step_name: str) -> int:
    """
    Abre un paso de ejecución y devuelve step_id
    """
    sql = text("""
        INSERT INTO ctl.etl_steps (control_id, step_name, status)
        OUTPUT INSERTED.step_id
        VALUES (:control_id, :step_name, 'RUNNING');
    """)

    with engine.begin() as conn:
        step_id = conn.execute(sql, {
            "control_id": control_id,
            "step_name": step_name
        }).scalar_one()

    return step_id


def etl_step_end(
    engine: Engine,
    step_id: int,
    status: str,
    row_count: int | None = None,
    message: str | None = None
):
    """
    Cierra un paso de ejecución (OK o ERROR)
    """
    if status not in ("OK", "ERROR"):
        raise ValueError("status debe ser 'OK' o 'ERROR'")

    sql = text("""
        UPDATE ctl.etl_steps
        SET
            end_time = SYSDATETIME(),
            status = :status,
            row_count = :row_count,
            message = :message
        WHERE step_id = :step_id;
    """)

    with engine.begin() as conn:
        result = conn.execute(sql, {
            "step_id": step_id,
            "status": status,
            "row_count": row_count,
            "message": message[:4000] if message else None
        })

        if result.rowcount != 1:
            raise RuntimeError(
                f"etl_step_end no actualizó filas (step_id={step_id})"
            )