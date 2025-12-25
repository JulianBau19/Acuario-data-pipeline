/* ==========================================================
   Purpose: FK (GOLD)
========================================================== */
SET NOCOUNT ON;
GO

/* =========================
   DIM (jerarquías)
========================= */

ALTER TABLE gold.dim_articulos
ADD CONSTRAINT FK_gold_dim_articulos_dim_familias
FOREIGN KEY (familia_key) REFERENCES gold.dim_familias (familia_key);
GO

ALTER TABLE gold.dim_articulos
ADD CONSTRAINT FK_gold_dim_articulos_dim_almacenes
FOREIGN KEY (almacen_key) REFERENCES gold.dim_almacenes (almacen_key);
GO

/* =========================
   FACTS
========================= */

-- fact_entradas
ALTER TABLE gold.fact_entradas
ADD CONSTRAINT FK_gold_fact_entradas_dim_proveedores
FOREIGN KEY (proveedor_key) REFERENCES gold.dim_proveedores (proveedor_key);
GO

ALTER TABLE gold.fact_entradas
ADD CONSTRAINT FK_gold_fact_entradas_dim_almacenes
FOREIGN KEY (almacen_key) REFERENCES gold.dim_almacenes (almacen_key);
GO

ALTER TABLE gold.fact_entradas
ADD CONSTRAINT FK_gold_fact_entradas_dim_fecha
FOREIGN KEY (fecha_key) REFERENCES gold.dim_fecha (fecha_key);
GO

-- fact_entradas_linea
ALTER TABLE gold.fact_entradas_linea
ADD CONSTRAINT FK_gold_fact_entradas_linea_fact_entradas
FOREIGN KEY (cod_entrada) REFERENCES gold.fact_entradas (cod_entrada);
GO

ALTER TABLE gold.fact_entradas_linea
ADD CONSTRAINT FK_gold_fact_entradas_linea_dim_articulos
FOREIGN KEY (articulo_key) REFERENCES gold.dim_articulos (articulo_key);
GO

ALTER TABLE gold.fact_entradas_linea
ADD CONSTRAINT FK_gold_fact_entradas_linea_dim_proveedores
FOREIGN KEY (proveedor_key) REFERENCES gold.dim_proveedores (proveedor_key);
GO

ALTER TABLE gold.fact_entradas_linea
ADD CONSTRAINT FK_gold_fact_entradas_linea_dim_almacenes
FOREIGN KEY (almacen_key) REFERENCES gold.dim_almacenes (almacen_key);
GO

ALTER TABLE gold.fact_entradas_linea
ADD CONSTRAINT FK_gold_fact_entradas_linea_dim_fecha
FOREIGN KEY (fecha_key) REFERENCES gold.dim_fecha (fecha_key);
GO

-- fact_facturas
ALTER TABLE gold.fact_facturas
ADD CONSTRAINT FK_gold_fact_facturas_dim_clientes
FOREIGN KEY (cliente_key) REFERENCES gold.dim_clientes (cliente_key);
GO

ALTER TABLE gold.fact_facturas
ADD CONSTRAINT FK_gold_fact_facturas_dim_fecha
FOREIGN KEY (fecha_factura_key) REFERENCES gold.dim_fecha (fecha_key);
GO

-- fact_facturas_linea
ALTER TABLE gold.fact_facturas_linea
ADD CONSTRAINT FK_gold_fact_facturas_linea_fact_facturas
FOREIGN KEY (factura_key) REFERENCES gold.fact_facturas (factura_key);
GO

ALTER TABLE gold.fact_facturas_linea
ADD CONSTRAINT FK_gold_fact_facturas_linea_dim_articulos
FOREIGN KEY (articulo_key) REFERENCES gold.dim_articulos (articulo_key);
GO

ALTER TABLE gold.fact_facturas_linea
ADD CONSTRAINT FK_gold_fact_facturas_linea_dim_fecha
FOREIGN KEY (fecha_factura_key) REFERENCES gold.dim_fecha (fecha_key);
GO

-- fact_listado_de_tarifas
ALTER TABLE gold.fact_listado_de_tarifas
ADD CONSTRAINT FK_gold_fact_listado_de_tarifas_dim_articulos
FOREIGN KEY (articulo_key) REFERENCES gold.dim_articulos (articulo_key);
GO

ALTER TABLE gold.fact_listado_de_tarifas
ADD CONSTRAINT FK_gold_fact_listado_de_tarifas_dim_fecha
FOREIGN KEY (fecha_tarifa_key) REFERENCES gold.dim_fecha (fecha_key);
GO

-- fact_ajustes_stock
ALTER TABLE gold.fact_ajustes_stock
ADD CONSTRAINT FK_gold_fact_ajustes_stock_dim_articulos
FOREIGN KEY (articulo_key) REFERENCES gold.dim_articulos (articulo_key);
GO

ALTER TABLE gold.fact_ajustes_stock
ADD CONSTRAINT FK_gold_fact_ajustes_stock_dim_fecha
FOREIGN KEY (fecha_key) REFERENCES gold.dim_fecha (fecha_key);
GO

-- fact_stock_actual
ALTER TABLE gold.fact_stock_actual
ADD CONSTRAINT FK_gold_fact_stock_actual_dim_articulos
FOREIGN KEY (articulo_key) REFERENCES gold.dim_articulos (articulo_key);
GO
