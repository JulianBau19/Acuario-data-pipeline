CREATE TABLE gold.fact_facturas_linea (
    factura_linea_key     int             IDENTITY(1,1) NOT NULL,
    factura_key           int             NOT NULL,
    num_linea             int             NOT NULL,
    articulo_key          int             NOT NULL,
    fecha_factura_key     int             NOT NULL,
    cantidad               decimal(18,4)  NOT NULL,
    total_linea            decimal(18,4)  NOT NULL,
    iva_linea              decimal(18,4)  NOT NULL,
    fecha_carga_gold       datetime2      NOT NULL
);
