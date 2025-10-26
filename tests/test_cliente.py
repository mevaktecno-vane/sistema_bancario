from src.cliente import Cliente
import pytest


def test_crear_cliente():
    cliente = Cliente("Ana", "Lopez", "12345678")
    assert cliente.get_nombre() == "Ana"
    assert cliente.get_apellido() == "Lopez"
    assert cliente.get_dni() == "12345678"


def test_dni_invalido():
    with pytest.raises(ValueError):
        Cliente("Ana", "Lopez", "12A345678")


def test_nombre_vacio():
    with pytest.raises(ValueError):
        Cliente("", "Lopez", "12345678")
