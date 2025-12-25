
CREATE TABLE [cln].[articulos](
	[cod_articulo] [varchar](max) NULL,
	[familia] [varchar](max) NULL,
	[nombre] [varchar](max) NULL,
	[costo] [float] NULL,
	[fecha_alta] [datetime2](7) NULL,
	[almacen] [varchar](max) NULL,
	[fecha_carga_cln] [datetime2](7) NOT NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

