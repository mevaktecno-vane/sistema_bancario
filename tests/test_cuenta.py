import pytest
from src.cliente import Cliente
from src.cuenta import Cuenta, SaldoInsuficienteError


def test_crear_cuenta_valida():
    cliente = Cliente("Juan", "Perez", "11111111")
    cuenta = Cuenta("001", cliente, saldo=500.0)
    assert cuenta.get_saldo() == 500.0
    assert cuenta.get_cliente().get_nombre() == "Juan"


def test_deposito_valido():
    cliente = Cliente("Ana", "Lopez", "22222222")
    cuenta = Cuenta("002", cliente)
    cuenta.depositar(100)
    assert cuenta.get_saldo() == 100.0


def test_retiro_valido():
    cliente = Cliente("Carlos", "Diaz", "33333333")
    cuenta = Cuenta("003", cliente, saldo=200)
    cuenta.retirar(50)
    assert cuenta.get_saldo() == 150.0


def test_saldo_insuficiente():
    cliente = Cliente("Pedro", "Gomez", "44444444")
    cuenta = Cuenta("004", cliente, saldo=10)
    with pytest.raises(SaldoInsuficienteError):
        cuenta.retirar(50)


def test_monto_no_numerico():
    cliente = Cliente("Laura", "Mendez", "55555555")
    cuenta = Cuenta("005", cliente)
    with pytest.raises(TypeError):
        cuenta.depositar("cien")
