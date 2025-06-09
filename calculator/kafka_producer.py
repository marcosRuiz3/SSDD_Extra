from kafka import KafkaProducer
import json


producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def send_calculation_request(id, operation, op1, op2):
    """Envía una petición de cálculo al topic de Kafka."""
    request = {
        "id": id,
        "operation": operation,
        "args": {
            "op1": op1,
            "op2": op2
        }
    }
    
    producer.send("peticiones", request)
    print(f"Petición enviada: {request}")


