import requests
import os
import pandas as pd

def extract_api():
    url = f"https://binance43.p.rapidapi.com/exchangeInfo?symbol=ETHBTC"

    headers = {
        "x-rapidapi-host": os.getenv("API_HOST"),
        "x-rapidapi-key" : os.getenv("API_KEY")
    }

    response = requests.get(url, headers=headers)

    response.raise_for_status()

    data = response.json()

    return data

result = extract_api()

print(result, [])






