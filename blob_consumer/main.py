from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

import json
import time

print("STARTING CONSUMER")
consumer = None

while consumer is None:

    try:
        consumer = KafkaConsumer(
            "user",
            bootstrap_servers="kafka:9092",
            auto_offset_reset="earliest",
            group_id="blob-consumers",
            value_deserializer=lambda m: json.loads(m.decode("utf-8"))
        )
        print("Connected to Kafka")

    except NoBrokersAvailable:
        print("Kafka not ready, retrying in 5 seconds...")
        time.sleep(5)

for message in consumer:
    print(message.value)