CREATE TABLE [stg].[articulos](
	[cod_articulo] [varchar](max) NULL,
	[familia] [varchar](max) NULL,
	[nombre] [varchar](max) NULL,
	[costo] [float] NULL,
	[fecha_alta] [datetime] NULL,
	[almacen] [varchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
