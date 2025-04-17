from kafka import KafkaConsumer

from pipeline.config import settings

_consumer = None


def get_consumer(topic: str) -> KafkaConsumer:
    global _consumer
    if _consumer is None:
        print(f"Creating Kafka consumer at {settings.KAFKA_BROKER_URL}")
        _consumer = KafkaConsumer(
            topic,
            bootstrap_servers=settings.KAFKA_BROKER_URL,
            auto_offset_reset="earliest",  # or "latest"
            enable_auto_commit=True,
            group_id="my-consumer-group",
            value_deserializer=lambda v: v.decode("utf-8"),
        )
    return _consumer


def consume_messages(topic: str):
    consumer = get_consumer(topic)
    print(f"Consuming from topic: {topic}")
    for message in consumer:
        print(f"Received message: {message.value}")
