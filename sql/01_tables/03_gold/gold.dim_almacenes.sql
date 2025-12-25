CREATE TABLE gold.dim_almacenes (
    almacen_key        int          IDENTITY(1,1) NOT NULL,
    cod_almacen        varchar(50)  NOT NULL,
    nombre_almacen     varchar(50)  NOT NULL,
    fecha_carga_gold   datetime2    NOT NULL
);
