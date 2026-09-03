# Integracion del DAO

## Estado actual

El proyecto tiene dos usos del DAO:

- `main.py` usa SQLite para guardar y consultar clientes, cuentas y tarjetas.
- `programa_dao.py` ejecuta una demostracion completa y persistente de todas las operaciones del DAO.
- `src/app_banco.py` inicializa el DAO y carga los clientes existentes, pero sus operaciones de cuenta y tarjeta todavia trabajan principalmente con objetos en memoria.

La base de datos utilizada por los programas es `sistema_bancario.db`. El DAO crea las tablas automaticamente al inicializarse.

## Operaciones disponibles en DAO

### Conexion y tablas

```python
dao = DAO("sistema_bancario.db")
dao.create_tables()
session = dao.connect()
session.close()
dao.cerrar_conexion()
```

### Clientes

```python
id_cliente = dao.guardar_cliente(Cliente("Lucia", "Gomez", "30123456"))
cliente = dao.obtener_cliente_por_dni("30123456")
clientes = dao.obtener_todos_clientes()
```

### Cuentas

```python
id_cuenta = dao.guardar_cuenta(
    "CA-0001", id_cliente, "Ahorro", saldo=1200.0, tasa_interes=2.5
)
cuentas = dao.obtener_cuentas_por_cliente(id_cliente)
cuenta = dao.obtener_cuenta_por_numero("CA-0001")
dao.actualizar_saldo_cuenta(id_cuenta, 1600.0)
```

### Tarjetas

```python
id_tarjeta = dao.guardar_tarjeta(
    "4500-0000-0000-0001", id_cliente, limite_credito=3000.0
)
tarjetas = dao.obtener_tarjetas_por_cliente(id_cliente)
dao.actualizar_saldo_tarjeta(id_tarjeta, 200.0)
```

### Historiales

```python
dao.guardar_transaccion(id_cuenta, "deposito", 500.0)
transacciones = dao.obtener_transacciones_por_cuenta(id_cuenta)

dao.guardar_movimiento_tarjeta(id_tarjeta, "Compra", 250.0)
movimientos = dao.obtener_movimientos_por_tarjeta(id_tarjeta)
```

### Limpieza

`limpiar_base_datos()` elimina todos los registros respetando el orden de las
relaciones. Es una operacion destructiva y no se ejecuta en el flujo normal de
`programa_dao.py`; solo se activa con:

```powershell
python programa_dao.py --limpiar
```

## Pendientes en `src/app_banco.py`

La interfaz Flet todavia necesita completar la integracion para que todas sus
operaciones persistan en SQLite:

1. Guardar el cliente con `dao.guardar_cliente()` y conservar su ID.
2. Crear cuentas con `dao.guardar_cuenta()` y consultar sus saldos desde la BD.
3. Crear tarjetas con `dao.guardar_tarjeta()` y consultar su deuda desde la BD.
4. En depositos, retiros e intereses, guardar la transaccion y actualizar el saldo.
5. En compras y pagos, guardar el movimiento y actualizar el saldo de la tarjeta.
6. Cargar los historiales desde `obtener_transacciones_por_cuenta()` y
   `obtener_movimientos_por_tarjeta()` al seleccionar una cuenta o tarjeta.
7. Cerrar el DAO cuando se cierre la ventana de Flet.

El estado recomendado para la interfaz es:

```python
estado = {
    "id_cliente": None,
    "id_cuenta": None,
    "id_tarjeta": None,
}
```

Los IDs deben utilizarse para consultar y actualizar la base de datos. Los
objetos de dominio pueden mantenerse para mostrar la interfaz, pero no deben
ser la unica fuente de datos persistentes.

## Ejemplos ejecutables

Demostracion completa del DAO:

```powershell
python programa_dao.py
```

Ejemplo basico de persistencia:

```powershell
python main.py
```
