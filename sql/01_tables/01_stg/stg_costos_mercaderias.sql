
CREATE TABLE [stg].[costos_mercaderias](
	[N° FACTURA] [varchar](max) NULL,
	[PROVEEDOR] [varchar](max) NULL,
	[CUOTIFICADA] [varchar](max) NULL,
	[FECHA DE COMPRA] [varchar](max) NULL,
	[VENCIMIENTO] [datetime] NULL,
	[MONTO TOTAL] [float] NULL,
	[ESTADO DE PAGO] [varchar](max) NULL,
	[OBSERVACIONES] [varchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
