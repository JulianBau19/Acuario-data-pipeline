CREATE OR ALTER VIEW gold.vw_entradas_linea
AS
SELECT
    fel.cod_entrada,
    fel.num_linea,
    fel.fecha_key,
    df.fecha            AS fecha_entrada,
    df.anio,
    df.mes,

    fel.proveedor_key,
    dp.cod_proveedor,
    dp.nombre_proveedor AS proveedor,

    fel.almacen_key,
    da.cod_almacen,
    da.nombre_almacen   AS almacen,

    fel.articulo_key,
    dar.cod_articulo,
    dar.nombre          AS articulo,
    dar.familia_key,

    fel.cantidad,
    fel.precio_unitario,
    fel.total_linea     AS total_linea_sin_iva,
    fel.iva_pct,
    fel.iva_linea,
    (fel.total_linea + fel.iva_linea) AS total_linea_con_iva,

    fel.fecha_carga_gold
FROM gold.fact_entradas_linea AS fel
JOIN gold.dim_fecha AS df
    ON df.fecha_key = fel.fecha_key
JOIN gold.dim_proveedores AS dp
    ON dp.proveedor_key = fel.proveedor_key
JOIN gold.dim_almacenes AS da
    ON da.almacen_key = fel.almacen_key
JOIN gold.dim_articulos AS dar
    ON dar.articulo_key = fel.articulo_key;
GO
