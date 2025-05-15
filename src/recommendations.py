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

def generate_recommendations():
    try:
        forecast = pd.read_sql("SELECT ds, yhat, yhat_lower, yhat_upper FROM sales_forecast", engine)
        last_sales = forecast["yhat"].iloc[-1]
        # Simplified rules
        recommendations = []
        if last_sales < forecast["yhat"].mean():
            recommendations.append("Reduce digital ad spend by 15% to save costs.")
            recommendations.append("Increase top product price by 5% to boost revenue.")
            recommendations.append("Introduce bundle offers to increase sales volume.")
        else:
            recommendations.append("Maintain current strategy; sales are stable.")
        # Save recommendations
        with open("recommendations.txt", "w") as f:
            f.write("\n".join(recommendations))
        print("Recommendations generated")
        return recommendations
    except Exception as e:
        print(f"Error during recommendations: {e}")
        return None

if __name__ == "__main__":
    generate_recommendations()