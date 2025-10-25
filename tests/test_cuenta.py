import pytest
from src.cuenta import Cuenta, SaldoInsuficienteError
from src.cliente import Cliente


def test_crear_cuenta():
    cliente = Cliente("Juan", "Perez", "11111111")
    cuenta = Cuenta("001", cliente)
    assert cuenta.nro_cuenta == "001"
    assert cuenta.saldo == 0.0
    assert cuenta.cliente == cliente


def test_deposito():
    cliente = Cliente("Ana", "Lopez", "33333333")
    cuenta = Cuenta("002", cliente)
    cuenta.depositar(100)
    assert cuenta.saldo == 100


def test_saldo_insuficiente():
    cliente = Cliente("Pedro", "Gomez", "22222222")
    cuenta = Cuenta("003", cliente, saldo=10.0)
    with pytest.raises(SaldoInsuficienteError):
        cuenta.retirar(50)
