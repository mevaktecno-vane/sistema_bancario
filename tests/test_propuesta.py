import pytest

def test_infraestructura_tests_activa():
    """Verifica que la suite de pruebas y pytest están funcionando correctamente."""
    assert True

@pytest.mark.skip(reason="T-01: Esperando merge de Cristian (BE-01/BE-05) para probar PersonaModel y Login.")
def test_autenticacion_persona(db_session):
    pass

@pytest.mark.skip(reason="T-02: Esperando merge de Cristian (BE-03) para probar constraint una cuenta por tipo.")
def test_constraint_una_cuenta_por_tipo(db_session):
    pass

@pytest.mark.skip(reason="T-03: Esperando merge de Andrés (BE-07/BE-09) para probar alta y edición de cliente.")
def test_alta_y_edicion_cliente(db_session):
    pass

@pytest.mark.skip(reason="T-04: Esperando merge de Daniel (BE-10/BE-11) para probar depósitos y retiros.")
def test_depositos_y_retiros(db_session):
    pass