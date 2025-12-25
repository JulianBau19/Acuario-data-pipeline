-- Artículos: cod_articulo no debe repetirse
SELECT cod_articulo, COUNT(*) c
FROM gold.dim_articulos
GROUP BY cod_articulo
HAVING COUNT(*) > 1;

-- Proveedores: cod_proveedor no debe repetirse
SELECT cod_proveedor, COUNT(*) c
FROM gold.dim_proveedores
GROUP BY cod_proveedor
HAVING COUNT(*) > 1;

-- Facturas: (tipo_factura, num_factura) no debe repetirse
SELECT tipo_factura, num_factura, COUNT(*) c
FROM gold.fact_facturas
GROUP BY tipo_factura, num_factura
HAVING COUNT(*) > 1;

-- Entradas línea: (cod_entrada, num_linea) no debe repetirse
SELECT cod_entrada, num_linea, COUNT(*) c
FROM gold.fact_entradas_linea
GROUP BY cod_entrada, num_linea
HAVING COUNT(*) > 1;
