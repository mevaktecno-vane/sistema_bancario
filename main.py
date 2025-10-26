from src.cliente import Cliente
from src.cuenta import Cuenta, SaldoInsuficienteError
from src.cuenta_ahorro import CuentaAhorro
from src.tarjeta import Tarjeta, LimiteExcedidoError

clientes = []
cuentas = []
tarjetas = []


def buscar_cliente_por_dni(dni):
    for c in clientes:
        if c.get_dni() == dni:
            return c
    return None


def menu():
    while True:
        print("\n===== SISTEMA BANCARIO INTERACTIVO =====")
        print("1. Crear cliente")
        print("2. Crear cuenta corriente")
        print("3. Crear cuenta de ahorro")
        print("4. Depositar dinero")
        print("5. Retirar dinero")
        print("6. Ver saldo")
        print("7. Crear tarjeta")
        print("8. Realizar compra con tarjeta")
        print("9. Pagar tarjeta")
        print("10. Ver movimientos de tarjeta")
        print("0. Salir")

        opcion = input("\nSelecciona una opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            dni = input("DNI: ")
            try:
                cliente = Cliente(nombre, apellido, dni)
                clientes.append(cliente)
                print(f"Cliente creado: {cliente}")
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "2":
            dni = input("DNI del cliente: ")
            cliente = buscar_cliente_por_dni(dni)
            if cliente:
                nro = input("Número de cuenta: ")
                try:
                    cuenta = Cuenta(nro, cliente)
                    cuentas.append(cuenta)
                    print("Cuenta corriente creada con éxito.")
                except ValueError as e:
                    print(f"Error: {e}")
            else:
                print("Cliente no encontrado.")

        elif opcion == "3":
            dni = input("DNI del cliente: ")
            cliente = buscar_cliente_por_dni(dni)
            if cliente:
                nro = input("Número de cuenta ahorro: ")
                interes = float(input("Tasa de interés (%): "))
                cuenta = CuentaAhorro(nro, cliente, interes=interes)
                cuentas.append(cuenta)
                print("Cuenta de ahorro creada con éxito.")
            else:
                print("Cliente no encontrado.")

        elif opcion == "4":
            nro = input("Número de cuenta: ")
            for c in cuentas:
                if c.get_nro_cuenta() == nro:
                    monto = float(input("Monto a depositar: "))
                    try:
                        c.depositar(monto)
                        print(
                            f"Depósito exitoso. Saldo actual: ${c.get_saldo()}")
                    except ValueError as e:
                        print(f"Error: {e}")
                    break
            else:
                print("Cuenta no encontrada.")

        elif opcion == "5":
            nro = input("Número de cuenta: ")
            for c in cuentas:
                if c.get_nro_cuenta() == nro:
                    monto = float(input("Monto a retirar: "))
                    try:
                        c.retirar(monto)
                        print(
                            f"Retiro exitoso. Saldo actual: ${c.get_saldo()}")
                    except (SaldoInsuficienteError, ValueError) as e:
                        print(f"Error: {e}")
                    break
            else:
                print("Cuenta no encontrada.")

        elif opcion == "6":
            nro = input("Número de cuenta: ")
            for c in cuentas:
                if c.get_nro_cuenta() == nro:
                    print(f"Saldo actual: ${c.get_saldo()}")
                    break
            else:
                print("Cuenta no encontrada.")

        elif opcion == "7":
            dni = input("DNI del cliente: ")
            cliente = buscar_cliente_por_dni(dni)
            if cliente:
                numero = input("Número de tarjeta: ")
                limite = float(input("Límite de crédito: "))
                try:
                    tarjeta = Tarjeta(numero, cliente, limite)
                    tarjetas.append(tarjeta)
                    print("Tarjeta creada con éxito.")
                except ValueError as e:
                    print(f"Error: {e}")
            else:
                print("Cliente no encontrado.")

        elif opcion == "8":
            numero = input("Número de tarjeta: ")
            for t in tarjetas:
                if t.get_numero() == numero:
                    monto = float(input("Monto de la compra: "))
                    try:
                        t.realizar_compra(monto)
                        print(
                            f"Compra registrada. Saldo actual: ${t.get_saldo_actual()}")
                    except (ValueError, LimiteExcedidoError) as e:
                        print(f"Error: {e}")
                    break
            else:
                print("Tarjeta no encontrada.")

        elif opcion == "9":
            numero = input("Número de tarjeta: ")
            for t in tarjetas:
                if t.get_numero() == numero:
                    monto = float(input("Monto del pago: "))
                    try:
                        t.pagar_tarjeta(monto)
                        print(
                            f"Pago registrado. Saldo actual: ${t.get_saldo_actual()}")
                    except ValueError as e:
                        print(f"Error: {e}")
                    break
            else:
                print("Tarjeta no encontrada.")

        elif opcion == "10":
            numero = input("Número de tarjeta: ")
            for t in tarjetas:
                if t.get_numero() == numero:
                    print("\nMovimientos de tarjeta:")
                    for fecha, monto, tipo in t.get_movimientos():
                        print(
                            f" - {fecha.strftime('%Y-%m-%d %H:%M:%S')} | {tipo}: ${monto}")
                    break
            else:
                print("Tarjeta no encontrada.")

        elif opcion == "0":
            print("Gracias por usar el sistema bancario.")
            break

        else:
            print("Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    menu()
