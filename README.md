# Sistema Bancario  
Proyecto integrador final de **Laboratorio I** y **Control de Versiones**  

---

## Integrantes
- **Mara Vanesa San Martín**  
- **Daniel Ricardo González**

---

## Descripción del Proyecto
Este proyecto modela un **sistema bancario** utilizando los principios de la **Programación Orientada a Objetos (POO)** con Python, integrando además control de versiones con Git/GitHub, pruebas unitarias, manejo de errores, generación de reportes PDF y una **interfaz gráfica desarrollada con Flet**.

---

## Objetivos del Trabajo
- Aplicar **abstracción, herencia, polimorfismo y encapsulamiento** en la implementación de las clases.
- Desarrollar un sistema funcional que permita:
  - Registrar clientes.  
  - Crear cuentas bancarias y tarjetas.  
  - Realizar operaciones (depósitos, retiros, compras, pagos).  
  - Exportar la información a un archivo PDF.  
- Implementar una **interfaz visual amigable**.
- Usar control de versiones (**Git y GitHub**) con trabajo colaborativo.
- Documentar y gestionar tareas mediante **Trello**.

---

---

## Clases Implementadas

###  `Cliente`
Representa a un cliente del banco con atributos privados (`nombre`, `apellido`, `dni`).

- Validación de datos (solo letras en nombre y apellido, DNI numérico).
- Métodos `get_` y `mostrar_datos()` para mostrar la información.

###  `Cuenta`
Maneja las operaciones bancarias principales.

- Métodos: `depositar()`, `retirar()`.
- Control de errores:
  - `SaldoInsuficienteError`
  - Validación de montos y tipos de datos.
- Registra transacciones automáticamente.

### `CuentaAhorro`
Hereda de `Cuenta` e implementa polimorfismo aplicando una **tasa de interés**.

###  `Tarjeta`
Permite registrar compras y pagos de crédito, con límite configurable.

### `Transaccion`
Registra la información de cada operación

---

## Interfaz con Flet

Se desarrolló una **interfaz gráfica completa** que permite:
- Registrar nuevos clientes.  
- Crear cuentas y tarjetas.  
- Realizar operaciones bancarias.
- Visualizar movimientos.  
- Exportar toda la información a PDF.  


---

##  Generación de PDF
Se implementó la función `generar_pdf_reporte()` con la librería **FPDF**.  
El archivo PDF exporta datos de:
- Cliente
- Cuenta y saldo actual
- Movimientos y transacciones

---

##  Pruebas Unitarias (pytest)
Cada clase principal cuenta con su archivo de prueba:
- `test_cliente.py`
- `test_cuenta.py`
- `test_tarjeta.py`

Ejemplo para ejecutar los tests:
```bash
pytest -v

Manejo de Errores

Se utiliza try-except en toda la app 

Validación de datos inválidos al crear clientes o cuentas.

Control de saldos insuficientes y límites de tarjeta.


Requerimientos

Archivo requirements.txt:

flet
fpdf
pytest

Control de Versiones y Trabajo Colaborativo

Proyecto gestionado con Git y GitHub.

Cada integrante trabajó en su rama personal (Vane y Daniel).

Se realizaron commits descriptivos y frecuentes.

Las tareas fueron organizadas en Trello, con estados:

* Pendiente

* En curso

* Finalizada

Documentos adicionales

trello_board.pdf: Export del tablero Trello usando Pretty Print.

docs/gitdiagram.png: Diagrama visual del flujo de Git (ramas, merges, commits).

docs/gitingest.md: Explicación del proceso de integración y control de versiones.



                                    Ejecución del Proyecto

Clonar el repositorio:

git clone https://github.com/mevaktecno-vane/sistema_bancario.git


Entrar al proyecto:

cd sistema_bancario


Activar entorno virtual:

python -m venv venv
venv\Scripts\activate  # En Windows


Instalar dependencias:

pip install -r requirements.txt


Ejecutar la aplicación:

python main.py

 Evaluación Final

El proyecto cumple con:

Principios de POO.

Manejo de errores.

Pruebas unitarias.

Interfaz gráfica funcional.

Control de versiones y documentación.

Trabajo colaborativo documentado.