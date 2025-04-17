# traffy-data-pipeline

## Prerequisites

Download these tools before you start working on the project.

- python 3.12
- poetry
- `Black Formatter` VSCode extension (also set format on save, and set as default formatter for python in `settings.json`)

## Setup

1. Run `poetry install` (to add packages do `poetry add <package>` and `poetry update` to update all packages)
2. Paste the `bangkok_traffy.csv` dataset into the `data` folder
3. Copy `.env.template` file in root of the folder as `.env` into the same directory fill in the values.
4. Run `poetry env activate` to activate the virtual environment
5. Run `poetry env info --path` to get the path of the virtual environment
6. In VSCode, `Ctrl + Shift + P` and type `Python: Select Interpreter`, select `Enter interpreter path...` and paste the path of the virtual environment. This will allow intellisense for the project
7. Run `docker-compose up` to start the Kafka container
8. Run `poetry run python pipeline/main.py` to start the application

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
