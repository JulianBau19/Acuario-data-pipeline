/* ==========================================================
   Purpose: PK + UK (GOLD)
========================================================== */
SET NOCOUNT ON;
GO

/* =========================
   DIMENSIONS - PK / UK
========================= */

ALTER TABLE gold.dim_fecha
ADD CONSTRAINT PK_gold_dim_fecha
PRIMARY KEY CLUSTERED (fecha_key);
GO

ALTER TABLE gold.dim_almacenes
ADD CONSTRAINT PK_gold_dim_almacenes
PRIMARY KEY CLUSTERED (almacen_key);
GO

ALTER TABLE gold.dim_articulos
ADD CONSTRAINT PK_gold_dim_articulos
PRIMARY KEY CLUSTERED (articulo_key);
GO

ALTER TABLE gold.dim_clientes
ADD CONSTRAINT PK_gold_dim_clientes
PRIMARY KEY CLUSTERED (cliente_key);
GO

ALTER TABLE gold.dim_familias
ADD CONSTRAINT PK_gold_dim_familias
PRIMARY KEY CLUSTERED (familia_key);
GO

ALTER TABLE gold.dim_proveedores
ADD CONSTRAINT PK_gold_dim_proveedores
PRIMARY KEY CLUSTERED (proveedor_key);
GO

ALTER TABLE gold.dim_proveedores
ADD CONSTRAINT UQ_gold_dim_proveedores_cod_proveedor
UNIQUE NONCLUSTERED (cod_proveedor);
GO

/* =========================
   FACTS - PK / UK
========================= */

ALTER TABLE gold.fact_ajustes_stock
ADD CONSTRAINT PK_gold_fact_ajustes_stock
PRIMARY KEY CLUSTERED (articulo_key, fecha_key, motivo);
GO

ALTER TABLE gold.fact_entradas
ADD CONSTRAINT PK_gold_fact_entradas
PRIMARY KEY CLUSTERED (cod_entrada);
GO

ALTER TABLE gold.fact_entradas_linea
ADD CONSTRAINT PK_gold_fact_entradas_linea
PRIMARY KEY CLUSTERED (entrada_linea_key);
GO

ALTER TABLE gold.fact_entradas_linea
ADD CONSTRAINT UQ_gold_fact_entradas_linea_codentrada_numlinea
UNIQUE NONCLUSTERED (cod_entrada, num_linea);
GO

ALTER TABLE gold.fact_facturas
ADD CONSTRAINT PK_gold_fact_facturas
PRIMARY KEY CLUSTERED (factura_key);
GO

ALTER TABLE gold.fact_facturas
ADD CONSTRAINT UQ_gold_fact_facturas_tipo_num
UNIQUE NONCLUSTERED (tipo_factura, num_factura);
GO

ALTER TABLE gold.fact_facturas_linea
ADD CONSTRAINT PK_gold_fact_facturas_linea
PRIMARY KEY CLUSTERED (factura_linea_key);
GO

ALTER TABLE gold.fact_facturas_linea
ADD CONSTRAINT UQ_gold_fact_facturas_linea_factura_numlinea
UNIQUE NONCLUSTERED (factura_key, num_linea);
GO

ALTER TABLE gold.fact_listado_de_tarifas
ADD CONSTRAINT UQ_gold_fact_listado_de_tarifas_art_fecha
UNIQUE NONCLUSTERED (articulo_key, fecha_tarifa_key);
GO

ALTER TABLE gold.fact_stock_actual
ADD CONSTRAINT PK_gold_fact_stock_actual
PRIMARY KEY CLUSTERED (articulo_key);
GO
