CREATE TABLE gold.dim_proveedores (
    proveedor_key       int           IDENTITY(1,1) NOT NULL,
    cod_proveedor       int           NOT NULL,
    nombre_proveedor    varchar(50)   NULL,
    fecha_carga_gold    datetime2     NOT NULL
);
