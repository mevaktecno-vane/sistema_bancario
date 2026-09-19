# DAO (Data Access Object) - SQLite

## Descripción

El módulo **DAO** implementa el patrón Data Access Object para gestionar la persistencia de datos del sistema bancario usando **SQLite**. Esto permite:

- ✅ Guardar datos de forma persistente
- ✅ Recuperar información de la base de datos
- ✅ Actualizar saldos y registros
- ✅ Mantener un historial de todas las operaciones
- ✅ Separar la lógica de acceso a datos del negocio

## Estructura de la Base de Datos

### Tablas

#### 1. **clientes**
Almacena información de los clientes.

```sql
CREATE TABLE clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    dni TEXT UNIQUE NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

#### 2. **cuentas**
Almacena las cuentas bancarias.

```sql
CREATE TABLE cuentas (
    id_cuenta INTEGER PRIMARY KEY AUTOINCREMENT,
    nro_cuenta TEXT UNIQUE NOT NULL,
    id_cliente INTEGER NOT NULL,
    tipo_cuenta TEXT NOT NULL,  -- 'Corriente' o 'Ahorro'
    saldo REAL NOT NULL DEFAULT 0.0,
    tasa_interes REAL DEFAULT 0.0,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
)
```

#### 3. **tarjetas**
Almacena las tarjetas de crédito.

```sql
CREATE TABLE tarjetas (
    id_tarjeta INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_tarjeta TEXT UNIQUE NOT NULL,
    id_cliente INTEGER NOT NULL,
    limite_credito REAL NOT NULL,
    saldo_actual REAL NOT NULL DEFAULT 0.0,
    fecha_emision TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
)
```

#### 4. **transacciones**
Registra todas las operaciones en las cuentas.

```sql
CREATE TABLE transacciones (
    id_transaccion INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cuenta INTEGER NOT NULL,
    tipo_transaccion TEXT NOT NULL,  -- 'deposito', 'retiro', 'interes'
    monto REAL NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cuenta) REFERENCES cuentas(id_cuenta)
)
```

#### 5. **movimientos_tarjeta**
Registra los movimientos de las tarjetas.

```sql
CREATE TABLE movimientos_tarjeta (
    id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
    id_tarjeta INTEGER NOT NULL,
    tipo_movimiento TEXT NOT NULL,  -- 'Compra' o 'Pago'
    monto REAL NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_tarjeta) REFERENCES tarjetas(id_tarjeta)
)
```

## Uso

### Inicializar el DAO

```python
from src.dao import DAO

# Crear instancia del DAO (crea la BD si no existe)
dao = DAO("sistema_bancario.db")
```

### Operaciones con Clientes

```python
# Guardar un cliente
from src.cliente import Cliente

cliente = Cliente("Juan", "Pérez", "12345678")
id_cliente = dao.guardar_cliente(cliente)

# Obtener cliente por DNI
cliente_data = dao.obtener_cliente_por_dni("12345678")

# Obtener todos los clientes
todos_clientes = dao.obtener_todos_clientes()
for cliente in todos_clientes:
    print(f"{cliente[1]} {cliente[2]}")
```

### Operaciones con Cuentas

```python
# Guardar una cuenta
id_cuenta = dao.guardar_cuenta(
    nro_cuenta="001",
    id_cliente=id_cliente,
    tipo_cuenta="Corriente",
    saldo=1500.0
)

# Obtener cuentas de un cliente
cuentas = dao.obtener_cuentas_por_cliente(id_cliente)

# Obtener cuenta por número
cuenta = dao.obtener_cuenta_por_numero("001")

# Actualizar saldo
dao.actualizar_saldo_cuenta(id_cuenta, 2000.0)
```

### Operaciones con Transacciones

```python
# Guardar transacción
id_trans = dao.guardar_transaccion(
    id_cuenta=id_cuenta,
    tipo_transaccion="deposito",
    monto=500.0
)

# Obtener transacciones de una cuenta
transacciones = dao.obtener_transacciones_por_cuenta(id_cuenta)
for trans in transacciones:
    # trans: (id, id_cuenta, tipo, monto, fecha)
    print(f"{trans[2]}: ${trans[3]}")
```

### Operaciones con Tarjetas

```python
# Guardar tarjeta
id_tarjeta = dao.guardar_tarjeta(
    numero_tarjeta="1111-2222-3333-4444",
    id_cliente=id_cliente,
    limite_credito=5000.0
)

# Obtener tarjetas de un cliente
tarjetas = dao.obtener_tarjetas_por_cliente(id_cliente)

# Actualizar saldo de tarjeta
dao.actualizar_saldo_tarjeta(id_tarjeta, 1500.0)

# Guardar movimiento
id_mov = dao.guardar_movimiento_tarjeta(
    id_tarjeta=id_tarjeta,
    tipo_movimiento="Compra",
    monto=250.0
)

# Obtener movimientos
movimientos = dao.obtener_movimientos_por_tarjeta(id_tarjeta)
```

### Utilidades

```python
# Limpiar toda la base de datos (¡CUIDADO!)
dao.limpiar_base_datos()

# Cerrar conexión
dao.cerrar_conexion()
```

## Ejemplo Completo

Ver archivo `ejemplo_dao.py`:

```bash
python ejemplo_dao.py
```

## Integración con el Sistema Actual

Para integrar el DAO con la aplicación actual, es necesario:

1. Instanciar el DAO al inicio de la aplicación
2. Usar los métodos del DAO para guardar/recuperar datos en lugar de usar listas en memoria
3. Actualizar las funciones de `main.py` y `app_banco.py` para usar el DAO

Ejemplo:

```python
from src.dao import DAO
from src.cliente import Cliente

dao = DAO()

# En lugar de:
# clientes = []
# cliente = Cliente(...)
# clientes.append(cliente)

# Hacer:
cliente = Cliente(...)
id_cliente = dao.guardar_cliente(cliente)

# Para recuperar:
clientes = dao.obtener_todos_clientes()
```

## Ventajas del DAO

- 📊 **Persistencia**: Los datos se guardan en disco
- 🔒 **Integridad**: Validaciones a nivel de base de datos
- 📈 **Escalabilidad**: Fácil de cambiar a otra BD (PostgreSQL, MySQL, etc.)
- 🎯 **Modularidad**: Lógica de datos separada de la lógica de negocio
- 📋 **Historial**: Se mantienen registros de todas las operaciones

## Notas

- El archivo de base de datos se crea automáticamente en el directorio raíz del proyecto
- Las tablas se crean automáticamente si no existen
- Los DNI y números de tarjeta son UNIQUE para evitar duplicados
- Las transacciones incluyen timestamp automático
