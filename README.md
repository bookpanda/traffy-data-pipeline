# traffy-data-pipeline

## Components (flow from top to bottom)
1. Data stream
2. Kafka
3. Spark
4. S3
5. AI/ML
6. S3

- Visualization will be done after component 2, 4, 6
- Data stream is simulated using a Python script feeding the Traffy Fondue dataset into Kafka 
- Airflow will be used to orchestrate the data pipeline