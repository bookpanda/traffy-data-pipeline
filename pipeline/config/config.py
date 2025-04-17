import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    STREAM_INGESTION_RATE: int = int(os.getenv("STREAM_INGESTION_RATE", 10))
    KAFKA_BROKER_URL: str = os.getenv("KAFKA_BROKER_URL", "localhost:9092")
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "")
    AWS_BUCKET_NAME: str = os.getenv("AWS_BUCKET_NAME", "")


settings = Settings()
