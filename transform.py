import pandas as pd
import requests
import os

def transform_symbols_dict(data):
    symbol_dict = data.get('symbols', [])

    transformed_data = []

    for sym in symbol_dict :
        cleaned_symbol = {
            'Symbol'       : sym.get('symbol'),
            'Base_Asset'   : sym.get('baseAsset'),
            'Quote_Asset'  : sym.get('quoteAsset'),
            'Status'       : sym.get('status'),
            'Spot_Ready'   : "Yes" if sym.get('isSpotTradingAllowed') else "No",
            'Margin_Ready' : "Yes" if sym.get('isMarginTradingAllowed') else "No"
        }

    transformed_data.append(cleaned_symbol)
    df = pd.DataFrame(transformed_data)
    return df

result_df = transform_symbols_dict(result)

print(result_df.head())



