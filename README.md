# calculator repository template

Template for the extra SSDD laboratory 2024-2025.
Este proyecto sigue la plantilla original de SSDD, con modificaciones en los archivos `.py` para cumplir los requisitos del enunciado.

## Cambios realizados  
- Se han completado los métodos en `server.py` que actuará como consumidor y enviará las respuesta a las peticiones al topic de "respuestas"; y otros módulos como `calculator.py`, que tiene el metodo que procesa una petición JSON de Kafka y ejecuta la operación correspondiente. .
- Se ha añadido `kafka_producer.py` para la comunicación con Kafka. 

## Installation

To locally install the package, just run

```
pip install .
```

Or, if you want to modify it during your development,

```
pip install -e .
```
## Configuración de Zookeeper y Kafka  

Para que Kafka funcione correctamente, primero se debe iniciar Zookeeper y luego el broker Kafka.  

### **Inicio de Zookeeper y Kafka**  

Ejecutar los siguientes comandos en la terminal:  
```
~/TU_RUTA/kafka/bin/zookeeper-server-start.sh ~/Escritorio/kafka/config/zookeeper.properties &
~/TU_RUTA/kafka/bin/kafka-server-start.sh ~/Escritorio/kafka/config/server.properties &
```

Verifica que Kafka esta corriendo: 
```
nc -zv localhost 9092
```

`TU_RUTA` es el directorio donde tienes instalado kafka

## Creación de Topics

El servicio usa los topics `peticiones` y `respuestas`, que deben crearse antes de ejecutar el servidor:

```
~/TU_RUTA/kafka/bin/kafka-topics.sh --create --topic peticiones --bootstrap-server localhost:9092
~/TU_RUTA/kafka/bin/kafka-topics.sh --create --topic respuestas --bootstrap-server localhost:9092
```


## Execution

To run the template server, just install the package and run

```
ssdd-calculator --Ice.Config=config/calculator.config
```

1º Ahora podremos ejecutar ```python3 kafka_producer.py``` para cargar el código y asegurarnos de que el productor Kafka está listo para enviar mensajes.

2º Una vez hecho esto abrimos un script de python con el comando `python3` 

3º ```>>> from kafka import KafkaProducer``` y enviamos el mensaje. por ejemplo ```>>> send_calculation_request("op1", "sum", 5.0, 10.0)```

4º Para comprobar que todo funciona correctamente y poder ver el contenido de los topics para ver los mensajes JSON enviados y recibidos, ejecuta:

Para ver las peticiones...
```
~/TU_RUTA/kafka/bin/kafka-console-consumer.sh --topic peticiones --bootstrap-server localhost:9092 --from-beginning

```
Mi ejemplo: {"id": "op1", "operation": "sum", "args": {"op1": 5.0, "op2": 10.0}}

Para ver las respuestas...
```
~/TU_RUTA/kafka/bin/kafka-console-consumer.sh --topic respuestas --bootstrap-server localhost:9092 --from-beginning

```
Mi ejemplo: "{\"id\": \"op1\", \"status\": true, \"result\": 15.0}"


## Configuration

This template only allows to configure the server endpoint. To do so, you need to modify
the file `config/calculator.config` and change the existing line.

For example, if you want to make your server to listen always in the same TCP port, your file
should look like

```
calculator.Endpoints=tcp -p 10000
```

## Slice usage

The Slice file is provided inside the `calculator` directory. It is only loaded once when the `calculator`
package is loaded by Python. It makes your life much easier, as you don't need to load the Slice in every module
or submodule that you define.

The code loading the Slice is inside the `__init__.py` file.
