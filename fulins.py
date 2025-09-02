### Skrypt do ściągniecia plików typu FULINS ###

import requests
import simplejson
import pandas as pd
import os
import pyodbc
import zipfile
from lxml import etree
import time
from sqlalchemy import create_engine

string = "https://api.data.fca.org.uk/fca_data_firds_files?q=((file_type:FULINS)%20AND%20(publication_date:[2025-07-12%20TO%202025-07-12]))&from=0&size=100&pretty=true"

response_API = requests.get(string)

train = pd.DataFrame.from_dict(simplejson.loads(response_API.text), orient='index')
train.reset_index(level=0, inplace=True)

json_string = simplejson.dumps((train.iloc[3,1])["hits"])
json_table = pd.DataFrame(simplejson.loads(json_string))

df_merged = pd.concat([json_table, pd.json_normalize(json_table["_source"])], axis=1)

print(df_merged)

for index, row in df_merged.iterrows():
    print(f"File number: {index + 1}")
    print(f"Name: {row['file_name']}")
    print("Start: download file...")

    file_url = row['download_link']

    # Download zip file
    file_path = "D:\\Matematyka\\Dyplom\\Firds\\" + row['file_name']

    response = requests.get(file_url)

    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)

    print("End: download file...")

    # Open .zip file
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall("D:\\Matematyka\\Dyplom\\Firds")

    print("Opened .zip file")

    # Delete .zip file
    os.remove(file_path)

    print("Deleted .zip file")

    # Open and parse xml
    file_path = "D:\\Matematyka\\Dyplom\\Firds\\" + row['file_name']

    print("Opening XML...")

    file_path_xml = file_path[:-3] + 'xml'

    tree = etree.parse(file_path_xml)
    root = tree.getroot()

    print("Opened XML...")

    namespace = 'urn:iso:std:iso:20022:tech:xsd:auth.017.001.02'

    print(f"Parsing XML... start: {time.strftime('%H:%M:%S')}")

    data = []
    for ref_data in root.findall(f'.//{{{namespace}}}RefData'):
        fin_instrm_gnl_attrbts = ref_data.find(f'.//{{{namespace}}}FinInstrmGnlAttrbts')
        issr = ref_data.find(f'.//{{{namespace}}}Issr')
        tradg_vn_rltd_attrbts = ref_data.find(f'.//{{{namespace}}}TradgVnRltdAttrbts')

        data.append({
            'ISIN': fin_instrm_gnl_attrbts.find(f'.//{{{namespace}}}Id').text,
            'Name': fin_instrm_gnl_attrbts.find(f'.//{{{namespace}}}ShrtNm').text,
            'CFICode': fin_instrm_gnl_attrbts.find(f'.//{{{namespace}}}ClssfctnTp').text,
            'Currency': fin_instrm_gnl_attrbts.find(f'.//{{{namespace}}}NtnlCcy').text,
            'CmmdtyDerivInd': fin_instrm_gnl_attrbts.find(f'.//{{{namespace}}}CmmdtyDerivInd').text,
            'Issr': issr.text,
            'MIC': tradg_vn_rltd_attrbts.find(f'.//{{{namespace}}}Id').text,
            'IssrReq': tradg_vn_rltd_attrbts.find(f'.//{{{namespace}}}IssrReq').text,
            'AdmssnApprvlDtByIssr': tradg_vn_rltd_attrbts.find(
                f'.//{{{namespace}}}AdmsnApprvlDtByIssr').text if tradg_vn_rltd_attrbts.find(
                f'.//{{{namespace}}}AdmsnApprvlDtByIssr') is not None else None,
            'RegForAdmssnDt': tradg_vn_rltd_attrbts.find(
                f'.//{{{namespace}}}ReqForAdmsnDt').text if tradg_vn_rltd_attrbts.find(
                f'.//{{{namespace}}}ReqForAdmsnDt') is not None else None,
            'FrstTradDt': tradg_vn_rltd_attrbts.find(
                f'.//{{{namespace}}}FrstTradDt').text if tradg_vn_rltd_attrbts.find(
                f'.//{{{namespace}}}FrstTradDt') is not None else None,
            'TermntnDt': tradg_vn_rltd_attrbts.find(
                f'.//{{{namespace}}}TermntnDt').text if tradg_vn_rltd_attrbts.find(
                f'.//{{{namespace}}}TermntnDt') is not None else None,
        })

    df = pd.DataFrame(data)

    os.remove(file_path_xml)

    print("Deleted XML...")
    print("Converting data...")

    for index, row in df.iterrows():
        if row['CmmdtyDerivInd'] == 'false':
            row['CmmdtyDerivInd'] = 0
        elif row['CmmdtyDerivInd'] == 'true':
            row['CmmdtyDerivInd'] = 1

        if row['IssrReq'] == 'false':
            row['IssrReq'] = 0
        elif row['IssrReq'] == 'true':
            row['IssrReq'] = 1

    print(df.iloc[0])

    print(f"Liczba rekordów: {df.shape[0]}")
    print(f"Liczba kolumn: {df.shape[1]}")

    # import do SQL Server

    print("Połączenie do serwera")

    username = ''
    password = ''
    server = 'LAPTOP-PH52I9TM'
    database = 'ImportDB'

    engine = create_engine(
        f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server;Trusted_Connection=yes"
    )

    print("Połączenie się powiodło")

    print("Start import")

    df.to_sql(
        name="FULINS",
        con=engine,
        schema="firds",
        if_exists='append',
        index=False,
        chunksize=161
    )

    print("End import")

