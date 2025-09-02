use FirdsDB; 

-- CFICode
INSERT firds.CFICode (CFICode)
SELECT DISTINCT
    CFICode
FROM ImportDB.firds.FULINS
WHERE CFICode IS NOT NULL;


-- Currency
INSERT firds.Currency (CurrencyCode)
SELECT DISTINCT
    Currency
FROM ImportDB.firds.FULINS
WHERE Currency IS NOT NULL;


-- MIC
INSERT firds.MIC (MIC)
SELECT DISTINCT
    MIC
FROM ImportDB.firds.FULINS
WHERE MIC IS NOT NULL;


-- ISIN
INSERT INTO firds.ISIN (ISIN, Name, Issr)
SELECT DISTINCT
    ISIN,
    [Name],
    Issr
FROM ImportDB.firds.FULINS
WHERE ISIN IS NOT NULL;


-- ISINData
INSERT INTO firds.ISINData (
    IsinId,
    CFICodeId,
    MicId,
    CurrencyId,
    CmmdtyDerivInd,
    IssrReq,
    AdmsnApprvlDtByIssr,
    ReqForAdmsnDt,
    FrstTradDt,
    TermntnDt
)
SELECT
    i.Id,
    c.Id,
    m.Id,
    cur.Id,
    f.CmmdtyDerivInd,
    f.IssrReq,
    f.AdmssnApprvlDtByIssr,
    f.RegForAdmssnDt,
    f.FrstTradDt,
    f.TermntnDt
FROM ImportDB.firds.FULINS f
JOIN firds.ISIN i
    ON f.ISIN = i.ISIN AND f.Issr = i.Issr and f.[Name] = i.[Name]
JOIN firds.CFICode c
    ON f.CFICode = c.CFICode
JOIN firds.Currency cur
    ON f.Currency = cur.CurrencyCode
JOIN firds.MIC m
    ON f.MIC = m.MIC;

