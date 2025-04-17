from pipeline.config import settings


def main():
    print(settings.KAFKA_BROKER_URL)
