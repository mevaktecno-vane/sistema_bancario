from src.cliente import Cliente
from src.cuenta import Cuenta, SaldoInsuficienteError
from src.cuenta_ahorro import CuentaAhorro
from src.tarjeta import Tarjeta, LimiteExcedidoError
from src.dao import DAO


# ====== INICIALIZAR DAO ======
dao = DAO("sistema_bancario.db")


# ====== FUNCIONES PRINCIPALES ======

def guardar_cliente(nombre, apellido, dni):
    """Agrega un nuevo cliente a la base de datos."""
    try:
        if not nombre or not apellido or not dni:
            raise ValueError("Todos los campos del cliente son obligatorios.")
        cliente = Cliente(nombre, apellido, dni)
        id_cliente = dao.guardar_cliente(cliente)
        print(f"Cliente agregado: {cliente} (ID: {id_cliente})\n")
        return id_cliente, cliente
    except ValueError as e:
        print(f"Error: {e}\n")
        return None, None


def mostrar_clientes():
    """Muestra todos los clientes registrados."""
    try:
        clientes_db = dao.obtener_todos_clientes()
        if len(clientes_db) == 0:
            raise IndexError("No hay clientes cargados.")
        print("\n=== LISTADO DE CLIENTES ===")
        for cliente in clientes_db:
            # cliente: (id_cliente, nombre, apellido, dni, fecha_registro)
            print(f"{cliente[1]} {cliente[2]} (DNI: {cliente[3]})")
        print()
    except IndexError as e:
        print(f"Atención: {e}\n")


def guardar_cuenta(nro_cuenta, id_cliente, tipo_cuenta="Corriente", saldo=0.0, tasa_interes=0.0):
    """Agrega una cuenta a la base de datos."""
    try:
        id_cuenta = dao.guardar_cuenta(nro_cuenta, id_cliente, tipo_cuenta, saldo, tasa_interes)
        print(f"Cuenta creada: {nro_cuenta} (ID: {id_cuenta})\n")
        return id_cuenta
    except ValueError as e:
        print(f"Error: {e}\n")
        return None


def mostrar_cuentas():
    """Muestra todas las cuentas registradas."""
    try:
        # Obtener todos los clientes para mostrar sus cuentas
        clientes_db = dao.obtener_todos_clientes()
        total_cuentas = 0
        
        if len(clientes_db) == 0:
            raise IndexError("No hay cuentas cargadas.")
        
        print("\n=== LISTADO DE CUENTAS ===")
        for cliente in clientes_db:
            id_cliente = cliente[0]
            nombre_cliente = f"{cliente[1]} {cliente[2]}"
            cuentas_cliente = dao.obtener_cuentas_por_cliente(id_cliente)
            
            if cuentas_cliente:
                print(f"\n{nombre_cliente}:")
                for cuenta in cuentas_cliente:
                    # cuenta: (id_cuenta, nro_cuenta, id_cliente, tipo_cuenta, saldo, tasa_interes, fecha_creacion)
                    print(f"  {cuenta[1]} - {cuenta[3]} - Saldo: ${cuenta[4]:.2f}")
                    total_cuentas += 1
        
        if total_cuentas == 0:
            raise IndexError("No hay cuentas cargadas.")
        print()
    except IndexError as e:
        print(f"Atención: {e}\n")


def guardar_tarjeta(numero, id_cliente, limite):
    """Agrega una tarjeta de crédito a la base de datos."""
    try:
        id_tarjeta = dao.guardar_tarjeta(numero, id_cliente, limite)
        print(f"Tarjeta agregada: {numero} (ID: {id_tarjeta})\n")
        return id_tarjeta
    except ValueError as e:
        print(f"Error: {e}\n")
        return None


def mostrar_tarjetas():
    """Muestra todas las tarjetas registradas."""
    try:
        clientes_db = dao.obtener_todos_clientes()
        total_tarjetas = 0
        
        if len(clientes_db) == 0:
            raise IndexError("No hay tarjetas registradas.")
        
        print("\n=== LISTADO DE TARJETAS ===")
        for cliente in clientes_db:
            id_cliente = cliente[0]
            nombre_cliente = f"{cliente[1]} {cliente[2]}"
            tarjetas_cliente = dao.obtener_tarjetas_por_cliente(id_cliente)
            
            if tarjetas_cliente:
                print(f"\n{nombre_cliente}:")
                for tarjeta in tarjetas_cliente:
                    # tarjeta: (id_tarjeta, numero_tarjeta, id_cliente, limite_credito, saldo_actual, fecha_emision)
                    print(f"  {tarjeta[1]} - Límite: ${tarjeta[3]:.2f} - Deuda: ${tarjeta[4]:.2f}")
                    total_tarjetas += 1
        
        if total_tarjetas == 0:
            raise IndexError("No hay tarjetas registradas.")
        print()
    except IndexError as e:
        print(f"Atención: {e}\n")


# ====== BLOQUE PRINCIPAL ======

def main():
    print("=== SISTEMA BANCARIO (Versión con Persistencia SQLite) ===\n")

    # Carga simulada de datos
    id_cliente1, cliente1 = guardar_cliente("Juan", "Pérez", "12345678")
    id_cliente2, cliente2 = guardar_cliente("Ana", "Gómez", "87654321")

    if id_cliente1:
        guardar_cuenta("001", id_cliente1, "Corriente", 1500)
    if id_cliente2:
        guardar_cuenta("002", id_cliente2, "Corriente", 2000)

    if id_cliente1:
        guardar_tarjeta("1111-2222-3333-4444", id_cliente1, 5000)
    if id_cliente2:
        guardar_tarjeta("9999-8888-7777-6666", id_cliente2, 3000)

    # Mostrar los datos cargados
    mostrar_clientes()
    mostrar_cuentas()
    mostrar_tarjetas()
    
    print("\n✅ Datos guardados en: sistema_bancario.db")
    
    # Cerrar conexión
    dao.cerrar_conexion()


if __name__ == "__main__":
    main()
