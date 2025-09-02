### Skrypt do ściągniecia plików typu FULCAN ###

import requests
import simplejson
import pandas as pd
import os
import zipfile
import pyodbc
from lxml import etree
import time
from sqlalchemy import create_engine
# from datetime import date

string = f"https://api.data.fca.org.uk/fca_data_firds_files?q=((file_type:FULCAN)%20AND%20(publication_date:[2025-07-12%20TO%202025-07-12]))&from=0&size=100&pretty=true"

response_API = requests.get(string)

train = pd.DataFrame.from_dict(simplejson.loads(response_API.text), orient='index')
train.reset_index(level=0, inplace=True)

json_string = simplejson.dumps((train.iloc[3,1])["hits"])

json_table = pd.DataFrame(simplejson.loads(json_string))

df_merged = pd.concat([json_table, pd.json_normalize(json_table["_source"])], axis=1)

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
            print("File downloaded successfully.")
    else:
        print("Failed to download the file.")

    print("End: download file...")

    # Open .zip file
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        # Extract all the contents to a specified directory
        zip_ref.extractall('D:\\Matematyka\\Dyplom\\Firds')

    # Delete .zip file
    os.remove(file_path)
    print("Deleted .zip file")

    # Open and parse xml

    file_path = "D:\\Matematyka\\Dyplom\\Firds\\" + row['file_name']

    print("Open XML...")

    file_path_xml = file_path[:-3] + 'xml'

    tree = etree.parse(file_path_xml)
    root = tree.getroot()

    print(f'Parse XML... start: {time.strftime("%H:%M:%S")}')

    data = []
    for cxl_data in root.findall('.//{urn:iso:std:iso:20022:tech:xsd:auth.102.001.01}CxlData'):
        fin_instrm_id = cxl_data.find('.//{urn:iso:std:iso:20022:tech:xsd:auth.102.001.01}Id').text
        tradg_vn_id = cxl_data.find('.//{urn:iso:std:iso:20022:tech:xsd:auth.102.001.01}TradgVnRltdAttrbts/{urn:iso:std:iso:20022:tech:xsd:auth.102.001.01}Id').text
        data.append({'ISIN': fin_instrm_id, 'MIC': tradg_vn_id})

    df = pd.DataFrame(data)
    print(f'Parse XML... end: {time.strftime("%H:%M:%S")}')

    os.remove(file_path_xml)

    print(df.iloc[0])

    print(f"Liczba rekordów: {df.shape[0]}")
    print(f"Liczba kolumn: {df.shape[1]}")

    # import do SQL Server

    print("Połączenie do serwera")

    username = ''
    password = ''
    server = 'LAPTOP-PH52I9TM'
    database = 'FirdsDB'

    engine = create_engine(
        f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server;Trusted_Connection=yes"
    )

    print("Połączenie się powiodło")

    print("Start import")

    df.to_sql(
        name="ISINCancel",
        con=engine,
        schema="firds",
        if_exists='append',
        index=False,
        chunksize=161
    )

    print("End import")
