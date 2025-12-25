
CREATE TABLE [cln].[listado_de_tarifas](
	[COD_ARTICULO] [varchar](max) NULL,
	[DESCRIPCION] [varchar](max) NULL,
	[PRECIO_DE_VENTA] [float] NULL,
	[fecha_carga_cln] [datetime2](7) NOT NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

