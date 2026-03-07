import json
import requests
from datetime import datetime
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler("weather_report.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def get_coordinates(city, zip_code):
    geo_resp = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "countryCode": "US"},
        timeout=10
    )
    geo_resp.raise_for_status()

    for item in geo_resp.json().get("results", []):
        if zip_code in item.get("postcodes", []):
            lat = item["latitude"]
            lon = item["longitude"]
            logger.debug(f"Coordinates found: {lat}, {lon}")
            return lat, lon

    raise ValueError(f"No match found for {city} with ZIP {zip_code}")


def get_weather(lat, lon, temp_unit, wind_unit):
    weather_resp = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,wind_speed_10m",
            "temperature_unit": temp_unit,
            "wind_speed_unit": wind_unit
        },
        timeout=10
    )
    weather_resp.raise_for_status()

    current = weather_resp.json().get("current", {})
    temp = current.get("temperature_2m")
    wind = current.get("wind_speed_10m")

    if temp is None or wind is None:
        raise ValueError("Weather response missing temperature or wind data.")

    logger.debug(f"Weather data: temp={temp}, wind={wind}")
    return temp, wind



def main():
    try:
        with open("config_data.json", "r") as file:
            data = json.load(file)

        weather_config = data["weather"]
        city = weather_config["city"]
        zip_code = weather_config["zip"]
        units = weather_config["units"]
        alert_temp = float(weather_config["alert_temp"])

        logger.debug(f"Loaded config for {city} ({zip_code})")

        if units == "imperial":
            temp_unit, wind_unit, symbol = "fahrenheit", "mph", "°F"
        elif units == "metric":
            temp_unit, wind_unit, symbol = "celsius", "kmh", "°C"
        else:
            raise ValueError("units must be 'imperial' or 'metric'")

        lat, lon = get_coordinates(city, zip_code)
        temp, wind = get_weather(lat, lon, temp_unit, wind_unit)

        alert_triggered = temp < alert_temp

        if alert_triggered:
            logger.warning(f"ALERT: Temp {temp}{symbol} below threshold {alert_temp}")
        else:
            logger.info(f"No alert. Temp {temp}{symbol} above threshold.")

        weather_report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "city": city,
            "zip": zip_code,
            "temp": temp,
            "temp_unit": symbol,
            "wind_speed": wind,
            "wind_unit": wind_unit,
            "alert": alert_triggered
        }

        with open("weather_report.jsonl", "a") as report_file:
            report_file.write(json.dumps(weather_report) + "\n")

        logger.info("Report successfully written to weather_report.jsonl")

    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Config error: {e}")
    except (KeyError, ValueError) as e:
        logger.error(f"Data validation error: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()