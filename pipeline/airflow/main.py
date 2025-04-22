from datetime import datetime

from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

from .message_count import MessageCountSensor


def main():
    with DAG("pipeline_control", start_date=datetime(2021, 1, 1), catchup=False) as dag:
        spark_task = SparkSubmitOperator(
            task_id="process_stream_data",
            application="./spark/main.py",
            conn_id="spark_default",
            conf={"spark.executor.memory": "2g", "spark.driver.memory": "1g"},
            # application_args=["--input", "s3://your-bucket/input-data"],
        )

        message_sensor = MessageCountSensor(
            task_id="wait_for_messages",
            threshold=10000,
            poke_interval=3,
            timeout=3600,
        )

    message_sensor >> spark_task
