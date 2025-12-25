CREATE TABLE [stg].[entradas_linea](
	[cod_entrada] [bigint] NULL,
	[num_linea] [bigint] NULL,
	[cod_articulo] [varchar](max) NULL,
	[descripcion] [varchar](max) NULL,
	[cantidad] [bigint] NULL,
	[precio_unitario] [float] NULL,
	[total_linea] [float] NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

