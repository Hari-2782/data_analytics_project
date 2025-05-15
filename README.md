# Data Analytics & Predictive Analytics Project

This project is an end-to-end data analytics and forecasting pipeline for retail sales data. It includes data ingestion, preprocessing, exploratory data analysis (EDA), forecasting using Prophet, profitability analysis, recommendations, a Streamlit dashboard, and a FastAPI backend.

## Features

- **Data Ingestion:** Load CSV data into a MySQL database.
- **Preprocessing:** Clean, impute, and prepare data for analysis.
- **EDA:** Generate statistical summaries and visualizations.
- **Forecasting:** Predict future sales using Facebook Prophet.
- **Profitability Analysis:** Assess business profitability.
- **Recommendations:** Generate business recommendations based on forecasts.
- **Dashboard:** Interactive analytics dashboard with Streamlit.
- **API:** REST endpoints for forecasts and recommendations via FastAPI.

## Project Structure
.
├── api.py
├── app.py
├── data/
│   └── train.csv
├── recommendations.txt
├── requirements.txt
├── Dockerfile
├── src/
│   ├── data_ingestion.py
│   ├── eda.py
│   ├── forecasting.py
│   ├── preprocessing.py
│   ├── profitability.py
│   └── recommendations.py
└── ...

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd data_analytics_project
```

### 2. Install Dependencies

```bash
python -m venv analytics_env
analytics_env\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory with the following variables:

```bash
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=localhost
MYSQL_DB=analytics_db
```

### 4. ### Prepare the Database
- Ensure MySQL is running.
- Create the database if it doesn't exist:

```bash
CREATE DATABASE analytics_db;
``` 
### Run the Pipeline 
 a. Data Ingestion
 ```bash
python src/data_ingestion.py
```
b. Preprocessing
```bash
python src/preprocessing.py
```
c. EDA
```bash
python src/eda.py
```
d. Forecasting
```bash
python src/forecasting.py
```
e. Profitability Analysis
```bash
python src/profitability.py
```
f. Recommendations
```bash
python src/recommendations.py
```
g. Streamlit Dashboard
```bash
streamlit run app.py
```
h. FastAPI Backend
```bash
uvicorn api:app --reload
``` 
## Docker Usage
To build and run the project with Docker:
```bash
docker build -t analytics_project .
docker run -p 8000:8000 analytics_project
```
## License
This project is licensed under the MIT License.
Note:

- Make sure your MySQL server is running and accessible.
- Update the .env file with your actual credentials.
- For any issues, check the logs or open an issue in the repository.
