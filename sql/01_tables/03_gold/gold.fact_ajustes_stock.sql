
CREATE TABLE gold.fact_ajustes_stock (
    articulo_key        int           NOT NULL,
    fecha_key           int           NOT NULL,
    cantidad_ajuste     int           NOT NULL,
    motivo              varchar(60)   NOT NULL,
    fecha_carga_gold    datetime2     NOT NULL
);
