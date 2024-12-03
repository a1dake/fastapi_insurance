from confluent_kafka import Producer, KafkaException, KafkaError
import json
from datetime import datetime

kafka_producer = Producer({'bootstrap.servers': 'localhost:9092'})

def log_action(user_id: int, action: str, timestamp: datetime):
    try:
        message = {
            "action": action,
            "timestamp": timestamp.isoformat(),
        }
        kafka_producer.produce(
            topic="rate_logs",
            key=str(user_id),
            value=json.dumps(message),
        )
        kafka_producer.flush()
        print("Message sent successfully")
    except KafkaException as e:
        print(f"Kafka error: {e}")
        if e.args[0].code() == KafkaError._ALL_BROKERS_DOWN:
            print("All brokers are down. Check Kafka server.")
