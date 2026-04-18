import psycopg2 as psy
from sqlalchemy import create_engine
from transform import clean_df
from dotenv import load_dotenv
import os

def load_to_postgres():
    # load environments
    load_dotenv(override=True)

    
    host     = os.getenv("DB_HOST")
    port     = os.getenv("DB_PORT")
    user     = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    dbname   = os.getenv("DB_NAME")
    sslmode  = "require"

    try:

        engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}?{sslmode}")

        clean_df.to_sql('binance_tickers', con=engine, if_exists='append', index=False)

        print(f"Successfully loaded {len(clean_df)} rows to the database.")
        
    except Exception as e:
        print(f"Error occurred: {e}")

load_to_postgres()
