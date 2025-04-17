import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    STREAM_INGESTION_RATE: int = int(os.getenv("STREAM_INGESTION_RATE", 10))
    KAFKA_BROKER_URL: str = os.getenv("KAFKA_BROKER_URL", "localhost:9092")
    POSTGRES_URL: str = os.getenv(
        "POSTGRES_URL", "jdbc:postgresql://localhost:5432/messenger_db"
    )
    POSTGRES_TABLE: str = os.getenv("POSTGRES_TABLE", "your_table_name")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "root")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")


settings = Settings()
