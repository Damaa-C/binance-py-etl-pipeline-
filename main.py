import requests
import os
import pandas as pd
import psycopg2 as psy
from psycopg2 import extras
from datetime import datetime

# --- PHASE 1: EXTRACT ---
def extract_api():
    """Fetches raw exchange information from the Binance API."""
    print("🔍 [1/3] Fetching data from API...")
    
    url = "https://binance43.p.rapidapi.com/exchangeInfo"
    headers = {
        "x-rapidapi-host": os.getenv("API_HOST"),
        "x-rapidapi-key": os.getenv("API_KEY")
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status() # Stops script if API call fails
    return response.json()

# --- PHASE 2: TRANSFORM ---
def transform_symbols(data):
    """Cleans the raw JSON and flattens it into a Pandas DataFrame."""
    print(" [2/3] Transforming JSON to structured DataFrame...")
    symbols_list = data.get('symbols', [])
    transformed_data = []

    for sym in symbols_list:
        # We extract only the fields required for the SQL schema
        cleaned_symbol = {
            'symbol'       : sym.get('symbol'),
            'base_asset'   : sym.get('baseAsset'),
            'quote_asset'  : sym.get('quoteAsset'),
            'status'       : sym.get('status'),
            'spot_ready'   : "Yes" if sym.get('isSpotTradingAllowed') else "No",
            'margin_ready' : "Yes" if sym.get('isMarginTradingAllowed') else "No"
        }
        transformed_data.append(cleaned_symbol)
    
    return pd.DataFrame(transformed_data)

# --- PHASE 3: LOAD ---
def load_to_postgres(df, btc_info):
    """Loads the DataFrame into Aiven PostgreSQL with Upsert logic."""
    print(f"[3/3] Loading {len(df)} rows to Aiven Cloud...")
    conn = None
    try:
        conn = psy.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            dbname=os.getenv("DB_NAME"),
            sslmode="require"
        )
        cur = conn.cursor()

        # Define Schema
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {btc_info} (
                symbol VARCHAR(20) PRIMARY KEY,
                base_asset VARCHAR(10),
                quote_asset VARCHAR(10),
                status VARCHAR(20),
                spot_ready VARCHAR(5),
                margin_ready VARCHAR(5),
                extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Execute Batch Upsert
        data_tuples = [tuple(x) for x in df.to_numpy()]
        insert_query = f"""
            INSERT INTO {btc_info} (symbol, base_asset, quote_asset, status, spot_ready, margin_ready)
            VALUES %s
            ON CONFLICT (symbol) DO UPDATE SET
                status = EXCLUDED.status,
                spot_ready = EXCLUDED.spot_ready,
                margin_ready = EXCLUDED.margin_ready,
                extracted_at = CURRENT_TIMESTAMP;
        """
        extras.execute_values(cur, insert_query, data_tuples)
        conn.commit()
        print(f" Pipeline Success: Data is live in {btc_info}.")

    except Exception as e:
        print(f" Database Error: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    try:
        # 1. Start Extraction
        raw_api_data = extract_api()
        
        # 2. Start Transformation
        final_df = transform_symbols(raw_api_data)
        
        # 3. Start Load
        if not final_df.empty:
            load_to_postgres(final_df, "stg_binance_symbols")
            # Preview for verification
            print("\nPreview of Loaded Data:")
            print(final_df.head())
        else:
            print(" No data found to load.")
            
    except Exception as pipeline_error:
        print(f"Critical Pipeline Failure: {pipeline_error}")