from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
import requests
import json
from datetime import datetime, timedelta




latitude='51.5074'
longitude='-0.1278'
postgress_conn_id='postgres_default'
api_conn_id='open_meteo_api'

default_args = {
    'owner': 'airflow',
    'start_date': datetime.now() - timedelta(days=1)
}

#DAG
with DAG(dag_id='weather_etl_pipeline',
         default_args=default_args,
         schedule='@daily',
         catchup=False) as dag:
    
    @task()
    def extract_weather_data():
        '''Extract weather data from open-mateo api using airflow connection'''
        
        #use http hooks to get connection details from airflow connection
        
        http_hook=HttpHook(http_conn_id=api_conn_id,method='GET')
        
        #build API endpoint
        #http://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true
        endpoint=f'/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true'
        
        #Make the request via the http request
        response=http_hook.run(endpoint)
        
        if response.status_code==200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch weather data: {response.status_code}")
        
    
    @task()
    def transform_weather_data(weather_data):
        current_weather=weather_data['current_weather']
        transformed_data={
            'latitude':latitude,
            'longitude':longitude,
            'temperature':current_weather['temperature'],
            'windspeed':current_weather['windspeed'],
            'winddirection':current_weather['winddirection'],
            'weathercode':current_weather['weathercode']
        }
        return transformed_data
    
    @task
    def load_weather_data(transformed_data):
        pg_hook=PostgresHook(postgres_conn_id=postgress_conn_id)
        conn=pg_hook.get_conn()
        cursor=conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data(
            latitude float,
            longitude float,
            temperature float,
            windspeed float,
            winddirection float,
            weathercode int,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        cursor.execute("""
        INSERT INTO weather_data (longitude,latitude,temperature,windspeed,winddirection,weathercode)
        values(%s,%s,%s,%s,%s,%s);
        """,(
            transformed_data['latitude'],
            transformed_data['longitude'],
            transformed_data['temperature'],
            transformed_data['windspeed'],
            transformed_data['winddirection'],
            transformed_data['weathercode']
        ))
        
        conn.commit()
        cursor.close()
        
    ##DAG Workflow
    
    weather_data=extract_weather_data()
    transformed_data=transform_weather_data(weather_data)
    load_weather_data(transformed_data)
    

