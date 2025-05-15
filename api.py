from fastapi import FastAPI
from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus 
load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = quote_plus(os.getenv("MYSQL_PASSWORD", "password"))  # <-- ENCODE PASSWORD
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_DB = os.getenv("MYSQL_DB", "analytics_db")

app = FastAPI()
engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}")


@app.get("/forecast")
def get_forecast():
    forecast = pd.read_sql("SELECT ds, yhat FROM sales_forecast", engine)
    return forecast.to_dict(orient="records")

@app.get("/recommendations")
def get_recommendations():
    with open("recommendations.txt", "r") as f:
        return {"recommendations": f.read().split("\n")}