# tests/test_transaccion.py
import pytest
from src.transaccion import Transaccion


def test_crear_transaccion_deposito():
    t = Transaccion("deposito", 100.0)
    assert t.tipo == "deposito"
    assert t.monto == 100.0
    assert hasattr(t, "fecha")


def test_crear_transaccion_retiro():
    t = Transaccion("retiro", 50.0)
    assert t.tipo == "retiro"
    assert t.monto == 50.0


def test_tipo_invalido():
    with pytest.raises(ValueError):
        Transaccion("transferencia", 100.0)


def test_monto_negativo():
    with pytest.raises(ValueError):
        Transaccion("deposito", -20)
