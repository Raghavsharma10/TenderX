import requests

BASE_URL = "https://restcountries.com/v3.1"

def make_request(endpoint, fields=None):
    if isinstance(fields, str):
        fields = [fields]
    url = f"{BASE_URL}/{endpoint}"
    if fields:
        url += f"?fields={','.join(fields)}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_country_by_name(name, fields=None):
    return make_request(f"name/{name}", fields)

def get_country_by_capital(capital, fields=None):
    return make_request(f"capital/{capital}", fields)

def get_country_by_currency(currency, fields=None):
    return make_request(f"currency/{currency}", fields)

def get_country_by_language(language, fields=None):
    return make_request(f"lang/{language}", fields)

def get_countries_by_subregion(subregion, fields=None):
    return make_request(f"subregion/{subregion}", fields)

def get_all_countries(fields=None):
    return make_request("all", fields)