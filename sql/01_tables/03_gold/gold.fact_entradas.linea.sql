CREATE TABLE gold.fact_entradas_linea (
    entrada_linea_key   int             IDENTITY(1,1) NOT NULL,
    cod_entrada          int             NOT NULL,
    num_linea            bigint          NOT NULL,
    articulo_key         int             NOT NULL,
    proveedor_key        int             NOT NULL,
    almacen_key          int             NOT NULL,
    fecha_key            int             NOT NULL,
    cantidad              decimal(18,4)  NOT NULL,
    precio_unitario       decimal(18,4)  NOT NULL,
    total_linea           decimal(18,4)  NOT NULL,
    iva_pct               decimal(6,4)   NOT NULL,
    iva_linea             decimal(18,4)  NOT NULL,
    fecha_carga_gold      datetime2      NOT NULL
);
