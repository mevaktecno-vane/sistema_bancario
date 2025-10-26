from datetime import datetime


class Transaccion:
    def __init__(self, tipo: str, monto: float):
        # Validar tipo
        if tipo not in ["deposito", "retiro"]:
            raise ValueError("Tipo de transacción inválido")

        if monto <= 0:
            raise ValueError("El monto debe ser mayor a cero.")

        self.__tipo = tipo
        self.__monto = monto
        self.__fecha = datetime.now()

    # Métodos getters
    def get_tipo(self):
        return self.__tipo

    def get_monto(self):
        return self.__monto

    def get_fecha(self):
        return self.__fecha

    def __str__(self):
        return f"Transacción: {self.__tipo} - Monto: ${self.__monto:.2f} - Fecha: {self.__fecha.strftime('%Y-%m-%d %H:%M:%S')}"
