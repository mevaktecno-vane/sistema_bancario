from sqlalchemy import update

from src.cliente import Cliente
from src.models import ClienteModel


# =========================================================
# BE-07 - ALTA DE CLIENTE
# =========================================================

def alta_cliente(dao, nombre, apellido, dni):
    """
    Crea un nuevo cliente y lo guarda en la base de datos.
    """

    # Comprobar si ya existe un cliente con ese DNI
    cliente_existente = dao.obtener_cliente_por_dni(dni)

    if cliente_existente is not None:
        raise ValueError("Ya existe un cliente con ese DNI.")

    # Crear el cliente.
    # La clase Cliente realiza las validaciones básicas.
    nuevo_cliente = Cliente(nombre, apellido, dni)

    # Guardar el cliente en la base de datos
    id_cliente = dao.guardar_cliente(nuevo_cliente)

    return id_cliente


# =========================================================
# BE-08 - ALTA DE CUENTA
# =========================================================

def alta_cuenta(
    dao,
    dni,
    nro_cuenta,
    tipo_cuenta,
    saldo_inicial=0.0
):
    """
    Crea una cuenta para un cliente existente.
    """

    # Validar saldo
    try:
        saldo_inicial = float(saldo_inicial)
    except (ValueError, TypeError):
        raise ValueError("El saldo inicial debe ser un número.")

    if saldo_inicial < 0:
        raise ValueError("El saldo inicial no puede ser negativo.")

    # Normalizar el tipo de cuenta
    tipo_cuenta = tipo_cuenta.strip().lower()

    if tipo_cuenta not in ("ahorro", "corriente"):
        raise ValueError(
            "El tipo de cuenta debe ser 'ahorro' o 'corriente'."
        )

    # Buscar cliente por DNI
    cliente = dao.obtener_cliente_por_dni(dni)

    if cliente is None:
        raise ValueError("No existe un cliente con ese DNI.")

    # La posición 0 de la tupla contiene el id_cliente
    id_cliente = cliente[0]

    # Obtener las cuentas actuales del cliente
    cuentas = dao.obtener_cuentas_por_cliente(id_cliente)

    # Comprobar que no tenga otra cuenta del mismo tipo
    for cuenta in cuentas:
        tipo_existente = cuenta[3].strip().lower()

        if tipo_existente == tipo_cuenta:
            raise ValueError(
                f"El cliente ya posee una cuenta de tipo {tipo_cuenta}."
            )

    # Comprobar que el número de cuenta no esté usado
    cuenta_existente = dao.obtener_cuenta_por_numero(nro_cuenta)

    if cuenta_existente is not None:
        raise ValueError("Ya existe una cuenta con ese número.")

    # Guardar la cuenta
    id_cuenta = dao.guardar_cuenta(
        nro_cuenta=nro_cuenta,
        id_cliente=id_cliente,
        tipo_cuenta=tipo_cuenta,
        saldo=saldo_inicial
    )

    return id_cuenta


# =========================================================
# BE-09 - EDITAR CLIENTE
# =========================================================

def editar_cliente(
    dao,
    dni_actual,
    nuevo_nombre,
    nuevo_apellido,
    nuevo_dni
):
    """
    Modifica los datos de un cliente existente.
    """

    # Buscar el cliente
    cliente_actual = dao.obtener_cliente_por_dni(dni_actual)

    if cliente_actual is None:
        raise ValueError("No existe un cliente con ese DNI.")

    # Crear temporalmente un Cliente para validar los datos nuevos
    datos_nuevos = Cliente(
        nuevo_nombre,
        nuevo_apellido,
        nuevo_dni
    )

    # Si cambia el DNI, comprobar que no esté ocupado
    if nuevo_dni != dni_actual:
        cliente_con_nuevo_dni = dao.obtener_cliente_por_dni(
            nuevo_dni
        )

        if cliente_con_nuevo_dni is not None:
            raise ValueError(
                "Ya existe otro cliente con ese DNI."
            )

    # Actualizar el cliente en la base de datos
    with dao.session_factory.begin() as session:
        session.execute(
            update(ClienteModel)
            .where(ClienteModel.dni == dni_actual)
            .values(
                nombre=datos_nuevos.get_nombre(),
                apellido=datos_nuevos.get_apellido(),
                dni=datos_nuevos.get_dni()
            )
        )

    return True