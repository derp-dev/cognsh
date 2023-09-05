# https://docs.golden.com/reference/public_api_schema_entitytypes_list
# https://docs.golden.com/reference/schema-1
import requests

url = "https://golden.com/api/v2/public/schema/predicates/"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.text)




url = "https://golden.com/api/v2/public/schema/entityTypes/"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.text)  