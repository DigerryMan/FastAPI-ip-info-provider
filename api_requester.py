# 91.123.181.184

# API LINKS
#https://ipquery.gitbook.io/ipquery-docs  
#https://www.bigdatacloud.com/ip-geolocation#apilist"
#https://open-meteo.com/

class APIRequester:
    def __init__(self):
        self.FIRST_API = "https://api.ipquery.io/"
        self.SECOND_API = "https://api-bdc.net/data/network-by-ip"
        self.WEATHER_API = "https://api.open-meteo.com/v1/forecast"
        self.api_key = ""
        with open("api_key.txt") as f:
            self.api_key = f.read().strip()
            if self.api_key.__contains__("PASTE_UR_API_KEY"):
                print("\nPASTE_UR_API_KEY into api_key.txt\n")
                raise KeyError("PASTE_UR_API_KEY into api_key.txt")

    def first_api_url(self, ip:str):
        return self.FIRST_API + ip

    def second_api_url(self, ip:str):
        return f"{self.SECOND_API}?ip={ip}&localityLanguage=en&key={self.api_key}"
    
    def third_api_url(self, location):
        lat, lon = location["latitude"], location["longitude"]
        return f"{self.WEATHER_API}?latitude={lat}&longitude={lon}&current=weathercode,precipitation,windspeed_10m"
