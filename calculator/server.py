"""Calculator server application with Kafka integration."""

import logging
import json
import Ice
from kafka import KafkaConsumer, KafkaProducer
from calculator.calculator import Calculator, process_request  # Importamos la función procesadora

class Server(Ice.Application):
    """Ice.Application for the server with Kafka support."""

    def __init__(self) -> None:
        """Initialise the Server objects."""
        super().__init__()
        self.logger = logging.getLogger(__file__)

    def run(self, args: list[str]) -> int:
        """Execute the main server actions.

        It will initialise the needed middleware elements in order to execute the server and
        consume messages from Kafka.
        """
        servant = Calculator()
        adapter = self.communicator().createObjectAdapter("calculator")
        proxy = adapter.add(servant, self.communicator().stringToIdentity("calculator"))
        self.logger.info('Proxy: "%s"', proxy)

        adapter.activate()
        self.shutdownOnInterrupt()

        # Configuramos el Kafka Consumer para recibir peticiones
        consumer = KafkaConsumer(
            "peticiones",
            bootstrap_servers="localhost:9092",
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            
        )


        # Configuramos el Kafka Producer para enviar respuestas al topic de respuestas
        producer = KafkaProducer(
            bootstrap_servers="localhost:9092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

        self.logger.info("Kafka Consumer iniciado. Escuchando el topic 'peticiones'...")

        # Procesamos mensajes en Kafka utilizando `process_request()` de `calculator.py`
        for message in consumer:
            self.logger.info(f"Mensaje recibido: {message.value}")
            
            try:
                response = process_request(json.dumps(message.value))  # Llamada a `process_request()` de la caluladora
            except Exception as e:
                response = json.dumps({"status": False, "error": str(e)})

            self.logger.info(f"Respuesta enviada: {response}")
            producer.send("respuestas", response)  # Enviamos respuesta al topic de Kafka correspondiente

        self.communicator().waitForShutdown()
        return 0
