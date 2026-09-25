import pytest
from datetime import datetime
from src.transaccion import Transaccion


# ==============================================================================
# PRUEBAS UNITARIAS: INICIALIZACIÓN Y GETTERS (Happy Path)
# ==============================================================================

def test_creacion_transaccion_deposito_exitosa():
    """Verifica la instanciación correcta de una transacción tipo depósito."""
    # Act
    transaccion = Transaccion(tipo="deposito", monto=1500.0)

    # Assert
    assert transaccion.get_tipo() == "deposito"
    assert transaccion.get_monto() == 1500.0
    assert isinstance(transaccion.get_fecha(), datetime)


def test_creacion_transaccion_retiro_exitosa():
    """Verifica la instanciación correcta de una transacción tipo retiro."""
    # Act
    transaccion = Transaccion(tipo="retiro", monto=500.0)

    # Assert
    assert transaccion.get_tipo() == "retiro"
    assert transaccion.get_monto() == 500.0


def test_representacion_cadena_formateada():
    """Verifica que __str__ incluya el tipo, el monto y el formato de fecha."""
    # Arrange
    transaccion = Transaccion(tipo="deposito", monto=250.0)

    # Act
    resultado_str = str(transaccion)

    # Assert
    assert "deposito: $250.0" in resultado_str
    assert transaccion.get_fecha().strftime('%Y-%m-%d') in resultado_str


# ==============================================================================
# PRUEBAS UNITARIAS: VALIDACIONES Y EXCEPCIONES (SRP)
# ==============================================================================

def test_lanza_excepcion_tipo_transaccion_invalido():
    """Valida que solo se permitan tipos 'deposito' o 'retiro'."""
    with pytest.raises(ValueError, match="Tipo de transacción inválido"):
        Transaccion(tipo="transferencia", monto=100.0)


def test_lanza_excepcion_monto_no_numerico():
    """Valida que el monto deba ser de tipo entero o flotante."""
    with pytest.raises(TypeError, match="El monto debe ser un número."):
        Transaccion(tipo="deposito", monto="cien")  # type: ignore


def test_lanza_excepcion_monto_menor_o_igual_a_cero():
    """Valida la regla de negocio: el monto debe ser mayor a cero."""
    with pytest.raises(ValueError, match="El monto debe ser mayor a cero."):
        Transaccion(tipo="deposito", monto=0)

    with pytest.raises(ValueError, match="El monto debe ser mayor a cero."):
        Transaccion(tipo="retiro", monto=-50.0)