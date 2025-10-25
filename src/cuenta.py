from src.cliente import Cliente
from src.transaccion import Transaccion


class SaldoInsuficienteError(Exception):
    pass


class Cuenta:
    def __init__(self, nro_cuenta: str, cliente: Cliente, saldo: float = 0.0):
        # Los atributos se llaman como los espera el test
        self.nro_cuenta = nro_cuenta
        self.cliente = cliente
        self.saldo = saldo
        self.transacciones = []

    def depositar(self, monto: float):
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        self.saldo += monto
        self.transacciones.append(Transaccion("deposito", monto))

    def retirar(self, monto: float):
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        if monto > self.saldo:
            raise SaldoInsuficienteError("Saldo insuficiente")
        self.saldo -= monto
        self.transacciones.append(Transaccion("retiro", monto))

    def obtener_historial(self):
        return self.transacciones
