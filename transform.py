import pandas as pd
from extract import binance_data
from datetime import datetime

def transform_binance():

    df = pd.DataFrame(binance_data)

    cols_to_keep = [
        'symbol', 'priceChange', 'priceChangePercent', 
        'lastPrice', 'volume', 'quoteVolume', 'openTime'
    ]

    df = df[cols_to_keep]

    numeric_cols = ['priceChange', 'priceChangePercent', 'lastPrice', 'volume', 'quoteVolume']

    for col in numeric_cols:

        df[col] = pd.to_numeric(df[col], errors='coerce')

    df['openTime'] = pd.to_datetime(df['openTime'], unit='ms')

    return df

clean_df = transform_binance()

print(clean_df.head())





