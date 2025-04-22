from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

from pipeline.spark import main as spark_main

from .message_count import MessageCountSensor


def main():
    with DAG("pipeline_control", start_date=datetime(2021, 1, 1), catchup=False) as dag:
        trigger_spark = PythonOperator(
            task_id="trigger_spark_job",
            python_callable=spark_main,
        )

        message_sensor = MessageCountSensor(
            task_id="wait_for_messages",
            threshold=10000,
            poke_interval=3,
            timeout=3600,
        )

    message_sensor >> trigger_spark
