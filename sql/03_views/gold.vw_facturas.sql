CREATE OR ALTER VIEW gold.vw_facturas
AS
SELECT
    ff.factura_key,
    ff.tipo_factura,
    ff.num_factura,

    df.fecha        AS fecha_factura,
    df.anio,
    df.mes,

    ff.cliente_key,
    dc.cod_cliente,
    dc.nombre_cliente,

    ff.total_base,
    ff.total_iva,
    ff.total_factura,

    ff.fecha_carga_gold
FROM gold.fact_facturas AS ff
JOIN gold.dim_fecha AS df
    ON df.fecha_key = ff.fecha_factura_key
JOIN gold.dim_clientes AS dc
    ON dc.cliente_key = ff.cliente_key;
GO
