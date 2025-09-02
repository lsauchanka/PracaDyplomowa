### Skrypt do sprawdzenia czy występuje plik/pliki do pobrania ###

import requests
import pandas as pd
from datetime import date
import sys


try:
    today = str(date.today())
    string = f"https://api.data.fca.org.uk/fca_data_firds_files?q=((file_type:DLTINS)%20AND%20(publication_date:[{today}%20TO%20{today}]))&from=0&size=100&pretty=true"

    response = requests.get(string)

    if response.status_code == 200:
        data1 = response.json()
        df1 = pd.json_normalize(data1['hits'])


        if len(df1) == 0:
            raise ValueError("No files to download")
            sys.exit(1)


except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
else:
    sys.exit(0)

