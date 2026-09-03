"""
Ejemplo de uso del DAO (Data Access Object) con SQLite.
Muestra cómo guardar y recuperar datos de la base de datos.
"""

from src.dao import DAO
from src.cliente import Cliente
from src.cuenta import Cuenta
from src.cuenta_ahorro import CuentaAhorro
from src.tarjeta import Tarjeta


def ejemplo_dao():
    """Ejemplo completo de uso del DAO."""
    
    # Inicializar el DAO
    dao = DAO("sistema_bancario.db")
    
    print("\n" + "="*60)
    print("EJEMPLO DE USO DEL DAO CON SQLITE")
    print("="*60)
    
    # 1. GUARDAR CLIENTES
    print("\n1️⃣  GUARDANDO CLIENTES...")
    try:
        cliente1 = Cliente("Juan", "Pérez", "12345678")
        cliente2 = Cliente("Ana", "Gómez", "87654321")
        
        id_cliente1 = dao.guardar_cliente(cliente1)
        id_cliente2 = dao.guardar_cliente(cliente2)
        
        print(f"   ✅ Cliente Juan guardado con ID: {id_cliente1}")
        print(f"   ✅ Cliente Ana guardado con ID: {id_cliente2}")
    except ValueError as e:
        print(f"   ⚠️  {e}")
        # Obtener los clientes existentes si ya están en la BD
        clientes_existentes = dao.obtener_todos_clientes()
        if len(clientes_existentes) >= 2:
            id_cliente1 = clientes_existentes[0][0]
            id_cliente2 = clientes_existentes[1][0]
            print(f"   ℹ️  Usando clientes existentes: Juan (ID: {id_cliente1}), Ana (ID: {id_cliente2})")
    
    # 2. OBTENER CLIENTES
    print("\n2️⃣  OBTENIENDO CLIENTES DE LA BD...")
    clientes = dao.obtener_todos_clientes()
    for cliente in clientes:
        print(f"   - ID: {cliente[0]}, Nombre: {cliente[1]} {cliente[2]}, DNI: {cliente[3]}")
    
    # 3. GUARDAR CUENTAS
    print("\n3️⃣  GUARDANDO CUENTAS...")
    try:
        # Cuenta corriente para Juan
        id_cuenta1 = dao.guardar_cuenta("001", id_cliente1, "Cuenta Corriente", 1500.0)
        print(f"   ✅ Cuenta Corriente guardada con ID: {id_cuenta1}")
        
        # Cuenta de ahorro para Ana
        id_cuenta2 = dao.guardar_cuenta("002", id_cliente2, "Ahorro", 2000.0, 2.5)
        print(f"   ✅ Cuenta de Ahorro guardada con ID: {id_cuenta2}")
    except ValueError as e:
        print(f"   ⚠️  {e}")
    
    # 4. OBTENER CUENTAS POR CLIENTE
    print("\n4️⃣  OBTENIENDO CUENTAS DE JUAN (ID: 1)...")
    cuentas = dao.obtener_cuentas_por_cliente(id_cliente1)
    for cuenta in cuentas:
        print(f"   - Nro: {cuenta[1]}, Tipo: {cuenta[3]}, Saldo: ${cuenta[4]:.2f}")
    
    # 5. GUARDAR TRANSACCIONES
    print("\n5️⃣  GUARDANDO TRANSACCIONES...")
    try:
        # Depósito
        id_trans1 = dao.guardar_transaccion(id_cuenta1, "deposito", 500.0)
        print(f"   ✅ Depósito de $500 registrado")
        
        # Retiro
        id_trans2 = dao.guardar_transaccion(id_cuenta1, "retiro", 200.0)
        print(f"   ✅ Retiro de $200 registrado")
        
        # Interés
        id_trans3 = dao.guardar_transaccion(id_cuenta2, "interes", 50.0)
        print(f"   ✅ Interés de $50 registrado")
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    # 6. OBTENER TRANSACCIONES
    print("\n6️⃣  OBTENIENDO TRANSACCIONES DE LA CUENTA...")
    transacciones = dao.obtener_transacciones_por_cuenta(id_cuenta1)
    for trans in transacciones:
        print(f"   - {trans[2].upper()}: ${trans[3]:.2f} - {trans[4]}")
    
    # 7. GUARDAR TARJETAS
    print("\n7️⃣  GUARDANDO TARJETAS...")
    try:
        id_tarjeta1 = dao.guardar_tarjeta("1111-2222-3333-4444", id_cliente1, 5000.0)
        print(f"   ✅ Tarjeta de Juan guardada con ID: {id_tarjeta1}")
        
        id_tarjeta2 = dao.guardar_tarjeta("9999-8888-7777-6666", id_cliente2, 3000.0)
        print(f"   ✅ Tarjeta de Ana guardada con ID: {id_tarjeta2}")
    except ValueError as e:
        print(f"   ⚠️  {e}")
    
    # 8. GUARDAR MOVIMIENTOS DE TARJETA
    print("\n8️⃣  GUARDANDO MOVIMIENTOS DE TARJETA...")
    try:
        # Compra
        id_mov1 = dao.guardar_movimiento_tarjeta(id_tarjeta1, "Compra", 250.0)
        print(f"   ✅ Compra de $250 registrada")
        
        # Pago
        id_mov2 = dao.guardar_movimiento_tarjeta(id_tarjeta1, "Pago", 100.0)
        print(f"   ✅ Pago de $100 registrado")
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    # 9. OBTENER MOVIMIENTOS DE TARJETA
    print("\n9️⃣  OBTENIENDO MOVIMIENTOS DE TARJETA...")
    movimientos = dao.obtener_movimientos_por_tarjeta(id_tarjeta1)
    for mov in movimientos:
        print(f"   - {mov[2]}: ${mov[3]:.2f} - {mov[4]}")
    
    # 10. ACTUALIZAR SALDOS
    print("\n🔟 ACTUALIZANDO SALDOS...")
    dao.actualizar_saldo_cuenta(id_cuenta1, 1800.0)
    print(f"   ✅ Saldo de cuenta actualizado a $1800")
    
    dao.actualizar_saldo_tarjeta(id_tarjeta1, 150.0)
    print(f"   ✅ Saldo de tarjeta actualizado a $150")
    
    # 11. RESUMEN FINAL
    print("\n" + "="*60)
    print("RESUMEN FINAL DE LA BASE DE DATOS")
    print("="*60)
    
    print("\n📋 CLIENTES REGISTRADOS:")
    for cliente in dao.obtener_todos_clientes():
        print(f"   • {cliente[1]} {cliente[2]} (DNI: {cliente[3]})")
    
    print("\n💳 CUENTAS:")
    for cuenta in dao.obtener_cuentas_por_cliente(id_cliente1):
        print(f"   • Nro {cuenta[1]} - {cuenta[3]} - Saldo: ${cuenta[4]:.2f}")
    for cuenta in dao.obtener_cuentas_por_cliente(id_cliente2):
        print(f"   • Nro {cuenta[1]} - {cuenta[3]} - Saldo: ${cuenta[4]:.2f}")
    
    print("\n💰 TRANSACCIONES (Cuenta Juan):")
    for trans in dao.obtener_transacciones_por_cuenta(id_cuenta1):
        print(f"   • {trans[2].upper()}: ${trans[3]:.2f}")
    
    print("\n🎫 TARJETAS:")
    print(f"   • {dao.obtener_tarjetas_por_cliente(id_cliente1)[0][1]} (Juan)")
    print(f"   • {dao.obtener_tarjetas_por_cliente(id_cliente2)[0][1]} (Ana)")
    
    print("\n" + "="*60)
    print("✅ Ejemplo completado exitosamente")
    print("="*60 + "\n")
    
    # Cerrar conexión
    dao.cerrar_conexion()


if __name__ == "__main__":
    ejemplo_dao()
