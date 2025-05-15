import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus  # <-- ADD THIS

load_dotenv()

# Database connection
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = quote_plus(os.getenv("MYSQL_PASSWORD", "password"))  # <-- ENCODE PASSWORD
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_DB = os.getenv("MYSQL_DB", "analytics_db")

print(f"MYSQL_USER: '{MYSQL_USER}'")
print(f"MYSQL_PASSWORD: '{MYSQL_PASSWORD}'")
print(f"MYSQL_HOST: '{MYSQL_HOST}'")
print(f"MYSQL_DB: '{MYSQL_DB}'")

# Show the connection string
print(f"Connection string: mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}")

engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}")

def ingest_data(file_path):
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            raise ValueError("Empty dataset")
        df.to_sql("retail_sales", engine, if_exists="replace", index=False)
        print("Data ingested successfully")
        return df
    except Exception as e:
        print(f"Error during ingestion: {e}")
        return None

if __name__ == "__main__":
    file_path = "D:/Prg_Language/data_analytics_project/data/train.csv"
    ingest_data(file_path)
