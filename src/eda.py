import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import sweetviz as sv
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus 
load_dotenv()
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = quote_plus(os.getenv("MYSQL_PASSWORD", "password"))  # <-- ENCODE PASSWORD
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_DB = os.getenv("MYSQL_DB", "analytics_db")
# engine = create_engine(f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}")
engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}")

def run_eda():
    try:
        df = pd.read_sql("SELECT * FROM retail_sales_cleaned", engine)
        # Statistical summary
        print(df.describe())
        # Correlation heatmap
        plt.figure(figsize=(10, 6))
        sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
        plt.savefig("correlation_heatmap.png")
        # Sales trend
        plt.figure(figsize=(12, 6))
        df.groupby("Date")["Sales"].sum().plot()
        plt.title("Sales Trend Over Time")
        plt.savefig("sales_trend.png")
        # Automated EDA report
        report = sv.analyze(df)
        report.show_html("eda_report.html")
        print("EDA completed")
    except Exception as e:
        print(f"Error during EDA: {e}")

if __name__ == "__main__":
    run_eda()