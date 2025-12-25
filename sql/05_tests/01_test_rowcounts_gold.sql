SELECT 'dim_fecha' AS tabla, COUNT(*) AS rows FROM gold.dim_fecha
UNION ALL SELECT 'dim_almacenes', COUNT(*) FROM gold.dim_almacenes
UNION ALL SELECT 'dim_familias', COUNT(*) FROM gold.dim_familias
UNION ALL SELECT 'dim_articulos', COUNT(*) FROM gold.dim_articulos
UNION ALL SELECT 'dim_clientes', COUNT(*) FROM gold.dim_clientes
UNION ALL SELECT 'dim_proveedores', COUNT(*) FROM gold.dim_proveedores
UNION ALL SELECT 'fact_entradas', COUNT(*) FROM gold.fact_entradas
UNION ALL SELECT 'fact_entradas_linea', COUNT(*) FROM gold.fact_entradas_linea
UNION ALL SELECT 'fact_facturas', COUNT(*) FROM gold.fact_facturas
UNION ALL SELECT 'fact_facturas_linea', COUNT(*) FROM gold.fact_facturas_linea
UNION ALL SELECT 'fact_listado_de_tarifas', COUNT(*) FROM gold.fact_listado_de_tarifas
UNION ALL SELECT 'fact_stock_actual', COUNT(*) FROM gold.fact_stock_actual
UNION ALL SELECT 'fact_ajustes_stock', COUNT(*) FROM gold.fact_ajustes_stock;
