CREATE OR ALTER VIEW gold.vw_facturas_linea
AS
SELECT
    ff.tipo_factura,
    ff.num_factura,

    ffl.num_linea,
    ffl.factura_key,

    ffl.articulo_key,
    da.cod_articulo,
    da.nombre,
    da.familia_key,

    ff.cliente_key,
    dc.cod_cliente,
    dc.nombre_cliente,

    ff.fecha_factura_key,
    df.fecha              AS fecha_factura,
    df.anio,
    df.mes,
    df.nombre_mes,

    ffl.cantidad,
    ffl.total_linea,
    ffl.iva_linea,
    (ffl.total_linea + ffl.iva_linea) AS total_linea_con_iva,

    ffl.fecha_carga_gold
FROM gold.fact_facturas_linea AS ffl
JOIN gold.fact_facturas AS ff
    ON ff.factura_key = ffl.factura_key
JOIN gold.dim_fecha AS df
    ON df.fecha_key = ff.fecha_factura_key
JOIN gold.dim_clientes AS dc
    ON dc.cliente_key = ff.cliente_key
JOIN gold.dim_articulos AS da
    ON da.articulo_key = ffl.articulo_key;
GO
