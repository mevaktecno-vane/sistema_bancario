from datetime import datetime


class Transaccion:
    def __init__(self, tipo: str, monto: float):
        # Validar tipo
        if tipo not in ["deposito", "retiro"]:
            raise ValueError("Tipo de transacción inválido")
        # Validar monto
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")

        # Asignar atributos
        self.tipo = tipo
        self.monto = monto
        self.fecha = datetime.now()

    def __str__(self):
        return f"{self.fecha.strftime('%Y-%m-%d %H:%M:%S')} - {self.tipo}: ${self.monto:.2f}"
