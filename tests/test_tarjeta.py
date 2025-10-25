import pytest
from src.tarjeta import Tarjeta, LimiteExcedidoError
from src.cliente import Cliente


def test_crear_tarjeta():
    cliente = Cliente("Carlos", "Martinez", "55555555")
    tarjeta = Tarjeta("1234-5678", cliente, 1000.0)
    assert tarjeta.numero == "1234-5678"
    assert tarjeta.get_limite_credito() == 1000.0
    assert tarjeta.get_saldo_disponible() == 1000.0


def test_compra_exitosa():
    cliente = Cliente("Laura", "Gomez", "44444444")
    tarjeta = Tarjeta("5678-9999", cliente, 500.0)
    tarjeta.comprar(200.0)
    assert tarjeta.get_saldo_disponible() == 300.0


def test_compra_limite_excedido():
    cliente = Cliente("Pedro", "Luna", "66666666")
    tarjeta = Tarjeta("7890-1111", cliente, 300.0)
    with pytest.raises(LimiteExcedidoError):
        tarjeta.comprar(400.0)


def test_pago_tarjeta():
    cliente = Cliente("Lucia", "Suarez", "88888888")
    tarjeta = Tarjeta("1111-2222", cliente, 1000.0)
    tarjeta.comprar(400.0)
    tarjeta.pagar(200.0)
    assert tarjeta.get_saldo_disponible() == 800.0


def test_pago_excede_limite():
    cliente = Cliente("Mariano", "Vega", "99999999")
    tarjeta = Tarjeta("9999-0000", cliente, 1000.0)
    tarjeta.pagar(500.0)
    assert tarjeta.get_saldo_disponible() == 1000.0
