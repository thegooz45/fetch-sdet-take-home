import argparse
import requests
import sys

def fetch_coordinates(location, api_key):
    """ using OpenWeatherMap's API, fetch the latitude, longitude, and place for a given city, state, or zip code"""
    base_url = "http://api.openweathermap.org/geo/1.0/"

    # checking if location is a zip code
    if location.isdigit():
        url = f"{base_url}zip?zip={location}&appid={api_key}"
    else:
        city, state = map(str.strip, location.split(","))
        if state.upper in ["HI", "AK"]:
            raise ValueError("hawaii and alaska are not supported!")
        url = f"{base_url}direct?q={city},{state},US&limit=1&appid={api_key}"

    # making the request
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"API request failed! status code {response.status_code}: {response.text}")
    
    data = response.json()
    if not data:
        raise ValueError(f"Location {location} not found!")
    
    # extracting the data
    result = data[0] if isinstance(data, list) else data
    return {
        "location": location,
        "name": result.get("name", location),
        "latitude": result.get("lat"),
        "longitude": result.get("lon")
    }

# the main function
def main():
    parser = argparse.ArgumentParser(description="fetch the coordinates for a given location")
    parser.add_argument("--locations", nargs="+", required=True, help="list of city/state or zip code")
    parser.add_argument("--api_key", required=True, help="OpenWeatherMap API key")
    args = parser.parse_args()

    results = []
    for location in args.locations:
        try:
            result = fetch_coordinates(location, args.api_key)
            results.append(result)
        except Exception as e:
            print(f"error fetching location {location}: {e}", file=sys.stderr)
    
    for res in results:
        print(res)

if __name__ == "__main__":
    main()