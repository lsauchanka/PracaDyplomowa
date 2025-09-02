USE FirdsDB
GO

-- Dictionaries 
-- CFICode
INSERT firds.CFICode (CFICode)
SELECT DISTINCT a.CFICode
FROM ImportDB.firds.DLTINS a
LEFT JOIN firds.CFICode b
ON a.CFICode = b.CFICode
WHERE b.CFICode IS NULL AND Record <> 'CancRcrd'

-- Currency
INSERT firds.Currency (CurrencyCode)
SELECT DISTINCT a.Currency
FROM ImportDB.firds.DLTINS a
LEFT JOIN firds.Currency b
ON a.Currency = b.CurrencyCode
WHERE b.CurrencyCode IS NULL AND a.Record <> 'CancRcrd';

-- MIC
INSERT firds.MIC (MIC)
SELECT DISTINCT a.MIC
FROM ImportDB.firds.DLTINS a
LEFT JOIN firds.MIC b
ON a.MIC = b.MIC
WHERE b.MIC IS NULL AND a.Record <> 'CancRcrd';

-- ISIN
INSERT firds.ISIN (ISIN, [Name], Issr)
SELECT DISTINCT a.ISIN, a.[Name], a.Issr
FROM ImportDB.firds.DLTINS a
LEFT JOIN firds.ISIN b
ON a.ISIN = b.ISIN 
WHERE b.ISIN IS NULL AND a.Record <> 'CancRcrd';

UPDATE b
SET [Name] = a.[Name], Issr = a.Issr 
FROM ImportDB.firds.DLTINS a
JOIN firds.ISIN b
ON a.ISIN = b.ISIN and a.Issr != b.Issr
WHERE Record = 'ModfdRcrd'


-- Obsluga rekordow NewRcrd, ModfdRcrd
INSERT firds.ISINData
SELECT DISTINCT
    i.Id,
    c.Id,
    m.Id,
    cur.Id,
    d.CmmdtyDerivInd,
    d.IssrReq,
    d.AdmssnApprvlDtByIssr,
    d.ReqForAdmssnDt,
    d.FrstTradDt,
    d.TermntnDt
FROM ImportDB.firds.DLTINS d
JOIN firds.ISIN i
ON d.ISIN = i.ISIN
JOIN firds.CFICode c
ON d.CFICode = c.CFICode
JOIN firds.Currency cur
ON d.Currency = cur.CurrencyCode
JOIN firds.MIC m
ON d.MIC = m.MIC
LEFT JOIN firds.ISINData existing
ON existing.IsinId = i.Id AND existing.MicId = m.Id
WHERE existing.Id IS NULL AND d.Record IN ('NewRcrd', 'ModfdRcrd');

-- ! IS DISTINCT FROM dzia?a od sql server 2022
UPDATE target
SET
    CFICodeId = c.Id,
    CurrencyId = cur.Id,
    CmmdtyDerivInd = d.CmmdtyDerivInd,
    IssrReq = d.IssrReq,
    AdmssnApprvlDtByIssr = d.AdmssnApprvlDtByIssr,
    ReqForAdmssnDt = d.ReqForAdmssnDt,
    FrstTradDt = d.FrstTradDt,
    TermntnDt = d.TermntnDt
FROM firds.ISINData target
JOIN firds.ISIN i
ON i.Id = target.IsinId
JOIN firds.MIC m
ON m.Id = target.MicId
JOIN ImportDB.firds.DLTINS d
ON d.ISIN = i.ISIN AND d.MIC = m.MIC
JOIN firds.CFICode c
ON d.CFICode = c.CFICode
JOIN firds.Currency cur
ON d.Currency = cur.CurrencyCode
WHERE d.Record = 'ModfdRcrd'
  AND (
      target.CFICodeId IS DISTINCT FROM c.Id OR
      target.CurrencyId IS DISTINCT FROM cur.Id OR
      target.CmmdtyDerivInd IS DISTINCT FROM d.CmmdtyDerivInd OR
      target.IssrReq IS DISTINCT FROM d.IssrReq OR
      target.AdmssnApprvlDtByIssr IS DISTINCT FROM d.AdmssnApprvlDtByIssr OR
      target.ReqForAdmssnDt IS DISTINCT FROM d.ReqForAdmssnDt OR
      target.FrstTradDt IS DISTINCT FROM d.FrstTradDt OR
      target.TermntnDt IS DISTINCT FROM d.TermntnDt
  );


-- Obsluga rekordow ISINTermntd
INSERT firds.ISINTermntd
SELECT DISTINCT
    i.Id,
    c.Id,
    m.Id,
    cur.Id,
    d.CmmdtyDerivInd,
    d.IssrReq,
    d.AdmssnApprvlDtByIssr,
    d.ReqForAdmssnDt,
    d.FrstTradDt,
    d.TermntnDt
FROM ImportDB.firds.DLTINS d
JOIN firds.ISIN i
ON d.ISIN = i.ISIN
JOIN firds.CFICode c
ON d.CFICode = c.CFICode
JOIN firds.Currency cur
ON d.Currency = cur.CurrencyCode
JOIN firds.MIC m
ON d.MIC = m.MIC
LEFT JOIN firds.ISINTermntd existing
ON existing.IsinId = i.Id AND existing.MicId = m.Id
WHERE existing.Id IS NULL AND d.Record = 'TermntdRcrd';

DELETE id
FROM firds.ISINData id
JOIN firds.ISINTermntd it
ON id.IsinId = it.IsinId AND id.MicId = it.MicId


-- Obsluga rekordow CancRcrd
INSERT firds.ISINCancel 
SELECT DISTINCT d.ISIN, d.MIC
FROM ImportDB.firds.DLTINS d
LEFT JOIN firds.ISINCancel c
ON c.ISIN = d.ISIN AND c.MIC = d.MIC
WHERE d.Record = 'CancRcrd' AND c.ISIN IS NULL;

DELETE id
FROM firds.ISINData id
JOIN firds.ISIN isin ON id.IsinId = isin.Id
JOIN firds.MIC mic ON id.MicId = mic.Id
JOIN firds.ISINCancel c ON c.ISIN = isin.ISIN AND c.MIC = mic.MIC;

DELETE it
FROM firds.ISINTermntd it
JOIN firds.ISIN isin ON it.IsinId = isin.Id
JOIN firds.MIC mic ON it.MicId = mic.Id
JOIN firds.ISINCancel c ON c.ISIN = isin.ISIN AND c.MIC = mic.MIC;
