FROM astrocrpublic.azurecr.io/runtime:3.0-2

RUN airflow db migrate
RUN pip install apache-airflow
RUN pip install apache-airflow-providers-http
