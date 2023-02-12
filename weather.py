import argparse
import json
import sys
from configparser import ConfigParser
from urllib import parse, request, error

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
    """Builds the URL for an API request to OpenWeather's API.

    Args:
        city_input (List[str]): Name of a city collected by argparse
        imperial (bool): Whether or not to use imperial units for temperature

    Returns:
        str: URL formatted for a call to OpenWeather's city name
    """
    api_key = _get_api_key()
    city_name = " ".join(city_input)
    url_encoded_city_name = parse.quote_plus(city_name)
    units = "imperial" if imperial else "metric"
    url = (
        f"{BASE_WEATHER_API_URL}?q={url_encoded_city_name}"
        f"&units={units}&APPID={api_key}"
    )
    return url


def get_weather_data(query_url):
    """Makes an API request to a URL and returns the data as a Python object.

    Args:
        query_url (str): URL formatted for OpenWeather's city name endpoint
    
    response: make an HTTP GET request to the query_url parameter and saves the result as response
    data: extracts the data from response
    
    Returns:
        dict: Weather information for a specific city
    """
    try:
        response = request.urlopen(query_url)
    except error.HTTPError as http_error:
        if http_error.code == 401: #Unauthorized
            sys.exit("Access denied. Check your API key.")  #sys module allow to exit the program without traceback
        elif http_error.code == 404: #Not found
            sys.exit("Can't find weather data for this city.")
        else:
            sys.exit(f"Something went wrong...({http_error.code})")

    data = response.read()
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        sys.exit("Couldn't read the server response.")


if __name__ == "__main__":
    user_args = read_user_cli_args()
    query_url = build_weather_query(user_args.city, user_args.imperial)
    weather_data = get_weather_data(query_url)
    print(weather_data)

