CREATE TABLE gold.dim_familias (
    familia_key        int            IDENTITY(1,1) NOT NULL,
    codigo_familia     varchar(50)    NOT NULL,
    descripcion        varchar(255)   NOT NULL,
    fecha_carga_gold   datetime2      NOT NULL
);
