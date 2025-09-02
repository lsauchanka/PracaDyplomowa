# Repozytorium – Praca Dyplomowa

To repozytorium stanowi **suplement** do pracy dyplomowej.  

Repozytorium zawiera materiały pomocnicze oraz kod źródłowy wykorzystany w trakcie realizacji projektu:

## Zawartość
- **Skrypty T-SQL** – definicje tabel, procedur składowanych oraz widoków, używanych do budowy i utrzymania hurtowni danych w systemie **Microsoft SQL Server**:
1. [**createTablesFirdsdb.sql**](./createTablesFirdsdb.sql) – tworzenie tabel dla bazy głównej.  
2. [**createTablesImportdb.sql**](./createTablesImportdb.sql) – tworzenie tabel dla bazy importowej.  
3. [**createTablesReportdb.sql**](./createTablesReportdb.sql) – tworzenie tabel dla bazy raportowej.
4. [**createDLTINS.sql**](./createDLTINS.sql) – tworzenie tabeli DLTINS.  
5. [**createViews.sql**](./createViews.sql) – tworzenie widoków.
6. [**FULINSInsert.sql**](./FULINSInsert.sql) – ładowanie danych z plików FULINS do tabel importowych.
7. [**job_script_createto.sql**](./job_script_createTO.sql) – tworzenie jobu w SQL Server Agent do automatyzacji procesu.
8. [**DLTINS_proc.sql**](./DLTINS_proc.sql) – procedura do przetwarzania danych z plików DLTINS.
9. [**CheckDataQuality_proc.sql**](./CheckDataQuality_proc.sql) – procedura weryfikująca poprawność i spójność danych w hurtowni w jobie.   
10. [**RefreshReportingInstruments_proc.sql**](./RefreshReportingInstruments_proc.sql) – procedura odświeżania tabeli raportowej.  

- **Skrypty Python** – implementacja procesu **ETL** (Extract–Transform–Load), odpowiedzialnego za pobieranie, parsowanie i ładowanie danych do hurtowni:
1. [**filecheck.py**](./filecheck.py) – sprawdzanie dostępności plików źródłowych do pobrania.  
2. [**fulcan.py**](./fulcan.py) – obsługa plików typu FULCAN.  
3. [**fulins.py**](./fulins.py) – obsługa plików typu FULINS.  
4. [**dltins.py**](./dltins.py) – obsługa plików typu DLTINS.

- **Projekt SSRS (SQL Server Reporting Services)** [**ProjektSSRS.zip**](./ProjektSSRS.zip) – zestaw raportów stworzonych w środowisku **Visual Studio**

- **Backupy baz danych** - dane, które zostały przeprocesowane w projekcie oraz struktura baz danych znajdują sie pod linkiem: https://drive.google.com/drive/folders/1Bk15b6bAn-ooOQ670aWck34Njbjqh9LO?usp=sharing

## Cel repozytorium
Repozytorium ma charakter dokumentacyjny i dydaktyczny – jego celem jest pokazanie praktycznej implementacji rozwiązania opisanego w pracy dyplomowej.  
Dzięki kodom i projektowi raportów możliwe jest odtworzenie procesu tworzenia hurtowni danych oraz analizy instrumentów finansowych w środowisku **Microsoft SQL Server** i **SSRS**.



