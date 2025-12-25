

CREATE TABLE [cln].[facturas_linea](
	[tipo_factura] [bigint] NULL,
	[num_factura] [varchar](max) NULL,
	[num_linea] [bigint] NULL,
	[cod_articulo] [varchar](max) NULL,
	[descripcion] [varchar](max) NULL,
	[cantidad] [bigint] NULL,
	[precio_unitario] [float] NULL,
	[total_linea] [float] NULL,
	[iva_linea] [bigint] NULL,
	[total_linea_con_iva] [float] NULL,
	[fecha_carga_cln] [datetime2](7) NOT NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

