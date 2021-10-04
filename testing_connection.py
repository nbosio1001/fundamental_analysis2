import http.client
# print(dir(http.client))
connection = http.client.HTTPSConnection("efts.sec.gov/LATEST/search-index")
# print(help(connection.request))
# connection.request("POST","efts.sec.gov/LATEST/search-index")
# response = connection.getresponse()
# print(response)
# print(dir(h1))
# print(h1.getresponse)
# connection.request("GET", "/")
# response = connection.getresponse()
import json
from urllib.request import urlopen
text = "tesla"
headers = {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}
connection.request("POST",'/',text,headers)
response = connection.getresponse()
print(response.read().decode())