-- fact_facturas -> dim_clientes
SELECT TOP 50 ff.*
FROM gold.fact_facturas ff
LEFT JOIN gold.dim_clientes dc
  ON dc.cliente_key = ff.cliente_key
WHERE dc.cliente_key IS NULL;

-- fact_facturas -> dim_fecha
SELECT TOP 50 ff.*
FROM gold.fact_facturas ff
LEFT JOIN gold.dim_fecha df
  ON df.fecha_key = ff.fecha_factura_key
WHERE df.fecha_key IS NULL;

-- fact_entradas_linea -> dim_articulos
SELECT TOP 50 fel.*
FROM gold.fact_entradas_linea fel
LEFT JOIN gold.dim_articulos da
  ON da.articulo_key = fel.articulo_key
WHERE da.articulo_key IS NULL;
