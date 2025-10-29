from datetime import datetime


class LimiteExcedidoError(Exception):
    """Excepción personalizada para límite de crédito excedido."""
    pass


class Tarjeta:
    def __init__(self, numero: str, cliente, limite: float = 10000.0):
        # === VALIDACIONES ===
        if not numero:
            raise ValueError("El número de tarjeta no puede estar vacío.")
        if not isinstance(limite, (int, float)):
            raise TypeError("El límite debe ser un valor numérico.")
        if limite <= 0:
            raise ValueError("El límite debe ser mayor a cero.")

        # === ATRIBUTOS PRIVADOS ===
        self.__numero = numero
        self.__cliente = cliente
        self.__limite = limite
        self.__saldo_actual = 0.0
        self.__movimientos = []  # [(fecha, monto, tipo)]

    # === MÉTODOS GETTERS ===
    def get_numero(self):
        return self.__numero

    def get_limite(self):
        return self.__limite

    def get_saldo_actual(self):
        return self.__saldo_actual

    def get_movimientos(self):
        # Devuelve una copia de los movimientos para mantener encapsulamiento
        return list(self.__movimientos)

    # === OPERACIONES ===
    def realizar_compra(self, monto: float):
        if not isinstance(monto, (int, float)):
            raise TypeError("El monto de la compra debe ser numérico.")
        if monto <= 0:
            raise ValueError("El monto de la compra debe ser mayor a cero.")
        if self.__saldo_actual + monto > self.__limite:
            raise LimiteExcedidoError("Se excede el límite de crédito.")

        self.__saldo_actual += monto
        self.__movimientos.append((datetime.now(), monto, "Compra"))

    def pagar_tarjeta(self, monto: float):
        if not isinstance(monto, (int, float)):
            raise TypeError("El monto del pago debe ser numérico.")
        if monto <= 0:
            raise ValueError("El monto del pago debe ser mayor a cero.")

        self.__saldo_actual -= monto
        self.__movimientos.append((datetime.now(), monto, "Pago"))

    def __str__(self):
        return (
            f"Tarjeta {self.__numero} - "
            f"Cliente: {self.__cliente.get_nombre()} {self.__cliente.get_apellido()} - "
            f"Saldo actual: ${self.__saldo_actual:.2f} / Límite: ${self.__limite:.2f}"
        )
