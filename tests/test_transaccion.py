import pytest
from src.transaccion import Transaccion


def test_crear_transaccion_deposito():
    t = Transaccion("deposito", 100.0)
    assert t.get_tipo() == "deposito"
    assert t.get_monto() == 100.0
    assert t.get_fecha() is not None
    assert "deposito" in str(t)


def test_crear_transaccion_retiro():
    t = Transaccion("retiro", 50.0)
    assert t.get_tipo() == "retiro"
    assert t.get_monto() == 50.0
    assert t.get_fecha() is not None
    assert "retiro" in str(t)


def test_tipo_permitido_desde_tabla_tipo_transaccion():
    t = Transaccion("pagoIntereses", 100.0)
    assert t.get_tipo() == "pagoIntereses"
    assert t.get_monto() == 100.0


def test_monto_invalido():
    with pytest.raises(ValueError):
        Transaccion("deposito", -50.0)


def test_monto_no_numerico():
    with pytest.raises(TypeError):
        Transaccion("deposito", "cien")


def test_crear_transaccion_desde_fila_db():
    fecha = "2025-01-12 10:30:00"
    t = Transaccion.from_db_row((7, 3, 3, 250.5, fecha))
    assert t.get_id_transaccion() == 7
    assert t.get_id_cuenta() == 3
    assert t.get_id_tipo_transaccion() == 3
    assert t.get_tipo() == "pagoIntereses"
    assert t.get_monto() == 250.5
    assert str(t.get_fecha()) == fecha
