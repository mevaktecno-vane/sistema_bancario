
import pytest
from src.cliente import Cliente


def test_crear_cliente_valido():
    cliente = Cliente("Ana", "López", "12345678")
    assert cliente.get_nombre() == "Ana"
    assert cliente.get_apellido() == "López"
    assert cliente.get_dni() == "12345678"


def test_cliente_nombre_vacio():
    with pytest.raises(ValueError):
        Cliente("", "López", "12345678")


def test_cliente_dni_vacio():
    with pytest.raises(ValueError):
        Cliente("Ana", "López", "")
