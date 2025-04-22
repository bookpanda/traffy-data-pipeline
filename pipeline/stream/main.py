import math
import time

import pandas as pd
from tqdm import tqdm

from pipeline.config import settings
from pipeline.kafka_client import send_message

# df = pd.read_csv("./data/bangkok_traffy.csv")
df = pd.read_csv("./data/bangkok_traffy_mini.csv")

sleep_time = 1 / settings.STREAM_INGESTION_RATE


def handle_nan(data):
    """replace NaN with None (to be treated as null in Avro)"""
    return {
        key: (None if isinstance(value, float) and math.isnan(value) else value)
        for key, value in data.items()
    }


count = 0


def get_count():
    return count


def decrease_count_by(amount: int):
    global count
    count -= amount
    if count < 0:
        count = 0


# 500 rows/s = 1600s
def main():
    print(f"stream size {len(df)}")

    for index, row in tqdm(df.iterrows()):
        data = row.to_dict()
        data = handle_nan(data)
        send_message("raw_data", data)
        count += 1

        time.sleep(sleep_time)


if __name__ == "__main__":
    main()
