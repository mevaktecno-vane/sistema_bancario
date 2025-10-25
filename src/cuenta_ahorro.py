from src.cuenta import Cuenta, SaldoInsuficienteError


class CuentaAhorro(Cuenta):
    def __init__(self, nro_cuenta: str, cliente, saldo: float = 0.0, tasa_interes: float = 0.01):
        super().__init__(nro_cuenta, cliente, saldo)
        self.tasa_interes = tasa_interes

    def aplicar_interes(self):
        interes = self.saldo * self.tasa_interes
        self.saldo += interes
        return interes
