from datetime import datetime


class LimiteExcedidoError(Exception):
    """Excepción personalizada para límite de crédito excedido."""
    pass


class Tarjeta:
    def __init__(self, numero: str, cliente, limite: float = 10000.0):
        if not numero:
            raise ValueError("El número de tarjeta no puede estar vacío.")
        if limite <= 0:
            raise ValueError("El límite debe ser mayor a cero.")

        self.__numero = numero
        self.__cliente = cliente
        self.__limite = limite
        self.__saldo_actual = 0.0
        self.__movimientos = []

    # Métodos getters
    def get_numero(self):
        return self.__numero

    def get_limite(self):
        return self.__limite

    def get_saldo_actual(self):
        return self.__saldo_actual

    def get_movimientos(self):
        return self.__movimientos

    # Operaciones
    def realizar_compra(self, monto: float):
        if monto <= 0:
            raise ValueError("El monto de la compra debe ser mayor a cero.")
        if self.__saldo_actual + monto > self.__limite:
            raise LimiteExcedidoError("Se excede el límite de crédito.")
        self.__saldo_actual += monto
        self.__movimientos.append((datetime.now(), monto, "Compra"))

    def pagar_tarjeta(self, monto: float):
        if monto <= 0:
            raise ValueError("El monto del pago debe ser mayor a cero.")
        self.__saldo_actual -= monto
        self.__movimientos.append((datetime.now(), monto, "Pago"))

    def __str__(self):
        return f"Tarjeta {self.__numero} - Cliente: {self.__cliente.get_nombre()} {self.__cliente.get_apellido()}"
