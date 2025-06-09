"""Calculator implementation."""

import Ice
import json
import RemoteCalculator


class Calculator(RemoteCalculator.Calculator):
    """Implementación del servicio de calculadora remota."""

    def sum(self, a: float, b: float) -> float:
        return a + b

    def sub(self, a: float, b: float) -> float:
        return a - b

    def mult(self, a: float, b: float) -> float:
        return a * b

    def div(self, a: float, b: float) -> float:
        if b == 0:
            raise RemoteCalculator.ZeroDivisionError()
        return a / b


def process_request(json_message: str) -> str:
    """Procesa una petición JSON de Kafka y ejecuta la operación correspondiente."""
    try:
        request = json.loads(json_message)
        operation = request["operation"]
        operands = request["args"]
        calculator = Calculator()

        if operation == "sum":
            result = calculator.sum(operands["op1"], operands["op2"])
        elif operation == "sub":
            result = calculator.sub(operands["op1"], operands["op2"])
        elif operation == "mult":
            result = calculator.mult(operands["op1"], operands["op2"])
        elif operation == "div":
            try:
                result = calculator.div(operands["op1"], operands["op2"])
            except RemoteCalculator.ZeroDivisionError:
                return json.dumps({"id": request["id"], "status": False, "error": "Division by zero"})
        else:
            return json.dumps({"id": request["id"], "status": False, "error": "Operation not found"})

        return json.dumps({"id": request["id"], "status": True, "result": result})

    except KeyError:
        return json.dumps({"status": False, "error": "Invalid request format"})

