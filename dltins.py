import requests
import simplejson
import pandas as pd
import os
import zipfile
from lxml import etree
from datetime import date
from sqlalchemy import create_engine
import sys
import pyodbc

try:
    today = str(date.today())

    string = f"https://api.data.fca.org.uk/fca_data_firds_files?q=((file_type:DLTINS)%20AND%20(publication_date:[{today}%20TO%20{today}]))&from=0&size=100&pretty=true"

    response_API = requests.get(string)

    train = pd.DataFrame.from_dict(simplejson.loads(response_API.text), orient='index')
    train.reset_index(level=0, inplace=True)

    json_string = simplejson.dumps((train.iloc[3,1])["hits"])
    json_table = pd.DataFrame(simplejson.loads(json_string))

    df_merged = pd.concat([json_table, pd.json_normalize(json_table["_source"])], axis=1)

    for index, row in df_merged.iterrows():

        file_url = row['download_link']

        # Download zip file
        file_path = "D:\\Matematyka\\Dyplom\\Firds\\" + row['file_name']

        response = requests.get(file_url)

        if response.status_code == 200:
            with open(file_path, "wb") as file:
                file.write(response.content)

        # Open .zip file
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall("D:\\Matematyka\\Dyplom\\Firds")

        # Delete .zip file
        os.remove(file_path)

        # Open and parse xml
        file_path = "D:\\Matematyka\\Dyplom\\Firds\\" + row['file_name']

        file_path_xml = file_path[:-3] + 'xml'

        tree = etree.parse(file_path_xml)
        root = tree.getroot()

        schema = '{urn:iso:std:iso:20022:tech:xsd:auth.036.001.03}'

        data = []

        for fin_instrm in root.findall(f'.//{schema}FinInstrmRptgRefDataDltaRpt/{schema}FinInstrm'):
            record_type1 = fin_instrm.find(f'.//{schema}NewRcrd').text if fin_instrm.find(f'.//{schema}NewRcrd') is not None else None
            record_type2 = fin_instrm.find(f'.//{schema}ModfdRcrd').text if fin_instrm.find(f'.//{schema}ModfdRcrd') is not None else None
            record_type3 = fin_instrm.find(f'.//{schema}CancRcrd').text if fin_instrm.find(f'.//{schema}CancRcrd') is not None else None
            record_type4 = fin_instrm.find(f'.//{schema}TermntdRcrd').text if fin_instrm.find(f'.//{schema}TermntdRcrd') is not None else None

            fin_instrm_id = fin_instrm.find(f'.//{schema}Id').text
            #full_name = fin_instrm.find(f'.//{schema}FullNm').text if fin_instrm.find(f'.//{schema}FullNm') is not None else None
            short_name = fin_instrm.find(f'.//{schema}ShrtNm').text if fin_instrm.find(f'.//{schema}ShrtNm') is not None else None
            classification_type = fin_instrm.find(f'.//{schema}ClssfctnTp').text if fin_instrm.find(f'.//{schema}ClssfctnTp') is not None else None
            national_currency = fin_instrm.find(f'.//{schema}NtnlCcy').text if fin_instrm.find(f'.//{schema}NtnlCcy') is not None else None
            cmmdty_deriv_ind = fin_instrm.find(f'.//{schema}CmmdtyDerivInd').text if fin_instrm.find(f'.//{schema}CmmdtyDerivInd') is not None else None
            issr = fin_instrm.find(f'.//{schema}Issr').text if fin_instrm.find(f'.//{schema}Issr') is not None else None

            tradg_vn_rltd_attrbts_id = fin_instrm.find(f'.//{schema}TradgVnRltdAttrbts/{schema}Id').text if fin_instrm.find(f'.//{schema}TradgVnRltdAttrbts/{schema}Id') is not None else None
            issr_req = fin_instrm.find(f'.//{schema}TradgVnRltdAttrbts/{schema}IssrReq').text if fin_instrm.find(f'.//{schema}TradgVnRltdAttrbts/{schema}IssrReq') is not None else None
            admsn_apprvl_dt_by_issr = fin_instrm.find(f'.//{schema}TradgVnRltdAttrbts/{schema}FrstTradDt').text if fin_instrm.find(f'.//{schema}TradgVnRltdAttrbts/{schema}AdmssnApprvlDtByIssr') is not None else None
            frst_trad_dt = fin_instrm.find(f'.//{schema}TradgVnRltdAttrbts/{schema}FrstTradDt').text if fin_instrm.find(f'.//{schema}TradgVnRltdAttrbts/{schema}FrstTradDt') is not None else None
            ReqForAdmsnDt = fin_instrm.find(f'.//{schema}TradgVnRltdAttrbts/{schema}ReqForAdmsnDt').text if fin_instrm.find(f'.//{schema}TradgVnRltdAttrbts/{schema}ReqForAdmsnDt') is not None else None
            termntn_dt = fin_instrm.find(f'.//{schema}TradgVnRltdAttrbts/{schema}TermntDt').text if fin_instrm.find(f'.//{schema}TradgVnRltdAttrbts/{schema}TermntDt') is not None else None

            record_type = None
            if record_type1 is not None:
                record_type = "NewRcrd"
            elif record_type2 is not None:
                record_type = "ModfdRcrd"
            elif record_type3 is not None:
                record_type = "CancRcrd"
            elif record_type4 is not None:
                record_type = "TermntdRcrd"

            data.append({
                'ISIN': fin_instrm_id,
                #'FullNm': full_name,
                'Name': short_name,
                'CFICode': classification_type,
                'Currency': national_currency,
                'CmmdtyDerivInd': cmmdty_deriv_ind,
                'Issr': issr,
                'MIC': tradg_vn_rltd_attrbts_id,
                'IssrReq': issr_req,
                'AdmssnApprvlDtByIssr': admsn_apprvl_dt_by_issr,
                'ReqForAdmssnDt': ReqForAdmsnDt,
                'FrstTradDt': frst_trad_dt,
                'TermntnDt': termntn_dt,
                # dod kolumny ...
                'Record': record_type
            })

        df = pd.DataFrame(data)

        os.remove(file_path_xml)


        for index, row in df.iterrows():
            if row['CmmdtyDerivInd'] == 'false':
                row['CmmdtyDerivInd'] = 0
            elif row['CmmdtyDerivInd'] == 'true':
                row['CmmdtyDerivInd'] = 1

            if row['IssrReq'] == 'false':
                row['IssrReq'] = 0
            elif row['IssrReq'] == 'true':
                row['IssrReq'] = 1

        # import do SQL Server

        username = ''  # zostaw puste dla Windows Authentication
        password = ''  # zostaw puste dla Windows Authentication
        server = 'LAPTOP-PH52I9TM'
        database = 'ImportDB'

        engine = create_engine(
            f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server;Trusted_Connection=yes"
        )


        df.to_sql(
            name="DLTINS",
            con=engine,
            schema="firds",
            if_exists='append',
            index=False,
            chunksize=161
        )

except Exception as e:

    print(f"Error: {e}")
    sys.exit(1)