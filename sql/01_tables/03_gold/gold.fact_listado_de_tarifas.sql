CREATE TABLE gold.fact_listado_de_tarifas (
    articulo_key        int             NOT NULL,
    fecha_tarifa_key    int             NULL,
    precio_de_venta     decimal(10,2)   NOT NULL,
    fecha_carga_gold    datetime2       NOT NULL
);
