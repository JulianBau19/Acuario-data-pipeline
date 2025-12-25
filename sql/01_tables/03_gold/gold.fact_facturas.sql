CREATE TABLE gold.fact_facturas (
    factura_key          int             IDENTITY(1,1) NOT NULL,
    tipo_factura         tinyint         NOT NULL,
    num_factura          int             NOT NULL,
    cliente_key          int             NOT NULL,
    fecha_factura_key    int             NOT NULL,
    total_base           decimal(18,2)   NOT NULL,
    total_iva            decimal(18,2)   NOT NULL,
    total_factura        decimal(18,2)   NOT NULL,
    fecha_carga_gold     datetime2       NOT NULL
);

