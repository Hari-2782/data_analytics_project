import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus 

load_dotenv()
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = quote_plus(os.getenv("MYSQL_PASSWORD", "password"))  # <-- ENCODE PASSWORD
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_DB = os.getenv("MYSQL_DB", "analytics_db")
# Database connection
# engine = create_engine(f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}")
engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}")

def preprocess_data():
    try:
        # Load data from MySQL
        df = pd.read_sql("SELECT * FROM retail_sales", engine)

        # Handle missing values
        fill_dict = {}
        if "Sales" in df.columns:
            fill_dict["Sales"] = df["Sales"].mean()
        if "Price" in df.columns:
            fill_dict["Price"] = df["Price"].mean()
        df.fillna(fill_dict, inplace=True)

        # Convert date columns
        for col in ["Order Date", "Ship Date"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], dayfirst=True)

        # Remove outliers (e.g., sales > 99th percentile)
        if "Sales" in df.columns:
            df = df[df["Sales"] <= df["Sales"].quantile(0.99)]

        # Save cleaned data
        df.to_sql("retail_sales_cleaned", engine, if_exists="replace", index=False)
        print("Data preprocessed successfully")
        return df
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        return None


if __name__ == "__main__":
    preprocess_data()