# Binance to Aiven PostgreSQL ETL Pipeline
### Data Engineering Project 

## 1. Project Overview
This project demonstrates an automated **ETL (Extract, Transform, Load)** pipeline. It fetches real-time market data from the Binance API, processes it for analytical readiness using Python, and stores it in a managed PostgreSQL database on the Aiven Cloud.

---

## 2. Testing & Environment Strategy

### **Jupyter Notebook (The Testing Sandbox)**
Before script finalization, **Jupyter Notebooks** were used to prototype and validate the pipeline logic cell-by-cell.
> ![deploy.ipynb](https://github.com/Damaa-C/binance-py-etl-pipeline-/blob/main/test.ipynb)

* **Data Profiling:** Used `df.shape` and `df.dtypes` to ensure the 1,400+ rows were structured correctly.
* **Logic Validation:** Verified filtering and timestamp conversion visually.

### **Python Virtual Environment (The Production Core)**
* **Isolation:** Managed via `venv` to ensure dependency stability.
* **Secret Management:** Utilized `python-dotenv` for `.env` file security.
> ![pipeline.py](https://github.com/Damaa-C/binance-py-etl-pipeline-/blob/main/pipeline.png)

---

## 3. The ETL Architecture

### **Extract**
* **Source:** Binance 24-hour Ticker API.
* **Code:** [extract.py](https://github.com/Damaa-C/binance-py-etl-pipeline-/blob/main/extract.py)

### **Transform**
* **Cleaning:** Filtered for `USDT` trading pairs and converted numeric types via Pandas.
* **Code:** [transform.py](https://github.com/Damaa-C/binance-py-etl-pipeline-/blob/main/transform.py)

### **Load**
* **Destination:** Aiven Cloud PostgreSQL.
* **Strategy:** Uses `if_exists='append'` for time-series history.
* **Code:** [load.py](https://github.com/Damaa-C/binance-py-etl-pipeline-/blob/main/load.py)

---

## 4. Automation with Apache Airflow
The pipeline is scheduled as a **Directed Acyclic Graph (DAG)** to run every hour.

[Airflow DAG ](https://github.com/Damaa-C/binance-py-etl-pipeline-/blob/main/airflow.py)

* **DAG ID:** `damaa_binance_etl_pipeline`
* **Task:** Single-task `PythonOperator` for simplified monitoring and logging.

---

## 5. Data Success Overview
Verified data structure in Aiven PostgreSQL:

| symbol | priceChange | lastPrice | volume | openTime |
| :--- | :--- | :--- | :--- | :--- |
| BTCUSDT | -540.20 | 64310.50 | 12450.00 | 2026-04-18 20:00:00 |

This shows total rows loaded to postgres.
` SELECT COUNT(*) FROM binance_tickers;`
> ![total rows](https://github.com/Damaa-C/binance-py-etl-pipeline-/blob/main/rows%20loaded%20to%20sql.png)

This shows that data has been loaded to our database; postgres.
` SELECT * FROM binance_tickers;`
> ![Database result](https://github.com/Damaa-C/binance-py-etl-pipeline-/blob/main/data%20overview%20in%20sql.png)

---
*Developed as part of Data Engineering Training - 2026*
