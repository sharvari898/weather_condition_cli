import requests
import json
import logging
"""
Author : Sharvari D 27-12-2025 Developed weather.py
Updated: Sharvari Added logs
"""
logging.basicConfig(
    level=logging.INFO,   # change to DEBUG if needed
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


def get_weather(city,url,api_key):
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    logger.info(f"{params}")

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        logger.info(f"hit the api")
        return response.status_code,response.json()
    except requests.exceptions.Timeout:
        logger.error("Request timed out")
    except requests.exceptions.HTTPError:
        logger.error("HTTP error: %s", response.text)
    except requests.exceptions.RequestException as e:
        logger.error("Request failed: %s", e)
        logger.info(f"exception occured in get weather")
        return None


def print_weather(data):
    try:
        weather_data = dict()
        weather_data["city"] = data['name']
        weather_data["Temperature"] = data['main']['temp']
        weather_data["Condition"] = data['weather'][0]['description']
        weather_data["wind speed"] = data['wind']['speed']
        weather_data["Humidity"] = data['main']['humidity']
        logger.info("read weather condition")
        return  weather_data
    except Exception as e:
        print(f"exception occured in print weather {e}")

def main():
    try:
        cities = input("Enter city name seperated by comma: ").strip().split(",")
        if not cities or cities !="":
            file = open("config.json", "r")
            data = file.read()
            file.close()
            config_data = json.loads(data)
            api_key = config_data["api_key"]
            url = config_data["weather_url"]
            logger.info("read weather condition")
            for city in cities:
                status,weather_info = get_weather(city,url,api_key)
                logger.info("received weather response")
                if status == 200:
                    weather_data = print_weather(weather_info)
                    logger.info("read weather condtion successfully")
                    print(weather_data)
                else:
                    logger.info(f"error occured while hiting the api {status}")
                    print("no data returned status code : ", status)
    except Exception as e:
        print("An Error occured in main function", e)



if __name__ == "__main__":
    main()
    logger.info("calling mail function")
