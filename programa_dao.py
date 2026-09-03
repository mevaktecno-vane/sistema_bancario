"""Programa demostrativo que utiliza todas las operaciones publicas de DAO."""

import argparse

from src.cliente import Cliente
from src.dao import DAO


def mostrar_datos(dao: DAO, registros: list[tuple[int, int, int, str, str]]) -> None:
    """Consulta y muestra la informacion de todos los clientes de prueba."""
    clientes = dao.obtener_todos_clientes()
    print("\nTOTAL DE CLIENTES:", len(clientes))
    print("TODOS LOS CLIENTES:", clientes)

    for id_cliente, id_cuenta, id_tarjeta, dni, nro_cuenta in registros:
        print(f"\n--- CLIENTE {dni} ---")
        print("CLIENTE POR DNI:", dao.obtener_cliente_por_dni(dni))
        print("CUENTAS DEL CLIENTE:", dao.obtener_cuentas_por_cliente(id_cliente))
        print("CUENTA POR NUMERO:", dao.obtener_cuenta_por_numero(nro_cuenta))
        print("TARJETAS DEL CLIENTE:", dao.obtener_tarjetas_por_cliente(id_cliente))
        print("TRANSACCIONES:", dao.obtener_transacciones_por_cuenta(id_cuenta))
        print("MOVIMIENTOS DE TARJETA:", dao.obtener_movimientos_por_tarjeta(id_tarjeta))


def ejecutar_demo(limpiar: bool = False) -> None:
    """Ejecuta un flujo completo y persistente del DAO."""
    ruta_bd = "sistema_bancario.db"
    dao = DAO(ruta_bd)

    try:
        # Estas llamadas son idempotentes y muestran las utilidades de conexion.
        dao.create_tables()
        session = dao.connect()
        session.close()

        clientes = [
            ("Lucia", "Gomez", "30123456", "CA-0001", "4500-0000-0000-0001", 1600.0, 200.0),
            ("Carlos", "Rodriguez", "30234567", "CA-0002", "4500-0000-0000-0002", 2450.0, 450.0),
            ("Marta", "Fernandez", "30345678", "CA-0003", "4500-0000-0000-0003", 980.0, 125.0),
            ("Diego", "Martinez", "30456789", "CA-0004", "4500-0000-0000-0004", 3200.0, 700.0),
        ]
        registros = []

        for nombre, apellido, dni, nro_cuenta, nro_tarjeta, saldo, deuda in clientes:
            cliente = Cliente(nombre, apellido, dni)
            cliente_guardado = dao.obtener_cliente_por_dni(dni)
            id_cliente = cliente_guardado[0] if cliente_guardado else dao.guardar_cliente(cliente)

            cuenta_guardada = dao.obtener_cuenta_por_numero(nro_cuenta)
            id_cuenta = cuenta_guardada[0] if cuenta_guardada else dao.guardar_cuenta(
                nro_cuenta, id_cliente, "Ahorro", saldo=saldo, tasa_interes=2.5
            )

            tarjetas_guardadas = dao.obtener_tarjetas_por_cliente(id_cliente)
            tarjeta_guardada = next(
                (tarjeta for tarjeta in tarjetas_guardadas if tarjeta[1] == nro_tarjeta),
                None,
            )
            id_tarjeta = tarjeta_guardada[0] if tarjeta_guardada else dao.guardar_tarjeta(
                nro_tarjeta, id_cliente, 3000.0
            )

            dao.guardar_transaccion(id_cuenta, "deposito", 500.0)
            dao.guardar_transaccion(id_cuenta, "retiro", 100.0)
            dao.guardar_transaccion(id_cuenta, "interes", 50.0)
            dao.guardar_movimiento_tarjeta(id_tarjeta, "Compra", 250.0)
            dao.guardar_movimiento_tarjeta(id_tarjeta, "Pago", 50.0)
            dao.guardar_movimiento_tarjeta(id_tarjeta, "Compra", 75.0)

            dao.actualizar_saldo_cuenta(id_cuenta, saldo)
            dao.actualizar_saldo_tarjeta(id_tarjeta, deuda)
            registros.append((id_cliente, id_cuenta, id_tarjeta, dni, nro_cuenta))

        print("=== DEMOSTRACION COMPLETA DEL DAO ===")
        print(f"Datos guardados en: {ruta_bd}")
        mostrar_datos(dao, registros)

        if limpiar:
            dao.limpiar_base_datos()
            print("\nBD LIMPIA:", dao.obtener_todos_clientes())
        else:
            print("\nLos datos permanecen guardados para futuras ejecuciones.")
    finally:
        dao.cerrar_conexion()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Demostracion persistente del DAO")
    parser.add_argument(
        "--limpiar",
        action="store_true",
        help="elimina todos los datos despues de mostrar la demostracion",
    )
    argumentos = parser.parse_args()
    ejecutar_demo(limpiar=argumentos.limpiar)