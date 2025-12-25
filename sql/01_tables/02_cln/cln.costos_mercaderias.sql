

CREATE TABLE [cln].[costos_mercaderias](
	[N° FACTURA] [varchar](max) NULL,
	[PROVEEDOR] [varchar](max) NULL,
	[CUOTIFICADA] [varchar](max) NULL,
	[FECHA DE COMPRA] [varchar](max) NULL,
	[VENCIMIENTO] [datetime2](7) NULL,
	[MONTO TOTAL] [float] NULL,
	[ESTADO DE PAGO] [varchar](max) NULL,
	[OBSERVACIONES] [varchar](max) NULL,
	[fecha_carga_cln] [datetime2](7) NOT NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

