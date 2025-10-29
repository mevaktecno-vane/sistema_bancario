from src.cliente import Cliente
from src.cuenta import Cuenta, SaldoInsuficienteError
from src.cuenta_ahorro import CuentaAhorro
from src.tarjeta import Tarjeta, LimiteExcedidoError


# ====== ARREGLOS ======
clientes = []
cuentas = []
tarjetas = []


# ====== FUNCIONES PRINCIPALES ======

def guardar_cliente(nombre, apellido, dni):
    """Agrega un nuevo cliente a la lista."""
    try:
        if not nombre or not apellido or not dni:
            raise ValueError("Todos los campos del cliente son obligatorios.")
        if any(c.get_dni() == dni for c in clientes):
            raise ValueError("Ya existe un cliente con ese DNI.")
        cliente = Cliente(nombre, apellido, dni)
        clientes.append(cliente)
        print(f"Cliente agregado: {cliente}\n")
        return cliente
    except ValueError as e:
        print(f"Error: {e}\n")


def mostrar_clientes():
    """Muestra todos los clientes registrados."""
    try:
        if len(clientes) == 0:
            raise IndexError("No hay clientes cargados.")
        print("\n=== LISTADO DE CLIENTES ===")
        for cliente in clientes:
            print(cliente)
        print()
    except IndexError as e:
        print(f"Atención: {e}\n")


def guardar_cuenta(nro_cuenta, cliente, saldo=0.0):
    """Agrega una cuenta corriente."""
    try:
        cuenta = Cuenta(nro_cuenta, cliente, saldo)
        cuentas.append(cuenta)
        print(f"Cuenta creada: {nro_cuenta}\n")
        return cuenta
    except ValueError as e:
        print(f"Error: {e}\n")


def mostrar_cuentas():
    """Muestra todas las cuentas creadas."""
    try:
        if len(cuentas) == 0:
            raise IndexError("No hay cuentas cargadas.")
        print("\n=== LISTADO DE CUENTAS ===")
        for cuenta in cuentas:
            print(
                f"{cuenta.get_nro_cuenta()} - {cuenta.get_cliente().get_dni()} - ${cuenta.get_saldo()}")
        print()
    except IndexError as e:
        print(f"Atención: {e}\n")


def guardar_tarjeta(numero, cliente, limite):
    """Agrega una nueva tarjeta de crédito."""
    try:
        tarjeta = Tarjeta(numero, cliente, limite)
        tarjetas.append(tarjeta)
        print(f"Tarjeta agregada: {numero}\n")
        return tarjeta
    except ValueError as e:
        print(f"Error: {e}\n")


def mostrar_tarjetas():
    """Muestra todas las tarjetas registradas."""
    try:
        if len(tarjetas) == 0:
            raise IndexError("No hay tarjetas registradas.")
        print("\n=== LISTADO DE TARJETAS ===")
        for tarjeta in tarjetas:
            print(
                f"{tarjeta.get_numero()} - {tarjeta.get_cliente().get_dni()} - Saldo: ${tarjeta.get_saldo_actual()}")
        print()
    except IndexError as e:
        print(f"Atención: {e}\n")


# ====== BLOQUE PRINCIPAL ======

def main():
    print("=== SISTEMA BANCARIO (Versión evaluable) ===\n")

    # Carga simulada de datos
    cliente1 = guardar_cliente("Juan", "Pérez", "12345678")
    cliente2 = guardar_cliente("Ana", "Gómez", "87654321")

    guardar_cuenta("001", cliente1, 1500)
    guardar_cuenta("002", cliente2, 2000)

    guardar_tarjeta("1111-2222-3333-4444", cliente1, 5000)
    guardar_tarjeta("9999-8888-7777-6666", cliente2, 3000)

    # Mostrar los datos cargados
    mostrar_clientes()
    mostrar_cuentas()
    mostrar_tarjetas()


if __name__ == "__main__":
    main()
