
CREATE TABLE [cln].[tarifas](
	[CODTAR] [bigint] NULL,
	[DESTAR] [varchar](max) NULL,
	[MARTAR] [float] NULL,
	[IVATAR] [bigint] NULL,
	[DIITAR] [bigint] NULL,
	[fecha_carga_cln] [datetime2](7) NOT NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

