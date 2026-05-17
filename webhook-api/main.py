from fastapi import FastAPI, Request
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

import json
import time

app = FastAPI()

producer = None

while producer is None:

    try:
        producer = KafkaProducer(
            bootstrap_servers="kafka:9092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

        print("Connected to Kafka")

    except NoBrokersAvailable:
        print("Kafka not ready, retrying in 5 seconds...")
        time.sleep(5)

@app.get("/")
def healthcheck():
    return {"status": "running"}

@app.post("/user")
async def webhook(request: Request):
    payload = await request.json()
    key = payload.get("email")
    producer.send(
        "user",
        value=payload,
        key=key.encode("utf-8") if key else None,
    )
    producer.flush()
    return {"status": "message sent"}