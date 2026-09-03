# Guía de Integración de DAO en app_banco.py

## Estado Actual

El archivo `app_banco.py` usa listas en memoria (`clientes_registrados`, `cuentas`, `tarjetas`) que no persisten entre sesiones.

## Plan de Integración

### 1. Ya Implementado ✅
- Importación del DAO: `from src.dao import DAO`
- Inicialización: `dao = DAO("sistema_bancario.db")`
- Cambio en estructura de estado: `estado = {"id_cliente": None, "id_cuenta": None, "id_tarjeta": None}`
- Cargar clientes desde BD al iniciar

### 2. Cambios Necesarios en Funciones Principales

#### Función: `registrar_cliente(e)`
**Cambio**: En lugar de agregar a `clientes_registrados`, guardar en DAO

```python
# ANTES:
cliente = Cliente(nombre, apellido, dni)
clientes_registrados.append(cliente)

# DESPUÉS:
cliente = Cliente(nombre, apellido, dni)
id_cliente = dao.guardar_cliente(cliente)
estado["id_cliente"] = id_cliente
```

#### Función: `crear_cuenta(e)`
**Cambio**: Guardar en DAO en lugar de en memoria

```python
# ANTES:
nueva_cuenta = Cuenta(nro_cuenta, estado["cliente"], saldo_inicial)
estado["cuenta"] = nueva_cuenta

# DESPUÉS:
id_cuenta = dao.guardar_cuenta(nro_cuenta, estado["id_cliente"], tipo_cuenta, saldo_inicial, interes)
estado["id_cuenta"] = id_cuenta
```

#### Función: `depositar(e)`
**Cambio**: Actualizar BD después de depósito

```python
# DESPUÉS DEL DEPÓSITO:
dao.guardar_transaccion(estado["id_cuenta"], "deposito", monto)
estado_cuenta = dao.obtener_cuentas_por_cliente(estado["id_cliente"])
nuevo_saldo = estado_cuenta[0][4]  # campo saldo
dao.actualizar_saldo_cuenta(estado["id_cuenta"], nuevo_saldo)
```

#### Función: `crear_tarjeta(e)`
**Cambio**: Guardar en DAO

```python
# DESPUÉS:
id_tarjeta = dao.guardar_tarjeta(nro_tarjeta, estado["id_cliente"], limite)
estado["id_tarjeta"] = id_tarjeta
```

### 3. Funciones Que Necesitan Refactorización

| Función | Cambio Necesario |
|---------|------------------|
| `actualizar_tarjeta_clientes()` | Cargar desde `dao.obtener_todos_clientes()` |
| `seleccionar_cliente()` | Usar `estado["id_cliente"]` en lugar de objeto |
| `reset_formulario_cliente()` | Limpiar IDs en estado |
| `guardar_cliente()` (en app_banco) | Llamar a `dao.guardar_cliente()` |
| `depositar()` | Guardar transacción en DAO + actualizar BD |
| `retirar()` | Guardar transacción en DAO + actualizar BD |
| `comprar()` | Guardar movimiento en DAO |
| `pagar()` | Guardar movimiento en DAO |

### 4. Carga de Datos al Iniciar

En `main(page)`, después de inicializar el DAO:

```python
# Cargar clientes desde BD
clientes_db = dao.obtener_todos_clientes()

# Actualizar interfaz con clientes existentes
for cliente_data in clientes_db:
    id_cliente = cliente_data[0]
    nombre = cliente_data[1]
    apellido = cliente_data[2]
    dni = cliente_data[3]
    
    # Agregar a la UI
    btn = ft.ElevatedButton(
        text="Seleccionar",
        on_click=lambda e, cid=id_cliente: seleccionar_cliente(cid)
    )
    lista_clientes_column.controls.append(
        ft.Row([ft.Text(f"{nombre} {apellido}"), btn])
    )
```

### 5. Funciones Auxiliares Para Trabajar con BD

```python
def obtener_saldo_cuenta(id_cuenta):
    """Obtiene el saldo actual de una cuenta desde la BD."""
    cuentas = dao.obtener_cuentas_por_cliente(estado["id_cliente"])
    for cuenta in cuentas:
        if cuenta[0] == id_cuenta:  # id_cuenta es el primer campo
            return cuenta[4]  # saldo es el quinto campo
    return 0.0

def obtener_deuda_tarjeta(id_tarjeta):
    """Obtiene la deuda actual de una tarjeta desde la BD."""
    tarjetas = dao.obtener_tarjetas_por_cliente(estado["id_cliente"])
    for tarjeta in tarjetas:
        if tarjeta[0] == id_tarjeta:  # id_tarjeta es el primer campo
            return tarjeta[4]  # saldo_actual es el quinto campo
    return 0.0
```

### 6. Persistencia de Transacciones

Cada operación debe:
1. Modificar el estado local
2. Guardar en la BD
3. Actualizar la UI

Ejemplo:
```python
def depositar(e):
    try:
        monto = float(txt_monto_cuenta.value)
        
        # 1. Crear transacción en BD
        dao.guardar_transaccion(estado["id_cuenta"], "deposito", monto)
        
        # 2. Obtener nuevo saldo
        cuenta_data = dao.obtener_cuentas_por_cliente(estado["id_cliente"])[0]
        nuevo_saldo = cuenta_data[4] + monto
        
        # 3. Actualizar BD
        dao.actualizar_saldo_cuenta(estado["id_cuenta"], nuevo_saldo)
        
        # 4. Actualizar UI
        mostrar_notificacion(f"💰 Depósito de ${monto:.2f} realizado")
        actualizar_saldo_cuenta()
    except Exception as ex:
        mostrar_notificacion(f"❌ Error: {ex}")
```

### 7. Al Cerrar la Aplicación

```python
def on_close(e):
    """Cierra la conexión a la BD al cerrar la app."""
    dao.cerrar_conexion()
    page.window_destroy()

page.window_on_close = on_close
```

## Próximos Pasos

1. Reemplazar todas las referencias a `clientes_registrados` con llamadas al DAO
2. Usar `estado["id_cliente"]`, `estado["id_cuenta"]`, `estado["id_tarjeta"]` en lugar de objetos
3. Guardar cada operación en la BD con `dao.guardar_transaccion()` y `dao.guardar_movimiento_tarjeta()`
4. Actualizar la UI para mostrar datos desde la BD

## Ejemplo Completo Refactorizado

Ver archivo `app_banco_persistente.py` (si se crea)
