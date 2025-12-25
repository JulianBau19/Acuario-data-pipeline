
CREATE TABLE [cln].[stock](
	[cod_articulo] [varchar](max) NULL,
	[stock_actual] [float] NULL,
	[fecha_carga_cln] [datetime2](7) NOT NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

