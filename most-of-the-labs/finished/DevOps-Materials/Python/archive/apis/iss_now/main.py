import requests

response = requests.get("http://api.open-notify.org/iss-now.json") # this is a valid url and will return a response
# response = requests.get("http://api.open-notify.org/iss-nows.json") # this is an invalid url and will cause an error
print(response)
# print(response.status_code)

# if response.status_code == 200:
#     print("an error occurred")

response.raise_for_status()

data = response.json()

print(data)
# easyli access the longitude and latitude of the iss
longitude = data["iss_position"]["longitude"]
latitude = data["iss_position"]["latitude"]