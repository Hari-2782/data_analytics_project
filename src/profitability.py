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
engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}")

def check_profitability():
    try:
        # Assume expenses are 70% of sales (simplified)
        forecast = pd.read_sql("SELECT ds, yhat FROM sales_forecast", engine)
        forecast["expenses"] = forecast["yhat"] * 0.7
        forecast["profit"] = forecast["yhat"] - forecast["expenses"]
        # Check last forecasted profit
        last_profit = forecast["profit"].iloc[-1]
        if last_profit > 0:
            print("Business is on track")
            return "profit"
        else:
            print("Loss detected, triggering AI recommendations")
            return "loss"
    except Exception as e:
        print(f"Error during profitability check: {e}")
        return None

if __name__ == "__main__":
    check_profitability()