CREATE TABLE gold.fact_stock_actual (
    articulo_key        int           NOT NULL,
    stock_actual        int           NOT NULL,
    fecha_carga_gold    datetime2     NOT NULL
);
