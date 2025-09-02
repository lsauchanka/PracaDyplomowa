USE ImportDB;

CREATE SCHEMA firds;

CREATE TABLE firds.FULINS (
    ISIN CHAR(12),
    [Name] NVARCHAR(MAX) null,
    CFICode CHAR(6) null,
    Currency CHAR(3) null, 
    CmmdtyDerivInd BIT null,
    Issr CHAR(20) null,
    MIC CHAR(4),
    IssrReq BIT null,
    AdmssnApprvlDtByIssr DATETIME2(7) null,
    RegForAdmssnDt DATETIME2(7) null,
    FrstTradDt DATETIME2(7) null,
    TermntnDt DATETIME2(7) null
);
