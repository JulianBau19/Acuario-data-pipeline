CREATE TABLE [stg].[entradas](
	[cod_entrada] [varchar](max) NULL,
	[fecha] [datetime] NULL,
	[cod_proveedor] [varchar](max) NULL,
	[cod_almacen] [varchar](max) NULL,
	[nombre_proveedor] [varchar](max) NULL,
	[total] [float] NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
