from src.transaccion import Transaccion


class SaldoInsuficienteError(Exception):
    """Excepción personalizada para saldo insuficiente."""
    pass


class Cuenta:
    def __init__(self, nro_cuenta: str, cliente, saldo: float = 0.0, dao=None, id_cuenta: int = None):
        if not nro_cuenta or not isinstance(nro_cuenta, str):
            raise ValueError(
                "El número de cuenta debe ser una cadena no vacía.")
        if saldo < 0:
            raise ValueError("El saldo inicial no puede ser negativo.")
        if cliente is None:
            raise ValueError("Debe asignarse un cliente válido a la cuenta.")

        self.__nro_cuenta = nro_cuenta
        self.__cliente = cliente
        self.__saldo = float(saldo)
        self.__transacciones = []
        self._dao = dao
        self._id_cuenta = id_cuenta

        # Si se pasó el DAO pero no el id_cuenta, intentamos resolver el id por nro_cuenta
        if self._dao and self._id_cuenta is None:
            cuenta_bd = self._dao.obtener_cuenta_por_numero(self.__nro_cuenta)
            if cuenta_bd:
                # cuenta_bd puede ser un objeto modelo o una tupla según el DAO
                self._id_cuenta = getattr(cuenta_bd, "id_cuenta", cuenta_bd[0] if isinstance(cuenta_bd, (tuple, list)) else None)

    # Métodos getters
    def get_nro_cuenta(self):
        return self.__nro_cuenta

    def get_saldo(self):
        return self.__saldo

    def get_cliente(self):
        return self.__cliente

    def get_transacciones(self):
        return self.__transacciones

    def set_dao(self, dao, id_cuenta: int = None):
        """Asocia el DAO a la cuenta posteriormente si no fue inyectado en el constructor."""
        self._dao = dao
        if id_cuenta is not None:
            self._id_cuenta = id_cuenta
        elif self._dao:
            cuenta_bd = self._dao.obtener_cuenta_por_numero(self.__nro_cuenta)
            if cuenta_bd:
                self._id_cuenta = getattr(cuenta_bd, "id_cuenta", cuenta_bd[0] if isinstance(cuenta_bd, (tuple, list)) else None)

    # Operaciones
    def depositar(self, monto: float, tipo_transaccion: str = "deposito"):
        """Agrega dinero a la cuenta y retorna el saldo actualizado"""
        if not isinstance(monto, (int, float)):
            raise TypeError("El monto del depósito debe ser un número.")
        if monto <= 0:
            raise ValueError("El monto del depósito debe ser mayor a cero.")

        self.__saldo += float(monto)
        self.__transacciones.append(Transaccion(tipo_transaccion, monto))

        # Persistencia en base de datos si el DAO está configurado
        if self._dao and self._id_cuenta:
            self._dao.actualizar_saldo_cuenta(self._id_cuenta, self.__saldo)
            self._dao.guardar_transaccion(self._id_cuenta, tipo_transaccion, float(monto))

        return self.__saldo

    def retirar(self, monto: float):
        """Retira dinero de la cuenta si hay saldo suficiente y retorna el saldo actualizado."""
        if not isinstance(monto, (int, float)):
            raise TypeError("El monto del retiro debe ser un número.")
        if monto <= 0:
            raise ValueError("El monto del retiro debe ser mayor a cero.")
        if monto > self.__saldo:
            raise SaldoInsuficienteError(
                "Saldo insuficiente para realizar el retiro.")
        
        self.__saldo -= float(monto)
        self.__transacciones.append(Transaccion("retiro", monto))

        # Persistencia en base de datos si el DAO está configurado
        if self._dao and self._id_cuenta:
            self._dao.actualizar_saldo_cuenta(self._id_cuenta, self.__saldo)
            self._dao.guardar_transaccion(self._id_cuenta, "retiro", float(monto))

        return self.__saldo


    def mostrar_transacciones(self):
        """Devuelve una lista legible de las transacciones realizadas."""
        if not self.__transacciones:
            return ["No hay transacciones registradas."]
        return [str(t) for t in self.__transacciones]
