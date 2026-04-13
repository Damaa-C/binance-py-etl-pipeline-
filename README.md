#  Binance-to-Aiven Cloud ETL Pipeline
##  Introduction
This project is a Modular ETL (Extract, Transform, Load) system designed to synchronize real-time financial metadata from the Binance API to a cloud-hosted PostgreSQL database.

The goal of this pipeline is to turn volatile API responses into a persistent, queryable data asset. This is a foundational project for building crypto-analytics dashboards or trading signal monitors.

##  Project Architecture: Why Modularity Matters
To ensure the code is scalable and maintainable, the logic is split into functional components:

- `extract_api()`:

- Functions as the "Sensor."

- Connects to the Binance exchange info endpoint.

- Uses Environment Variables (.env) to securely handle API keys.
  
[extract.py](https://github.com/Damaa-C/binance-py-etl-pipeline-/blob/main/extract.py)

- `transform_symbols_dict()`:

Functions as the "Processor."

Flattens nested JSON into a structured Pandas DataFrame.

Implements logic to convert boolean trading flags into human-readable "Yes/No" formats.

[transform.py](https://github.com/Damaa-C/binance-py-etl-pipeline-/blob/main/transform.py)

- `load_to_postgres()`:

Functions as the "Storage Engine."

Connects to Aiven PostgreSQL using SSL encryption.

Uses Upsert (ON CONFLICT) logic to ensure the pipeline is Idempotent (re-runnable without duplicating data).

[load.py](https://github.com/Damaa-C/binance-py-etl-pipeline-/blob/main/load.py) 

- `main_etl.py`:

The Compiler. It coordinates the flow of data between the three modules.

[main.py](https://github.com/Damaa-C/binance-py-etl-pipeline-/blob/main/main.py) 

##  Testing & Validation: test.ipynb
Before moving to a production-ready script, the pipeline was rigorously tested in a Jupyter Notebook ([test.ipynb](https://github.com/Damaa-C/binance-py-etl-pipeline-/blob/main/test.ipynb)).

Why? Notebooks allow for cell-by-cell execution, which was essential for:

- Verifying that the 3,500+ rows of data didn't exceed the  limits of the development.

- Inspecting the DataFrame head to ensure column mapping was accurate.

- Debugging SQL constraints (like the VARCHAR limit error) in a sandbox environment.

## Execution Output & Debugging
The following output demonstrates a successful run of the pipeline, including how the system handles real-world data constraints:

Plaintext
 [1/3] Fetching data from API...
 [2/3] Transforming JSON to structured DataFrame...
 [3/3] Loading 3559 rows to Aiven Cloud...

# --- Preview of Processed Data ---
   ```
symbol base_asset quote_asset   status spot_ready margin_ready
0  ETHBTC        ETH         BTC  TRADING        Yes          Yes
1  LTCBTC        LTC         BTC  TRADING        Yes          Yes
2  BNBBTC        BNB         BTC  TRADING        Yes          Yes
3  NEOBTC        NEO         BTC  TRADING        Yes           No
4 QTUMETH       QTUM         ETH    BREAK        Yes           No
```
✅ Success: 3559 rows synchronized with Aiven PostgreSQL.
Note on Innovation: During the first run, the pipeline identified a value too long for type character varying(10) error. This was a critical learning moment—I refactored the database schema to VARCHAR(20) to handle longer token names, ensuring the pipeline is resilient to future API changes.

##  Security & Configuration
To maintain professional security standards:

`.env` File: All sensitive credentials (DB passwords, API keys) are stored in a local .env file.

`.gitignore`: This file is explicitly ignored by Git to prevent accidental leakage of cloud credentials to public repositories.

`OS Library`: Used os.getenv to pull secrets into the runtime environment securely.

## How to Run
`Clone` the repo.

Create a `.env` file with your Aiven and Binance credentials.

Run python `main_etl.py`.
