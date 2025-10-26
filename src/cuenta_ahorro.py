from src.cuenta import Cuenta


class CuentaAhorro(Cuenta):
    def __init__(self, nro_cuenta: str, cliente, saldo: float = 0.0, interes: float = 1.0):
        super().__init__(nro_cuenta, cliente, saldo)
        if interes < 0:
            raise ValueError("La tasa de interés no puede ser negativa.")
        self.__interes = interes

    def get_interes(self):
        return self.__interes

    def aplicar_interes(self):
        """Aplica el interés al saldo actual."""
        saldo_actual = self.get_saldo()
        nuevo_saldo = saldo_actual + (saldo_actual * self.__interes / 100)
        # Actualizamos el saldo internamente
        self._Cuenta__saldo = nuevo_saldo  # usamos el atributo protegido de la clase base
        return nuevo_saldo
