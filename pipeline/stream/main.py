import pandas as pd

from pipeline.kafka_client import send_message

# df = pd.read_csv("./data/bangkok_traffy.csv")


# 500 rows/s = 1600s
def main():
    # print(f"stream size {len(df)}")

    send_message("test_topic", "Hello, Kafka!")
