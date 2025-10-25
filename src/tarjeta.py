from src.cliente import Cliente


class LimiteExcedidoError(Exception):
    """Excepción para cuando el monto supera el límite de crédito."""
    pass


class Tarjeta:
    def __init__(self, numero: str, cliente: Cliente, limite_credito: float):
        self.numero = numero
        self.cliente = cliente
        self.limite_credito = limite_credito
        self.saldo_disponible = limite_credito

    def comprar(self, monto: float):
        if monto > self.saldo_disponible:
            raise LimiteExcedidoError("Compra rechazada: límite excedido.")
        self.saldo_disponible -= monto

    def pagar(self, monto: float):
        if monto <= 0:
            raise ValueError("El monto del pago debe ser positivo.")
        nuevo_saldo = self.saldo_disponible + monto
        self.saldo_disponible = min(nuevo_saldo, self.limite_credito)

    def get_saldo_disponible(self):
        return self.saldo_disponible

    def get_limite_credito(self):
        return self.limite_credito
