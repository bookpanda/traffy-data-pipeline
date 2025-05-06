# traffy-data-pipeline

## Prerequisites

Download these tools before you start working on the project.

- python 3.12
- poetry
- `Black Formatter` VSCode extension (also set format on save, and set as default formatter for python in `settings.json`)

## Jar files for Spark

On the `Files` row in the website, click on the `jar` file to download it.

- [commons-pool2-2.12.0.jar](https://mvnrepository.com/artifact/org.apache.commons/commons-pool2/2.12.0)
- [kafka-clients-3.5.0.jar](https://mvnrepository.com/artifact/org.apache.kafka/kafka-clients/3.5.0)
- [spark-token-provider-kafka-0-10_2.12-3.5.0.jar](https://mvnrepository.com/artifact/org.apache.spark/spark-sql-kafka-0-10_2.12/3.5.0)
- [spark-token-provider-kafka-0-10_2.12-3.5.0.jar](https://mvnrepository.com/artifact/org.apache.spark/spark-token-provider-kafka-0-10_2.12/3.5.0)
- [postgresql-42.7.3.jar](https://mvnrepository.com/artifact/org.postgresql/postgresql/42.7.3)
- [elasticsearch-spark-20_2.12-8.18.0.jar](https://mvnrepository.com/artifact/org.elasticsearch/elasticsearch-spark-20_2.12/8.18.0)

Put these jar files in the `jars` folder in the root of the project. This is where the Spark job will look for the jar files.

## Setup

1. Run `poetry install` (to add packages do `poetry add <package>` and `poetry update` to update all packages)
2. Paste the `bangkok_traffy.csv` dataset into the `data` folder
3. Copy `.env.template` file in root of the folder as `.env` into the same directory fill in the values.
4. Run `poetry env activate` to activate the virtual environment
5. Run `poetry env info --path` to get the path of the virtual environment
6. In VSCode, `Ctrl + Shift + P` and type `Python: Select Interpreter`, select `Enter interpreter path...` and paste the path of the virtual environment. This will allow intellisense for the project
7. Run `docker-compose up` to start the Kafka container
8. Run `poetry run setup` to setup the pipeline
9. Run `poetry run stream` to start streaming data into the pipeline

## Components (flow from top to bottom)

1. Data stream: simulated using a Python script with Traffy Fondue dataset
2. Kafka: ingests data from stream
3. Spark: cleans and transforms data from Kafka
4. PostgreSQL/Elasticsearch database: stores cleaned data
5. Kibana: visualizes cleaned data + dashboards
6. AI/ML: trains on cleaned data, will be used for inferencing data from Kafka
7. Elasticsearch database: stores predictions
8. Predictions visualization + dashboards

- Data stream is simulated using a Python script feeding the Traffy Fondue dataset into Kafka
- Airflow will be used to orchestrate the data pipeline
