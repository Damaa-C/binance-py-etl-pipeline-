from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv



def run_binance_pipeline():

    try:
        # load environments

        load_dotenv(override=True)

        host     = os.getenv("DB_HOST")
        port     = os.getenv("DB_PORT")
        user     = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        dbname   = os.getenv("DB_NAME")
        sslmode  = "require"
        
        # --- 1. EXTRACT ---


        print("Step 1: Extracting from Binance...")

        url = "https://api.binance.com/api/v3/ticker/24hr"

        params = {
        'symbolStatus': 'TRADING',
        'type': 'FULL'
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
    

        # --- 2. TRANSFORM ---


        print("Step 2: Transforming data with Pandas...")

        df = pd.DataFrame(data)
    
        cols_to_keep = ['symbol', 'priceChange', 'priceChangePercent', 'lastPrice', 'volume', 'openTime']
        
        df = df[cols_to_keep]
    
        numeric_cols = ['priceChange', 'priceChangePercent', 'lastPrice', 'volume']

        for col in numeric_cols:
            
            df[col] = pd.to_numeric(df[col])
        
        df['openTime'] = pd.to_datetime(df['openTime'], unit='ms')
    
        df = df[df['symbol'].str.endswith('USDT')]
    

        # --- 3. LOAD ---

        print(f"Step 3: Loading {len(df)} rows to Aiven Cloud...")

        engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}?{sslmode}")
    
        df.to_sql('binance_tickers', con=engine, if_exists='append', index=False)

        print("Success: Pipeline complete.")

        return True
    
    except Exception as e:
        print(f" Pipeline failed! Error: {e}")
        raise


with DAG (
    dag_id     = "damaa_binance_etl_pipeline",
    start_date = datetime (2026,1,1),
    scheduler  = timedelta(hours=1),
    catchup    = False
) as dag:
    
    run_binance_pipeline_task = PythonOperator(
        task_id = "execute binance etl",
        pythoncallable = run_binance_pipeline
    )
    
  