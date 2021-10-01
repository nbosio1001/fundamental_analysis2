import requests
import pandas as pd
from pandas .io.json import json_normalize
from bs4 import BeautifulSoup
import pprint
import json

# def JSON_Request():
TESLA_CIK = "0001318605"
html_website = "https://data.sec.gov/submissions/CIK{}.json".format(TESLA_CIK)
response = requests.get(html_website, headers={'User-Agent': 'Mozilla/5.0'})
json_response = response.json()
# print(filings)
df = pd.DataFrame.from_dict(json_response["filings"]["recent"])

company_10ks = df[df["form"]=="10-K"]
print(company_10ks.columns)
company_10ks['link'] = company_10ks["accessionNumber"] \
    .apply(lambda row: f'https://www.sec.gov/cgi-bin/viewer?action=view&cik=1318605&accession_number={row}&xbrl_type=v')
# company_10ks["link"] = company_10ks[company_10ks[:,acces"https://www.sec.gov/cgi-bin/viewer?action=view&cik=1318605&accession_number={}&xbrl_type=v".format(company_10ks.loc[:,"accessionNumber"])
print(company_10ks["link"].head())


# Website we want https://www.sec.gov/cgi-bin/viewer?action=view&cik=1318605&accession_number=0001564590-21-004599&xbrl_type=v

https://data.sec.gov/api/xbrl/companyfacts/CIK0001318605.json

API endpoint, specific request,

line 1614