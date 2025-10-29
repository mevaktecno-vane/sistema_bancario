from datetime import datetime


class Transaccion:
    def __init__(self, tipo: str, monto: float):
        if tipo not in ["deposito", "retiro"]:
            raise ValueError("Tipo de transacción inválido")
        if not isinstance(monto, (int, float)):
            raise TypeError("El monto debe ser un número.")
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a cero.")

        self.__tipo = tipo
        self.__monto = monto
        self.__fecha = datetime.now()

    # Getters
    def get_tipo(self):
        return self.__tipo

    def get_monto(self):
        return self.__monto

    def get_fecha(self):
        return self.__fecha

    def __str__(self):
        return f"{self.__fecha.strftime('%Y-%m-%d %H:%M:%S')} - {self.__tipo}: ${self.__monto}"
