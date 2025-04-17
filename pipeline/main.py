from pipeline.kafka_client import consume_messages


def main():
    print("Starting setup...")
    # get_producer()
    # print("Kafka producer initialized.")
    consume_messages("raw_data")


if __name__ == "__main__":
    main()
