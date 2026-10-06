# 🏦 Sistema Bancario - Refactoring, Testing e Integración Continua

Proyecto integrador para las asignaturas **Refactoring y Testing** e **Integración y Entrega Continua**.

## 👥 Integrantes y Equipo de Desarrollo
* **Mara Vanesa San Martín** (Tests de Dominio, Tests de Integración DAO, CI/CD)
* **Daniel Ricardo González** (ABM de transacciones y front de personal)
* **Erika Muñoz** (Integración)
* **Cristian Testaseca** (Base de Datos y DAO)
* **Andrés Verdún** (Gestión de clientes desde Backend)
* **Romina Marín** (Front Login y cliente)
* **Valentina San Martín** (Template)
* **Zafiro Ávila** (Front "Operar" e "Historial" de cliente)

## 🎯 Objetivos del Proyecto
* **Refactoring & Código Limpio:** Aplicación de principios SOLID (SRP, OCP, LSP, ISP, DIP), eliminación de Code Smells y lectura tipo periódico (*Extract Method*).
* **Testing Automatizado:** Suite integral unitaria y de integración usando `pytest` con arquitectura Arrange-Act-Assert (AAA) y fixtures.
* **Persistencia Desacoplada:** Manejo de DAO (Data Access Object) mediante SQLAlchemy ORM y SQLite (con soporte en memoria para tests).
* **Integración Continua (CI/CD):** Pipeline automatizado con **GitHub Actions** que ejecuta la suite de pruebas tras cada `push` y `Pull Request`.

## 🏛️ Arquitectura y Principios SOLID
1. **Single Responsibility Principle (SRP):** Desacoplamiento total entre la Lógica de Negocio (`src/cliente.py`, `src/cuenta.py`, etc.), la Persistencia (`src/dao.py`, `src/models.py`) y la Presentación (`app_banco.py`).
2. **Liskov Substitution Principle (LSP):** La clase `CuentaAhorro` extiende de `Cuenta` respetando estrictamente los contratos y comportamiento de la clase base.
3. **Inversión de Dependencias & DAO:** Uso de `DAO(":memory:")` para aislar completamente las pruebas de integración sin afectar la base de datos de producción.

## 🧪 Pruebas Automatizadas (`pytest`)

El proyecto cuenta con una suite integral dividida en dos niveles de testing que suman un total de **47 casos de prueba automatizados** (44 activos en verde y 3 omitidos temporalmente a la espera de merges externos):

### 1. Tests Unitarios (Dominio de Negocio)
* `tests/test_autenticacion.py`: Autenticación segura de usuarios y gestión de sesiones.
* `tests/test_persona.py`: Validaciones de la clase base `Persona`, formato de DNI y hashing de contraseñas.
* `tests/test_cliente.py`: Validaciones de formato, datos requeridos e integridad de la entidad `Cliente`.
* `tests/test_empleado.py`: Comportamiento, atributos y asignación de legajos/sucursales para `Empleado`.
* `tests/test_cuenta.py`: Depósitos, retiros, control de saldo y captura de `SaldoInsuficienteError`.
* `tests/test_cuenta_ahorro.py`: Cálculo de tasas de interés y validación de herencia Liskov (LSP).
* `tests/test_transaccion.py`: Historial de operaciones, marcas de tiempo (`datetime`) y validaciones de tipo/monto.
* `tests/test_tarjeta.py`: Compras, pagos y control de cupo con `LimiteExcedidoError`.
* `tests/test_navegacion.py`: Flujos de navegación e interacción lógica en la interfaz Flet.

### 2. Tests de Integración (Persistencia & DAO)
* `tests/test_dao_schema.py`: Validación del esquema relacional en SQLite, claves foráneas (`PRAGMA foreign_keys=ON`) y mapeo SQLAlchemy ORM.
* `tests/test_propuesta.py`: Integración completa de flujos de depósitos, retiros e intereses con persistencia aislada mediante base de datos en memoria (`DAO(":memory:")`).

## 🚀 Instalación y Ejecución Local

1. Clonar el repositorio
```bash
git clone [https://github.com/mevaktecno-vane/sistema_bancario.git](https://github.com/mevaktecno-vane/sistema_bancario.git)
cd sistema_bancario

2. Crear y activar el Entorno Virtual (venv)
PowerShell
# En Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# En Linux/macOS
python3 -m venv venv
source venv/bin/activate

3. Instalar dependencias
Bash
pip install -r requirements.txt

4. Ejecutar la suite de pruebas
Bash
# Correr todos los tests unitarios e integrativos
pytest

# Correr con reporte detallado de cobertura
pytest --cov=src -v

5. Ejecutar la Aplicación
Bash
# Interfaz gráfica principal (Flet)
python main.py
⚙️ Integración Continua (CI/CD)
El repositorio cuenta con un workflow de GitHub Actions configurado en .github/workflows/ci.yml. En cada push a cualquier rama o apertura de Pull Request, el servidor de CI:
1.	Configura el entorno Python aislado.
2.	Instala las dependencias del requirements.txt.
3.	Ejecuta la suite completa de pytest asegurando que no se introduzcan regresiones a main.
