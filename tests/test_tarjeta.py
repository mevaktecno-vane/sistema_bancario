import pytest
from src.tarjeta import Tarjeta, LimiteExcedidoError
from src.cliente import Cliente


def test_crear_tarjeta():
    cliente = Cliente("Carla", "Romero", "11223344")
    tarjeta = Tarjeta("9999-8888-7777-6666", cliente, limite=5000.0)
    assert tarjeta.get_limite() == 5000.0
    assert tarjeta.get_saldo_actual() == 0.0


def test_realizar_compra():
    cliente = Cliente("Luis", "Fernandez", "22334455")
    tarjeta = Tarjeta("1111-2222-3333-4444", cliente, limite=1000)
    tarjeta.realizar_compra(500)
    assert tarjeta.get_saldo_actual() == 500


def test_limite_excedido():
    cliente = Cliente("Ana", "Perez", "33445566")
    tarjeta = Tarjeta("1234-5678-9012-3456", cliente, limite=1000)
    with pytest.raises(LimiteExcedidoError):
        tarjeta.realizar_compra(2000)


def test_pagar_tarjeta():
    cliente = Cliente("Mario", "Gomez", "44556677")
    tarjeta = Tarjeta("9876-5432-1098-7654", cliente, limite=3000)
    tarjeta.realizar_compra(1000)
    tarjeta.pagar_tarjeta(500)
    assert tarjeta.get_saldo_actual() == 500
