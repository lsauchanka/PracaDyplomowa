USE FirdsDB
GO

CREATE VIEW firds.v_ISINData
AS
SELECT DISTINCT
    id.Id,
    i.ISIN,
    i.[Name],
    i.Issr,
    ct.CFICode,
    m.MIC,
    c.CurrencyCode AS Currency,
    id.CmmdtyDerivInd,
    id.IssrReq,
    id.AdmssnApprvlDtByIssr,
    id.ReqForAdmssnDt,
    id.FrstTradDt,
    id.TermntnDt
FROM firds.ISINData id
INNER JOIN firds.ISIN i
ON id.IsinId = i.Id
INNER JOIN firds.CFICode ct
ON id.CFICodeId = ct.Id
INNER JOIN firds.MIC m
ON id.MicId = m.Id
INNER JOIN firds.Currency c
ON id.CurrencyId = c.Id; 


CREATE VIEW firds.v_ISINTermntd
AS
SELECT DISTINCT
    id.Id,
    i.ISIN,
    i.[Name],
    i.Issr,
    ct.CFICode,
    m.MIC,
    c.CurrencyCode AS Currency,
    id.CmmdtyDerivInd,
    id.IssrReq,
    id.AdmssnApprvlDtByIssr,
    id.ReqForAdmssnDt,
    id.FrstTradDt,
    id.TermntnDt
FROM firds.ISINTermntd id
INNER JOIN firds.ISIN i
ON id.IsinId = i.Id
INNER JOIN firds.CFICode ct
ON id.CFICodeId = ct.Id
INNER JOIN firds.MIC m
ON id.MicId = m.Id
INNER JOIN firds.Currency c
ON id.CurrencyId = c.Id


