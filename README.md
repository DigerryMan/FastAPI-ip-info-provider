# 🛰️ IP Info API – FastAPI

A Python application built with **FastAPI** that fetches detailed information about IP addresses using external APIs. It returns data such as IP location, network details, and current weather conditions based on the IP's location.

## 🛠 Technologies Used

- **FastAPI** – modern, high-performance web framework
- **httpx** – async HTTP client for API calls
- **CORS Middleware** – to enable frontend-backend communication
- **HTML + Vanilla JavaScript** – simple web frontend

## 🔗 External APIs Used

- 🌍 IP Location: [ipquery.io](https://ipquery.gitbook.io/ipquery-docs)  
- 🧠 Network Info: [bigdatacloud.com](https://www.bigdatacloud.com/ip-geolocation#apilist)  
- ☁️ Weather Data: [open-meteo.com](https://open-meteo.com/)

## Endpoints

GET /ips/{ip} – Returns data about a specific IP address

GET /ips – Returns a list of all previously checked IPs
