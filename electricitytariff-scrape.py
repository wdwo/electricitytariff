import pandas as pd
import requests
import gspread as gs

#environment secrets
credentials = os.environ.get('API_KEY')

#google sheets variables and authentication
# gsheet_url = 'https://docs.google.com/spreadsheets/d/1CDjYlS68ARa4wq_wD9vrbDHkixNTc2fiMqaArUUA1Cs/'
# sheet_tabid = '1123207130'                                                          #id number found at the end of url gid=xxxxxxx
# gc = gs.service_account_from_dict(credentials)
# gsht = gc.open_by_url(gsheet_url).get_worksheet_by_id(sheet_tabid)             


# get resource if from url and enter it here
resourceid = 'M890991'
apiendpoint = 'https://tablebuilder.singstat.gov.sg/api/table/tabledata/'
seriesno = '1'                                          #inspect JSON and determine 
url = apiendpoint + resourceid + '?seriesNoORrowNo=' + seriesno
headers = {'User-Agent': 'Mozilla/5.0', "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8"}

# Function to pull google sheets to df
def df_from_gsheets(gsheetobject):
    df0 = pd.DataFrame(gsheetobject.get_all_records())
    df0['Date'] = pd.to_datetime(df0['Date'], errors='coerce')                   #parsing Date column to datetime
    df0['Tariff'] = pd.to_numeric(df0['Tariff'])                                 #parsing Tariff column to numeric
    df0['amt'] = pd.to_numeric(df0['amt'])                                       #parse Tariff to numeric type
    return df0



#Get data from API and convert to JSON
response = requests.get(url, headers=headers)
json = response.json()

#Read into pandas df and normalize nested JSON structure
df = pd.json_normalize(json, record_path=['Data','row', 'columns'])
df.columns = ['Date','Tariff']              #rename columns
df.Date = pd.to_datetime(df.Date, format='%Y %b')

# Read gsheets data into df

# write to csv
df.to_csv('elec_tariff.csv',index=False)
