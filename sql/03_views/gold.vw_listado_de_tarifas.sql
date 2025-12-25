CREATE OR ALTER VIEW gold.vw_listado_de_tarifas
AS
SELECT
    flt.articulo_key,
    da.cod_articulo,
    da.nombre,
    df.codigo_familia,
    df.descripcion,
    flt.precio_de_venta,
    flt.fecha_carga_gold
FROM gold.fact_listado_de_tarifas AS flt
JOIN gold.dim_articulos AS da
    ON da.articulo_key = flt.articulo_key
LEFT JOIN gold.dim_familias AS df
    ON df.familia_key = da.familia_key;
GO


