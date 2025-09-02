# Repozytorium – Praca Dyplomowa

To repozytorium stanowi **suplement** do pracy dyplomowej.  

Repozytorium zawiera materiały pomocnicze oraz kod źródłowy wykorzystany w trakcie realizacji projektu:

## Zawartość
- **Skrypty T-SQL** – definicje tabel, procedur składowanych oraz widoków, używanych do budowy i utrzymania hurtowni danych w systemie **Microsoft SQL Server**:
1. [**CheckDataQuality_proc.sql**](./CheckDataQuality_proc.sql) – procedura weryfikująca poprawność i spójność danych w hurtowni.  
2. [**DLTINS.sql**](./DLTINS.sql) – przykładowe dane wejściowe w formacie DLTINS.  
3. [**DLTINS_proc.sql**](./DLTINS_proc.sql) – procedura do przetwarzania danych z plików DLTINS.  
4. [**FULINSInsert.sql**](./FULINSInsert.sql) – skrypt ładowania danych z plików FULINS do tabel importowych.  
5. [**RefreshReportingInstruments_proc.sql**](./RefreshReportingInstruments_proc.sql) – procedura odświeżania tabeli raportowej `ReportInstrumentView`.  
6. [**createDLTINS.sql**](./createDLTINS.sql) – skrypt tworzący tabelę dla danych DLTINS.  
7. [**createTablesFirdsdb.sql**](./createTablesFirdsdb.sql) – definicje tabel głównej bazy FIRDS.  
8. [**createTablesImportdb.sql**](./createTablesImportdb.sql) – definicje tabel dla bazy importowej.  
9. [**createTablesReportdb.sql**](./createTablesReportdb.sql) – definicje tabel raportowych.  
10. [**createViews.sql**](./createViews.sql) – widoki ułatwiające raportowanie i łączenie danych.  
11. [**job_script_createTO.sql**](./job_script_createTO.sql) – skrypt tworzący zadanie (job) w SQL Server Agent do automatyzacji procesu.

- **Skrypty Python** – implementacja procesu **ETL** (Extract–Transform–Load), odpowiedzialnego za pobieranie, parsowanie i ładowanie danych do hurtowni z plików udostępnianych przez system **FCA FIRDS**.  
- **Projekt SSRS (SQL Server Reporting Services)** – zestaw raportów analitycznych stworzonych w środowisku **Visual Studio**

## Cel repozytorium
Repozytorium ma charakter dokumentacyjny i dydaktyczny – jego celem jest pokazanie praktycznej implementacji rozwiązania opisanego w pracy dyplomowej.  
Dzięki kodom i projektowi raportów możliwe jest odtworzenie procesu tworzenia hurtowni danych oraz analizy instrumentów finansowych w środowisku **Microsoft SQL Server** i **SSRS**.



