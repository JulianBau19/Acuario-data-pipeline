
CREATE TABLE [cln].[facturas](
	[tipo_factura] [bigint] NULL,
	[num_factura] [varchar](max) NULL,
	[fecha] [datetime2](7) NULL,
	[cod_cliente] [varchar](max) NULL,
	[nombre_cliente] [varchar](max) NULL,
	[total_base] [float] NULL,
	[total_iva] [float] NULL,
	[total_factura] [float] NULL,
	[fecha_carga_cln] [datetime2](7) NOT NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

