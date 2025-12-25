
CREATE TABLE [cln].[entradas](
	[cod_entrada] [varchar](max) NULL,
	[fecha] [datetime2](7) NULL,
	[cod_proveedor] [varchar](max) NULL,
	[cod_almacen] [varchar](max) NULL,
	[nombre_proveedor] [varchar](max) NULL,
	[total] [float] NULL,
	[fecha_carga_cln] [datetime2](7) NOT NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

