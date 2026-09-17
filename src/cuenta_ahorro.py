from src.cuenta import Cuenta


class CuentaAhorro(Cuenta):
    def __init__(self, nro_cuenta: str, cliente, saldo: float = 0.0, interes: float = 1.0):
        super().__init__(nro_cuenta, cliente, saldo)
        if interes < 0:
            raise ValueError("La tasa de interés no puede ser negativa.")
        self.__interes = float(interes)

    def get_interes(self):
        return self.__interes

    def aplicar_interes(self):
        """Aplica el interés y lo acredita usando la logica de depósito."""
        saldo_actual = self.get_saldo()
        interes_ganado = saldo_actual * (self.__interes / 100)
        if interes_ganado > 0:
            # Pasa 'pagoIntereses' para que coincida con el catálogo de tipo_transaccion de la BD
            self.depositar(interes_ganado, tipo_transaccion="pagoIntereses")
        return self.get_saldo()
       