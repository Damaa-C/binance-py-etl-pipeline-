import requests 


def extract_binance():

    url = f"https://api.binance.com/api/v3/ticker/24hr"

    params = {
        'symbolStatus': 'TRADING',
        'type': 'FULL'
    }

    response = requests.get(url,params=params)


    response.raise_for_status()

    data = response.json()

    return data

binance_data = extract_binance()

print(binance_data,[])






