CREATE TABLE [stg].[facturas_linea](
	[tipo_linea] [bigint] NULL,
	[num_factura] [varchar](max) NULL,
	[num_linea] [bigint] NULL,
	[cod_articulo] [varchar](max) NULL,
	[descripcion] [varchar](max) NULL,
	[cantidad] [bigint] NULL,
	[precio_unitario] [float] NULL,
	[total_linea] [float] NULL,
	[iva_linea] [bigint] NULL,
	[total_linea_con_iva] [float] NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
