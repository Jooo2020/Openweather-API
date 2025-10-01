import requests

api_key = "4bf98e075d88a2d3e40ee0655aa76d74"
city = "innsbruck"

#limit is optional
geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={5}&appid={api_key}"

# JSON-Anfrage auf Server
response = requests.get(geo_url)
# Umwandlung in Dictionary
result = response.json()
print(result[1]["lat"])
print(result[1]["lon"])






#weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&lang={de}"