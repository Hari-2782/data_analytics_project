import pandas as pd
from prophet import Prophet
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus 
import matplotlib.pyplot as plt
load_dotenv()
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = quote_plus(os.getenv("MYSQL_PASSWORD", "password"))  # <-- ENCODE PASSWORD
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_DB = os.getenv("MYSQL_DB", "analytics_db")
engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}")

def forecast_sales():
    try:
        df = pd.read_sql("SELECT `Order Date` AS Date, Sales FROM retail_sales_cleaned", engine)
        # Prepare data for Prophet
        df_prophet = df.groupby("Date")["Sales"].sum().reset_index()
        df_prophet.columns = ["ds", "y"]
        # Train model
        print(df.columns)
        model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=True)
        model.fit(df_prophet)
        # Forecast for next 90 days
        future = model.make_future_dataframe(periods=90)
        forecast = model.predict(future)
        # Save forecast
        forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_sql("sales_forecast", engine, if_exists="replace", index=False)
        # Plot
        model.plot(forecast)
        plt.savefig("sales_forecast.png")
        print("Forecasting completed")
        return forecast
    except Exception as e:
        print(f"Error during forecasting: {e}")
        return None

if __name__ == "__main__":
    forecast_sales()
