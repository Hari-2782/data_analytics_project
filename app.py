import streamlit as st
import pandas as pd
import plotly.express as px
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

st.title("Data Analytics & Predictive Analytics Dashboard")

# Load data
df = pd.read_sql("SELECT * FROM retail_sales_cleaned", engine)
forecast = pd.read_sql("SELECT ds, yhat FROM sales_forecast", engine)

# Sales trend
st.subheader("Sales Trend")
fig = px.line(df.groupby("Order Date")["Sales"].sum().reset_index(), x="Order Date", y="Sales")
st.plotly_chart(fig)

# Forecast
st.subheader("Sales Forecast")
fig = px.line(forecast, x="ds", y="yhat", title="90-Day Sales Forecast")
st.plotly_chart(fig)

# Profitability
st.subheader("Profitability Status")
with open("recommendations.txt", "r") as f:
    status = f.read()
st.write(status)