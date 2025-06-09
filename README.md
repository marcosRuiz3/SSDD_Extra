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

## Execution

To run the template server, just install the package and run

```
ssdd-calculator --Ice.Config=config/calculator.config
```

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
