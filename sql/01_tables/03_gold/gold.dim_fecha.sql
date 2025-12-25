CREATE TABLE gold.dim_fecha (
    fecha_key          int         NOT NULL,
    fecha              date        NOT NULL,
    anio               smallint    NOT NULL,
    trimestre          tinyint     NOT NULL,
    mes                tinyint     NOT NULL,
    dia                tinyint     NOT NULL,
    dia_semana         tinyint     NOT NULL,
    nombre_mes         varchar(15) NOT NULL,
    es_fin_de_semana   bit         NOT NULL,
    fecha_carga_gold   datetime2   NOT NULL
);
