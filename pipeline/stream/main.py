import time

import pandas as pd

from pipeline.config import settings
from pipeline.kafka_client import send_message

# df = pd.read_csv("./data/bangkok_traffy.csv")
df = pd.read_csv("./data/bangkok_traffy_mini.csv")

sleep_time = 1 / settings.STREAM_INGESTION_RATE


# 500 rows/s = 1600s
def main():
    print(f"stream size {len(df)}")

    for index, row in df.iterrows():
        message = row.to_json()
        send_message("raw_data", message)

        time.sleep(sleep_time)


if __name__ == "__main__":
    main()
