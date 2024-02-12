import pandas as pd
import requests

# get resource if from url and enter it here
resourceid = 'M890991'
apiendpoint = 'https://tablebuilder.singstat.gov.sg/api/table/tabledata/'
seriesno = '1'                                          #inspect JSON and determine 
url = apiendpoint + resourceid + '?seriesNoORrowNo=' + seriesno
headers = {'User-Agent': 'Mozilla/5.0', "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8"}

#Get data from API and convert to JSON
response = requests.get(url, headers=headers)
json = response.json()

#Read into pandas df and normalize nested JSON structure
df = pd.json_normalize(json, record_path=['Data','row', 'columns'])
df.columns = ['Date','Tariff']              #rename columns
df.Date = pd.to_datetime(df.Date, format='%Y %b')

# write to csv
df.to_csv('elec_tariff.csv',index=False)