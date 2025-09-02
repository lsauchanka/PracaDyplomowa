use FirdsDB;

create schema firds;

-- CFICode
CREATE TABLE firds.CFICode (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    CFICode CHAR(6) NOT NULL
);

-- Currency
CREATE TABLE firds.Currency (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    CurrencyCode CHAR(3) NOT NULL
);

-- MIC 
CREATE TABLE firds.MIC (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    MIC CHAR(4) NOT NULL
);

-- ISIN 
CREATE TABLE firds.ISIN (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    ISIN CHAR(12) NOT NULL,
    [Name] NVARCHAR(MAX) NOT NULL,
    Issr CHAR(20) NOT NULL
);

-- ISINData
CREATE TABLE firds.ISINData (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    IsinId INT NOT NULL,
    CFICodeId INT NOT NULL,
    MicId INT NOT NULL,
    CurrencyId INT NOT NULL,
    CmmdtyDerivInd BIT NOT NULL,
    IssrReq BIT NOT NULL,
    AdmsnApprvlDtByIssr DATETIME NULL,
    ReqForAdmsnDt DATETIME NULL,
    FrstTradDt DATETIME NULL,
    TermntnDt DATETIME NULL
);

-- Klucze 
ALTER TABLE firds.ISINData
ADD CONSTRAINT FK_ISINData_ISIN
FOREIGN KEY (IsinId) REFERENCES firds.ISIN(Id);

ALTER TABLE firds.ISINData
ADD CONSTRAINT FK_ISINData_CFICode
FOREIGN KEY (CFICodeId) REFERENCES firds.CFICode(Id);

ALTER TABLE firds.ISINData
ADD CONSTRAINT FK_ISINData_MIC
FOREIGN KEY (MicId) REFERENCES firds.MIC(Id);

ALTER TABLE firds.ISINData
ADD CONSTRAINT FK_ISINData_Currency
FOREIGN KEY (CurrencyId) REFERENCES firds.Currency(Id);

-- ISINTermntd
CREATE TABLE firds.ISINTermntd (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    IsinId INT NOT NULL,
    CFICodeId INT NOT NULL,
    MicId INT NOT NULL,
    CurrencyId INT NOT NULL,
    CmmdtyDerivInd BIT NOT NULL,
    IssrReq BIT NOT NULL,
    AdmsnApprvlDtByIssr DATETIME NULL,
    ReqForAdmsnDt DATETIME NULL,
    FrstTradDt DATETIME NULL,
    TermntnDt DATETIME NULL
);

-- Klucze obce do slownikow
ALTER TABLE firds.ISINTermntd
ADD CONSTRAINT FK_ISINTermntd_ISIN
FOREIGN KEY (IsinId) REFERENCES firds.ISIN(Id);

ALTER TABLE firds.ISINTermntd
ADD CONSTRAINT FK_ISINTermntd_CFICode
FOREIGN KEY (CFICodeId) REFERENCES firds.CFICode(Id);

ALTER TABLE firds.ISINTermntd
ADD CONSTRAINT FK_ISINTermntd_MIC
FOREIGN KEY (MicId) REFERENCES firds.MIC(Id);

ALTER TABLE firds.ISINTermntd
ADD CONSTRAINT FK_ISINTermntd_Currency
FOREIGN KEY (CurrencyId) REFERENCES firds.Currency(Id);


CREATE TABLE firds.ISINCancel (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    ISIN CHAR(12) NOT NULL,
    MIC CHAR(4) NOT NULL
);
