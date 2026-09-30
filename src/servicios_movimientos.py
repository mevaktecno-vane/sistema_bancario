class ServiciosMovimientos:
    def __init__(self, dao_cuenta, dao_transaccion):
        self.dao_cuenta = dao_cuenta
        self.dao_transaccion = dao_transaccion

    def depositar(self, cuenta, monto: float, tipo: str = "deposito"):
        # 1. Regla de negocio y validación en entidad (actualiza saldo en memoria)
        cuenta.depositar(monto, tipo=tipo)

        # 2. Persistencia del nuevo saldo consultando el getter
        id_cuenta = cuenta.get_id_cuenta()
        self.dao_cuenta.actualizar_saldo_cuenta(id_cuenta, cuenta.get_saldo())

        # 3. Registro auditable de la transacción en la BD
        self.dao_transaccion.guardar_transaccion(id_cuenta, tipo, monto)
        return True

    def retirar(self, cuenta, monto: float, tipo: str = "retiro"):
        # 1. Regla de negocio en entidad (valida saldo y resta en memoria)
        cuenta.retirar(monto, tipo=tipo)

        # 2. Persistencia del nuevo saldo consultando el getter
        id_cuenta = cuenta.get_id_cuenta()
        self.dao_cuenta.actualizar_saldo_cuenta(id_cuenta, cuenta.get_saldo())

        # 3. Registro auditable de la transacción en la BD
        self.dao_transaccion.guardar_transaccion(id_cuenta, tipo, monto)
        return True