CREATE TABLE [firds].[DLTINS](
	[ISIN] [char](12) NULL,
	[Name] [nvarchar](max) NULL,
	[CFICode] [char](6) NULL,
	[Currency] [char](3) NULL,
	[CmmdtyDerivInd] [bit] NULL,
	[Issr] [char](20) NULL,
	[MIC] [char](4) NULL,
	[IssrReq] [bit] NULL,
	[AdmssnApprvlDtByIssr] [datetime2](7) NULL,
	[RegForAdmssnDt] [datetime2](7) NULL,
	[FrstTradDt] [datetime2](7) NULL,
	[TermntnDt] [datetime2](7) NULL, 
	[Record] varchar(256) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]



