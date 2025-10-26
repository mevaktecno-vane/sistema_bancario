import pytest
from src.cuenta import Cuenta, SaldoInsuficienteError
from src.cliente import Cliente


def test_crear_cuenta():
    cliente = Cliente("Juan", "Perez", "11111111")
    cuenta = Cuenta("001", cliente)
    assert cuenta.get_nro_cuenta() == "001"
    assert cuenta.get_saldo() == 0.0


def test_deposito():
    cliente = Cliente("Ana", "Lopez", "33333333")
    cuenta = Cuenta("002", cliente)
    cuenta.depositar(100)
    assert cuenta.get_saldo() == 100


def test_retiro_exitoso():
    cliente = Cliente("Pedro", "Gomez", "22222222")
    cuenta = Cuenta("003", cliente, saldo=200)
    cuenta.retirar(100)
    assert cuenta.get_saldo() == 100


def test_saldo_insuficiente():
    cliente = Cliente("Lucia", "Martinez", "44444444")
    cuenta = Cuenta("004", cliente, saldo=50)
    with pytest.raises(SaldoInsuficienteError):
        cuenta.retirar(100)
