# 🌦️ Weather Data ETL Pipeline

This project is an end-to-end **ETL (Extract, Transform, Load)** pipeline for fetching, cleaning, and storing real-time weather data from public APIs: Open Meteo. It automates the collection of weather metrics for further analysis or integration into other applications.

---

## 📌 Features

- 🌐 **Extract**: Fetches real-time weather data from a public API (e.g., OpenWeatherMap)
- 🧹 **Transform**: Cleans and standardizes the data (e.g., temperature units, timestamp formatting)
- 💾 **Load**: Stores the processed data into a local or cloud-based relational database (e.g., PostgreSQL)
- 🕒 **Scheduled Runs**: Supports scheduled/automated ETL jobs (can be extended using Airflow or Cron)
- 📊 **Scalable Foundation**: Ideal for building dashboards or analytics pipelines on top

---

## 🛠️ Tech Stack

- **Python 3.x**
- **Requests / HTTPx** – for API calls
- **Pandas** – for data transformation
- **SQLAlchemy / psycopg2** – for database interaction
- **PostgreSQL / SQLite** – as the storage backend
- *(Optional: Airflow / Cron for scheduling)*

---
