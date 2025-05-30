from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import httpx

from api_requester import APIRequester
from ip.ip_registry import IpRegistry
from ip.ip_validator import IpValidator
from request_parser import RequestParser

api_requester = APIRequester()
request_parser = RequestParser()
ip_registry = IpRegistry()
app = FastAPI()

# SERVER_HTML python -m http.server 8080    link: "http://127.0.0.1:8080"
# APKA (venv) uvicorn main:app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ips/{ip}")
async def check_ip(ip: str):
    if not IpValidator.validate(ip):
        print("Received incorrect ip!")
        raise HTTPException(status_code=404, detail="This ip is incorrect!")
    
    if ip_registry.check_if_already_known(ip):
        print("Sending cached ip information...")
        data = ip_registry.get_data_from_ip(ip)
        return JSONResponse(data)
    
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            ip_info_task = client.get(api_requester.first_api_url(ip))
            network_info_task = client.get(api_requester.second_api_url(ip))

            response1, response2 = await asyncio.gather(ip_info_task, network_info_task)
            handle_api_error(response1, response2)

            ip_location_dict = request_parser.parse_ip_location_info(response1.json())
            pure_ip_info_dict = request_parser.parse_pure_ip_info(response2.json()) 
            response_dict = dict(ip_location_dict)

            if "location" in ip_location_dict:
                weather_response = await client.get(api_requester.third_api_url(ip_location_dict["location"]))
                if weather_response.status_code == 200:
                    weather_data = request_parser.parse_weather(weather_response.json())
                    response_dict.update(weather_data)
                else:
                    raise HTTPException(503, "Error fetching data from weather API")

            response_dict.update(pure_ip_info_dict)

            ip_registry.add_ip(ip, response_dict)
            return JSONResponse(response_dict)
        
        except HTTPException as e:
            print(f"Parser raised HTTPException: {e.detail}")
            raise
        
        except httpx.RequestError as e:
            print(f"Request timeout or connection error: {e}")
            raise HTTPException(503, "Failed to connect to external service. Please try again later")

        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(500, "An unexpected error occurred")
    
@app.get("/ips")
async def get_all_ips():
    return JSONResponse(ip_registry.ip_dict)

def handle_api_error(response1, response2):
    error_occured = False
    error_message = "Error fetching data from "
    
    if response1.status_code != 200:
        error_message += "ip_location "
        error_occured = True

    if response1.status_code != 200 and response2.status_code != 200:
        error_message += "and "

    if response2.status_code != 200:
        error_message += "pure_ip_info "
        error_occured = True

    error_message += "API"
    if error_occured:
        raise HTTPException(503, error_message)