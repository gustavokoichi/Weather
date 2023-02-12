import argparse
from configparser import ConfigParser
from urllib import parse

BASE_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

# Starting a function with _ indicates that it should be non-public


def _get_api_key():
    """
    Fetch the api key from section [openweather] in secrets.ini file
    Returns: api_key

    OBS: API KEY FILE SHOULD NEVER BE COMMITED FOR SAFETY
    """

    config = ConfigParser()
    config.read("secrets.ini")
    return config["openweather"]["api_key"]


def read_user_cli_args():
    """
    Handle user CLI interactions
    
    "city" is an argument that will take 1 or more inputs separated by
    whitespace. Setting nargs to "+", users can pass city names that
    have more than 1 word

    Returns: argparse.Namespace: Populated namespace object
    """

    parser = argparse.ArgumentParser(
        description="Gets weather and temperature from a city."
    )

    parser.add_argument(
        "city",
        nargs="+",
        type=str,
        help="Enter city name",
    )

    parser.add_argument(
        "-i",
        "--imperial",
        action="store_true",
        help="Display the temperature in Fahrenheit",
    )
    return parser.parse_args()


def build_weather_query(city_input, imperial=False):
    api_key = _get_api_key()
    city_name = " ".join(city_input)
    url_encoded_city_name = parse.quote_plus(city_name)
    units = "imperial" if imperial else "metric"
    url = (
        f"{BASE_WEATHER_API_URL}?q={url_encoded_city_name}"
        f"&units={units}&APPID={api_key}"
    )
    return url

if __name__ == "__main__":
    user_args = read_user_cli_args()
    query_url = build_weather_query(user_args.city, user_args.imperial)
    print(query_url)

