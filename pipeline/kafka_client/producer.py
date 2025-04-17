from kafka import KafkaProducer

from pipeline.config import settings

_producer = None


def get_producer() -> KafkaProducer:
    global _producer
    if _producer is None:
        print(f"Creating Kafka producer at {settings.KAFKA_BROKER_URL}")
        _producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BROKER_URL,
            value_serializer=lambda v: str(v).encode("utf-8"),
        )
    return _producer


def send_message(topic: str, message: str):
    producer = get_producer()
    producer.send(topic, value=message)
    producer.flush()
    print(f"Message sent to topic {topic}: {message}")
