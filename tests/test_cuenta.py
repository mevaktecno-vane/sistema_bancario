import pytest
from src.cuenta import Cuenta, SaldoInsuficienteError
from src.cliente import Cliente


# ==============================================================================
# FIXTURES (Aislamiento de dependencias y Reusabilidad)
# ==============================================================================

@pytest.fixture
def cliente_valido():
    """Retorna un cliente válido para asignar a la cuenta."""
    return Cliente(nombre="Laura", apellido="Gomez", dni="12345678")


@pytest.fixture
def cuenta_con_saldo(cliente_valido):
    """Retorna una cuenta con un saldo inicial predeterminado de 1000.0."""
    return Cuenta(nro_cuenta="CTA-001", cliente=cliente_valido, saldo=1000.0)


# ==============================================================================
# PRUEBAS UNITARIAS: INICIALIZACIÓN Y VALIDACIONES DEL CONSTRUCTOR
# ==============================================================================

def test_inicializacion_cuenta_exitosa(cliente_valido):
    """Verifica la creación correcta de la cuenta con sus atributos getters."""
    # Act
    cuenta = Cuenta(nro_cuenta="CTA-123", cliente=cliente_valido, saldo=500.0)

    # Assert
    assert cuenta.get_nro_cuenta() == "CTA-123"
    assert cuenta.get_saldo() == 500.0
    assert cuenta.get_cliente() == cliente_valido
    assert cuenta.get_transacciones() == []


def test_lanza_excepcion_numero_cuenta_invalido(cliente_valido):
    """Valida que no se permitan números de cuenta vacíos o de tipo incorrecto."""
    with pytest.raises(ValueError, match="El número de cuenta debe ser una cadena no vacía."):
        Cuenta(nro_cuenta="", cliente=cliente_valido)

    with pytest.raises(ValueError, match="El número de cuenta debe ser una cadena no vacía."):
        Cuenta(nro_cuenta=123, cliente=cliente_valido)  # type: ignore


def test_lanza_excepcion_saldo_inicial_negativo(cliente_valido):
    """Valida la regla de negocio: el saldo inicial no puede ser negativo."""
    with pytest.raises(ValueError, match="El saldo inicial no puede ser negativo."):
        Cuenta(nro_cuenta="CTA-001", cliente=cliente_valido, saldo=-100.0)


def test_lanza_excepcion_cliente_nulo():
    """Valida que no se pueda instanciar una cuenta sin cliente asignado."""
    with pytest.raises(ValueError, match="Debe asignarse un cliente válido a la cuenta."):
        Cuenta(nro_cuenta="CTA-001", cliente=None)


# ==============================================================================
# PRUEBAS UNITARIAS: OPERACIÓN DE DEPÓSITO
# ==============================================================================

def test_depositar_monto_valido_actualiza_saldo_y_transaccion(cuenta_con_saldo):
    """Verifica que el depósito incremente el saldo y agregue la transacción."""
    # Act
    cuenta_con_saldo.depositar(500.0)

    # Assert
    assert cuenta_con_saldo.get_saldo() == 1500.0
    assert len(cuenta_con_saldo.get_transacciones()) == 1


def test_lanza_excepcion_deposito_monto_no_numerico(cuenta_con_saldo):
    """Valida que no se permitan montos con tipos de datos inválidos."""
    with pytest.raises(TypeError, match="El monto del depósito debe ser un número."):
        cuenta_con_saldo.depositar("quinientos")  # type: ignore


def test_lanza_excepcion_deposito_monto_menor_o_igual_a_cero(cuenta_con_saldo):
    """Valida que no se acepten depósitos negativos o de monto cero."""
    with pytest.raises(ValueError, match="El monto del depósito debe ser mayor a cero."):
        cuenta_con_saldo.depositar(0)

    with pytest.raises(ValueError, match="El monto del depósito debe ser mayor a cero."):
        cuenta_con_saldo.depositar(-50.0)


# ==============================================================================
# PRUEBAS UNITARIAS: OPERACIÓN DE RETIRO Y CONTROL DE EXCEPCIONES
# ==============================================================================

def test_retirar_monto_valido_reduce_saldo_y_registra_transaccion(cuenta_con_saldo):
    """Verifica que un retiro válido reste saldo y agregue la transacción."""
    # Act
    cuenta_con_saldo.retirar(400.0)

    # Assert
    assert cuenta_con_saldo.get_saldo() == 600.0
    assert len(cuenta_con_saldo.get_transacciones()) == 1


def test_lanza_excepcion_retiro_monto_no_numerico(cuenta_con_saldo):
    """Valida que el monto del retiro deba ser numérico."""
    with pytest.raises(TypeError, match="El monto del retiro debe ser un número."):
        cuenta_con_saldo.retirar("cien")  # type: ignore


def test_lanza_excepcion_retiro_monto_menor_o_igual_a_cero(cuenta_con_saldo):
    """Valida que el retiro deba ser mayor a cero."""
    with pytest.raises(ValueError, match="El monto del retiro debe ser mayor a cero."):
        cuenta_con_saldo.retirar(0)


def test_lanza_excepcion_saldo_insuficiente(cuenta_con_saldo):
    """Valida la excepción personalizada SaldoInsuficienteError al superar el saldo."""
    with pytest.raises(SaldoInsuficienteError, match="Saldo insuficiente para realizar el retiro."):
        cuenta_con_saldo.retirar(2000.0)


# ==============================================================================
# PRUEBAS UNITARIAS: MOSTRAR TRANSACCIONES
# ==============================================================================

def test_mostrar_transacciones_sin_movimientos(cuenta_con_saldo):
    """Verifica el mensaje devuelto cuando la cuenta no registra movimientos."""
    assert cuenta_con_saldo.mostrar_transacciones() == ["No hay transacciones registradas."]


def test_mostrar_transacciones_con_movimientos(cuenta_con_saldo):
    """Verifica que se retorne una lista con los elementos registrados."""
    # Arrange
    cuenta_con_saldo.depositar(200.0)
    cuenta_con_saldo.retirar(100.0)

    # Act
    transacciones = cuenta_con_saldo.mostrar_transacciones()

    # Assert
    assert len(transacciones) == 2