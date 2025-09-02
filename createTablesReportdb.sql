USE ReportDB
GO 

create schema firds; 

CREATE TABLE firds.ReportInstrument (
    ISIN CHAR(12) NOT NULL,
    MIC CHAR(4) NOT NULL,
    [Name] NVARCHAR(MAX) NULL,
    CFICodeId CHAR(6) NULL,
    Issr CHAR(20) NULL,
    FrstTradDt DATETIME NULL,
    TermntnDt DATETIME NULL, 
    SourceTable VARCHAR(20) NOT NULL,  -- 'isindata', 'isinterm', 'isincancel'
);

CREATE NONCLUSTERED INDEX IX_ReportInstrument_ISIN_MIC
ON firds.ReportInstrument (ISIN, MIC);

