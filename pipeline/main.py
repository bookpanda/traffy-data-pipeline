from pipeline.airflow import main as airflow_main
from pipeline.spark import main as spark_main


def main():
    print("Starting setup...")
    # spark_main()
    airflow_main()


if __name__ == "__main__":
    main()
