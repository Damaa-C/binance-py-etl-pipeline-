import psycopg2 as psy
from psycopg2 import extras
import os

def load_to_postgres(df,btc_info):

    try:
        conn = psy.connect(
            host = os.getenv("DB_HOST"),
            port = os.getenv("DB_PORT"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            dbname = os.getenv("DB_NAME"),
            sslmode = "require"
        )
        cur = conn.cursor()

        create_query = f"""
        CREATE TABLE IF NOT EXISTS {btc_info} (
            symbol VARCHAR(20) PRIMARY KEY,
            base_asset VARCHAR(10),
            quote_asset VARCHAR(10),
            status VARCHAR(20),
            spot_ready VARCHAR(5),
            margin_ready VARCHAR(5),
            extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cur.execute(create_query)

        data_tuples = [tuple(x) for x in df.to_numpy()]

        insert_query = f"""
        INSERT INTO {btc_info} (symbol, base_asset, quote_asset, status, spot_ready, margin_ready)
        VALUES %s
        ON CONFLICT (symbol) DO UPDATE SET
            status = EXCLUDED.status,
            spot_ready = EXCLUDED.spot_ready,
            margin_ready = EXCLUDED.margin_ready;
        """
        extras.execute_values(cur, insert_query, data_tuples)

        conn.commit()
        print(f"Cloud Load Complete: {len(df)} rows sent to Aiven via psycopg2.")

    except Exception as e:
        print(f" Database Error: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()


load_to_postgres(result_df, "stg_binance_symbols")
