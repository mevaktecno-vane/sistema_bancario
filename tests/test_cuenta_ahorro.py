import pytest
from src.cuenta_ahorro import CuentaAhorro
from src.cliente import Cliente


def test_crear_cuenta_ahorro():
    cliente = Cliente("Nora", "Ramirez", "12345678")
    cuenta_ahorro = CuentaAhorro(
        "AH001", cliente, saldo=1000.0, tasa_interes=0.05)
    assert cuenta_ahorro.nro_cuenta == "AH001"
    assert cuenta_ahorro.saldo == 1000.0
    assert cuenta_ahorro.tasa_interes == 0.05


def test_aplicar_interes():
    cliente = Cliente("Leo", "Perez", "22222222")
    cuenta_ahorro = CuentaAhorro(
        "AH002", cliente, saldo=1000.0, tasa_interes=0.10)
    interes = cuenta_ahorro.aplicar_interes()
    assert interes == 100.0
    assert cuenta_ahorro.saldo == 1100.0


def test_hereda_metodos_cuenta():
    cliente = Cliente("Marta", "Gomez", "33333333")
    cuenta_ahorro = CuentaAhorro("AH003", cliente, saldo=500.0)
    cuenta_ahorro.depositar(200.0)
    assert cuenta_ahorro.saldo == 700.0
    cuenta_ahorro.retirar(300.0)
    assert cuenta_ahorro.saldo == 400.0
