CREATE TABLE gold.fact_entradas (
    cod_entrada         int             NOT NULL,
    proveedor_key       int             NOT NULL,
    almacen_key         int             NOT NULL,
    total_entrada       decimal(10,2)   NOT NULL,
    fecha_key           int             NOT NULL,
    fecha_carga_gold    datetime2       NOT NULL
);
