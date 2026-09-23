from src.transaccion import Transaccion


class SaldoInsuficienteError(Exception):
    """Excepción personalizada para saldo insuficiente."""
    pass


class Cuenta:
    def __init__(self, nro_cuenta: str, cliente, saldo: float = 0.0, id_cuenta: int = None, dao=None):
        if not nro_cuenta or not isinstance(nro_cuenta, str):
            raise ValueError("El número de cuenta debe ser una cadena no vacía.")
        if saldo < 0:
            raise ValueError("El saldo inicial no puede ser negativo.")
        if cliente is None:
            raise ValueError("Debe asignarse un cliente válido a la cuenta.")

        self.__nro_cuenta = nro_cuenta
        self.__cliente = cliente
        self.__saldo = float(saldo)
        self.__transacciones = []
        self._id_cuenta = id_cuenta
        self._dao = dao

    # Getters y Setters
    def get_nro_cuenta(self):
        return self.__nro_cuenta

    def get_saldo(self):
        return self.__saldo

    def get_cliente(self):
        return self.__cliente

    def get_transacciones(self):
        return self.__transacciones

    def get_id_cuenta(self):
        return self._id_cuenta

    def set_id_cuenta(self, id_cuenta: int):
        self._id_cuenta = id_cuenta

    def set_dao(self, dao):
        """Asocia el DAO para permitir la persistencia en la base de datos."""
        self._dao = dao

    def sincronizar_id_desde_db(self):
        """Si no tiene id_cuenta pero tiene DAO, consulta el ID por su número."""
        if self._dao and not self._id_cuenta:
            cuenta_bd = self._dao.obtener_cuenta_por_numero(self.__nro_cuenta)
            if cuenta_bd:
                self._id_cuenta = cuenta_bd[0]

    # Operaciones
    def depositar(self, monto: float, tipo_transaccion: str = "deposito"):
        """Agrega dinero a la cuenta y persiste si hay DAO vinculado."""
        if not isinstance(monto, (int, float)):
            raise TypeError("El monto del depósito debe ser un número.")
        if monto <= 0:
            raise ValueError("El monto del depósito debe ser mayor a cero.")

        self.__saldo += monto
        transaccion = Transaccion(tipo_transaccion, monto)
        self.__transacciones.append(transaccion)

        # Persistencia en BD
        if self._dao:
            self.sincronizar_id_desde_db()
            if self._id_cuenta:
                self._dao.actualizar_saldo_cuenta(self._id_cuenta, self.__saldo)
                self._dao.guardar_transaccion(self._id_cuenta, tipo_transaccion, monto)

        return self.__saldo

    def retirar(self, monto: float, tipo_transaccion: str = "retiro"):
        """Retira dinero si hay saldo suficiente y persiste si hay DAO vinculado."""
        if not isinstance(monto, (int, float)):
            raise TypeError("El monto del retiro debe ser un número.")
        if monto <= 0:
            raise ValueError("El monto del retiro debe ser mayor a cero.")
        if monto > self.__saldo:
            raise SaldoInsuficienteError("Saldo insuficiente para realizar el retiro.")

        self.__saldo -= monto
        transaccion = Transaccion(tipo_transaccion, monto)
        self.__transacciones.append(transaccion)

        # Persistencia en BD
        if self._dao:
            self.sincronizar_id_desde_db()
            if self._id_cuenta:
                self._dao.actualizar_saldo_cuenta(self._id_cuenta, self.__saldo)
                self._dao.guardar_transaccion(self._id_cuenta, tipo_transaccion, monto)

        return self.__saldo

    def mostrar_transacciones(self):
        if not self.__transacciones:
            return ["No hay transacciones registradas."]
        return [str(t) for t in self.__transacciones]