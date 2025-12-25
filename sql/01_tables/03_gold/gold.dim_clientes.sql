CREATE TABLE gold.dim_clientes (
    cliente_key        int            IDENTITY(1,1) NOT NULL,
    cod_cliente        varchar(50)    NOT NULL,
    nombre_cliente     varchar(255)   NULL,
    fecha_carga_gold   datetime2      NOT NULL
);
