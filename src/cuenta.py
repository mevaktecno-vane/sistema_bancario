from src.transaccion import Transaccion


class SaldoInsuficienteError(Exception):
    """Excepción personalizada para saldo insuficiente."""
    pass


class Cuenta:
    def __init__(self, nro_cuenta: str, cliente, saldo: float = 0.0):
        if not nro_cuenta:
            raise ValueError("El número de cuenta no puede estar vacío.")
        if saldo < 0:
            raise ValueError("El saldo inicial no puede ser negativo.")

        self.__nro_cuenta = nro_cuenta
        self.__cliente = cliente
        self.__saldo = saldo
        self.__transacciones = []

    # Métodos getters
    def get_nro_cuenta(self):
        return self.__nro_cuenta

    def get_saldo(self):
        return self.__saldo

    def get_cliente(self):
        return self.__cliente

    # Operaciones
    def depositar(self, monto: float):
        if not isinstance(monto, (int, float)):
            raise TypeError("El monto del deposito debe ser un número.")
        if monto <= 0:
            raise ValueError("El monto del deposito debe ser mayor a cero.")
        self.__saldo += monto
        self.__transacciones.append(Transaccion("deposito", monto))

    def retirar(self, monto: float):
        if not isinstance(monto, (int, float)):
            raise TypeError("El monto del retiro debe ser un número.")
        if monto <= 0:
            raise ValueError("El monto del retiro debe ser mayor a cero.")
        if monto > self.__saldo:
            raise SaldoInsuficienteError(
                "Saldo insuficiente para realizar el retiro.")
        self.__saldo -= monto
        self.__transacciones.append(Transaccion("retiro", monto))

    def mostrar_transacciones(self):
        return [str(t) for t in self.__transacciones]

    def get_transacciones(self): 
        return self.__transacciones