import requests

TESLA_CIK = 0001318605
response = requests.get("https://data.sec.gov/submissions/CIK{}.json".format(TESLA_CIK))
print(response.status)
# https://data.sec.gov/submissions/CIK##########.json





