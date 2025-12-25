CREATE OR ALTER VIEW gold.vw_entradas
AS
SELECT
    f.cod_entrada,
    f.total_entrada,
    f.fecha_carga_gold,

    f.proveedor_key,
    f.almacen_key,
    f.fecha_key,

    dp.cod_proveedor,
    dp.nombre_proveedor,

    da.cod_almacen,
    da.nombre_almacen
FROM gold.fact_entradas AS f
JOIN gold.dim_proveedores AS dp
    ON dp.proveedor_key = f.proveedor_key
JOIN gold.dim_almacenes AS da
    ON da.almacen_key = f.almacen_key;
GO

