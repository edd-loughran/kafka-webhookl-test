from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from db_repositories.user_repository import UserRepository
from models.db import SessionLocal

import json
import time

print("STARTING CONSUMER")
consumer = None

while consumer is None:

    try:
        consumer = KafkaConsumer(
            "webhooks",
            bootstrap_servers="kafka:9092",
            auto_offset_reset="earliest",
            group_id="db-consumers",
            value_deserializer=lambda m: json.loads(m.decode("utf-8"))
        )
        print("Connected to Kafka")

    except NoBrokersAvailable:
        print("Kafka not ready, retrying in 5 seconds...")
        time.sleep(5)

for message in consumer:
    print(message.value)
    db = SessionLocal()
    repo = UserRepository(db)
    repo.upsert_user(
        email=message.value["email"],
        username=message.value["username"],
        hashed_password=message.value["hashed_password"]
    )
    print(f"Updated user: {message.value["email"]}")

    db.commit()
    db.close()