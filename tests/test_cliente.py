import pytest
from src.cliente import Cliente


def test_creacion_cliente():
    c = Cliente("Juan", "Perez", "12345678")
    assert c.get_nombre() == "Juan"
    assert c.get_apellido() == "Perez"
    assert c.get_dni() == "12345678"

    def test_validacion_nombre_invalido():
        c = Cliente("Juan", "Perez", "12345678")
        with pytest.raises(ValueError):
            c.set_nombre("Juan123")

    def test_mostrar_datos():
        c = Cliente("Ana", "Gomez", "87654321")
        salida = c.mostrar_datos()
        assert "Ana Gomez" in salida
        assert "87654321" in salida
