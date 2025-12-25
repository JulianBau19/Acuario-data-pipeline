CREATE TABLE gold.dim_articulos (
    articulo_key        int            IDENTITY(1,1) NOT NULL,
    cod_articulo        varchar(50)    NOT NULL,
    nombre              varchar(255)   NOT NULL,
    costo               decimal(18,4)  NULL,
    fecha_alta          datetime2      NULL,
    familia_key         int            NULL,
    almacen_key         int            NULL,
    fecha_carga_gold    datetime2      NOT NULL
);
