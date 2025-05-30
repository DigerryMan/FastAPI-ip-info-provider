from collections import defaultdict

class RequestParser:
    def parse_ip_location_info(self, response1:dict):
        response_dict = {} 
        response_dict["asn"] = response1.get("isp", {}).get("asn", "N/A")
        response_dict["org"] = response1.get("isp", {}).get("org", "N/A")
        response_dict["location"] = self.parse_location_dict(response1.get("location", {}))
        response_dict["risk_score"] = response1.get("risk", {}).get("risk_score", "N/A")
        return response_dict
    
    def parse_pure_ip_info(self, response2:dict):
        default_dict = defaultdict(lambda: "N/A", response2)
        response_dict = {}

        response_dict["bgp_network"] = default_dict["bgpPrefix"]
        response_dict["total_addresses"] = default_dict["totalAddresses"]

        self.calculate_carriers_from_same_and_other_countries(default_dict, response_dict)
        self.calculate_via_carriers_from_same_and_other_countries(default_dict, response_dict)
            
        return response_dict

    def parse_location_dict(self, location_dict:dict):
        location_dict.pop("country_code", None)
        location_dict.pop("timezone", None)
        location_dict.pop("localtime", None)
        return location_dict

    def parse_weather(self, response):
        response = response["current"]
        rain = response["precipitation"]
        wind = response["windspeed_10m"]
        value =  "high" if rain > 7.5 or wind > 50 else "low"
        return {"internet_lag_risk" : value}

    def calculate_carriers_from_same_and_other_countries(self, response2, response_dict):
        carriers = response2["carriers"]
        carriers_from_the_same_country = "N/A"
        carriers_from_other_countries = "N/A"

        if carriers != "N/A":
            carriers_from_the_same_country = 0
            carriers_from_other_countries = 0
            for carrier in carriers:
                if carrier["registeredCountryName"] == response2["registeredCountryName"]:
                    carriers_from_the_same_country += 1
                else:
                    carriers_from_other_countries += 1

        response_dict["carriers_from_the_same_country"] = carriers_from_the_same_country
        response_dict["carriers_from_other_countries"] = carriers_from_other_countries

    def calculate_via_carriers_from_same_and_other_countries(self, default_dict, response_dict):
        list_of_via_carriers = default_dict["viaCarriers"]
        via_carriers_from_the_same_country = "N/A"
        via_carriers_from_other_countries = "N/A"
        diffrent_countries_set = set()

        if list_of_via_carriers != "N/A":
            via_carriers_from_the_same_country = 0
            via_carriers_from_other_countries = 0
            for carrier in list_of_via_carriers:
                if carrier["registeredCountryName"] == default_dict["registeredCountryName"]:
                    via_carriers_from_the_same_country += 1
                else:
                    via_carriers_from_other_countries += 1
                    diffrent_countries_set.add(carrier["registeredCountryName"])

        diff_countries = list(diffrent_countries_set) if diffrent_countries_set else "N/A"
        response_dict["via_carriers_from_the_same_country"] = via_carriers_from_the_same_country
        response_dict["via_carriers_from_other_countries"] = via_carriers_from_other_countries
        response_dict["diffrent_countries"] = diff_countries  
