import flet as ft
from src.cliente import Cliente
from src.cuenta import Cuenta
from src.tarjeta import Tarjeta
from src.transaccion import Transaccion
from src.cuenta_ahorro import CuentaAhorro

def main(page: ft.Page):
    # Configuración básica de la página
    def show_alert(title: str, message: str, icon: ft.Icons, color=ft.Colors.RED):
    # Función local que puede acceder a 'page'
        def close_dlg(e):
            page.dialog.open = False
            page.update()
        
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Row([ft.Icon(icon, color=color), ft.Text(title)]),
            content=ft.Text(message),
            actions=[
                ft.TextButton("Ok", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
    
        page.dialog = dlg
        dlg.open = True
        page.update()


    page.title = "Banco estudiantil San Martín"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.update()
    nombre_input = ft.TextField(label="Nombre", width=200)
    apellido_input = ft.TextField(label="Apellido", width=200)
    dni_input = ft.TextField(label="DNI", width=200)
    nro_cuenta_input = ft.TextField(label="Nro de Cuenta", width=200, value="0001") 
    saldo_input = ft.TextField(label="Saldo Inicial", width=200, value="0.0") 
    transaction_list_cc = ft.Column()
    mi_cliente = Cliente(nombre="Daniel", apellido="Perez", dni="12345678") 
    mi_cuenta = CuentaAhorro(nro_cuenta="12345", cliente=mi_cliente, saldo=1000.0, interes=1.0)
    mi_tarjeta = Tarjeta(numero="9876-5432-1098-7654", cliente=mi_cliente)

    
    def manejar_nuevo_cliente(e):
        nonlocal mi_cliente, mi_cuenta, mi_tarjeta
        mi_cliente = Cliente(nombre=nombre_input.value, apellido=apellido_input.value, dni=dni_input.value)
        mi_cuenta = CuentaAhorro(nro_cuenta=nro_cuenta_input.value, cliente=mi_cliente, saldo=float(saldo_input.value), interes=1.0)
        mi_tarjeta = Tarjeta(numero="9876-5432-1098-7654", cliente=mi_cliente)
        
    # --- Nueva Variable para el Card que Muestra los Datos ---
    cliente_data_card = ft.Card(
        content=ft.ListTile(
        leading=ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLUE_GREY_700, size=30),
        title=ft.Text(f"Nombre Completo: {mi_cliente.get_nombre()} {mi_cliente.get_apellido()}", weight=ft.FontWeight.BOLD),
        subtitle=ft.Text(f"DNI: {mi_cliente.get_dni()}"),
    ),
    elevation=4
    )
    page.update()
   
    # Actualizar la sección de Cliente
    cliente_info = ft.Column(
        [
            ft.Text("Información del Cliente", size=24, weight=ft.FontWeight.W_600),
            ft.Container(height=80, content=ft.Text("Cargando cliente...")),
            cliente_data_card, 
            ft.Divider(),
            # Formulario para Nuevo Cliente (el fragmento que me pasaste)
            ft.Text("Nuevo Cliente y Cuentas:", size=20, weight=ft.FontWeight.W_500),
            ft.Row([nombre_input, apellido_input]),
            ft.Row([dni_input, nro_cuenta_input]),
            ft.Row([saldo_input]),
            ft.ElevatedButton(
                text="Crear Nuevo Cliente",
                icon=ft.Icons.SAVE,
                on_click=manejar_nuevo_cliente, 
                style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_500, color=ft.Colors.WHITE)
            )
        ],
        
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    cliente_info.controls[1] = ft.Card(
        content=ft.ListTile(
            leading=ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLUE_GREY_700, size=30),
            title=ft.Text(f"Nombre Completo: {mi_cliente.get_nombre()} {mi_cliente.get_apellido()}", weight=ft.FontWeight.BOLD),
            subtitle=ft.Text(f"DNI: {mi_cliente.get_dni()}"),
        ),
        elevation=4
    )
    # --- Función para Crear Nuevo Cliente ---
    
    # Intentar crear un nuevo cliente con los datos del formulario
    try:
        nuevo_saldo = float(saldo_input.value)
        
        # 1. Crea el nuevo Cliente
        mi_cliente = Cliente(
            nombre=nombre_input.value,   
            apellido=apellido_input.value,  
            dni=dni_input.value  
        )
        # 2. Crea la nueva Cuenta y Tarjeta (asociadas al nuevo cliente)
        mi_cuenta = CuentaAhorro(
            nro_cuenta=nro_cuenta_input.value,
            cliente=mi_cliente,
            saldo=nuevo_saldo,
            interes=1.0 # Tasa de interés por defecto
        )
        mi_tarjeta = Tarjeta(
            numero="9876-xxxx-xxxx-7654", # Un número de tarjeta simple
            cliente=mi_cliente
        )
        
        # 3. Actualizar la UI con la nueva información


        # Actualizar todos los controles dependientes
        actualizar_saldo() 
        actualizar_tarjeta()
        
        show_alert("Éxito", f"Cliente {mi_cliente.get_nombre()} agregado con éxito.", ft.Icons.PERSON_ADD, ft.Colors.BLUE_500)
        
    except Exception as ex:
        show_alert("Error de Creación", f"Error al crear: {ex}", ft.Icons.ERROR)
    
    # Reemplazamos el control existente con uno nuevo
        cliente_data_card.content = ft.ListTile(
            leading=ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLUE_GREY_700, size=30),
            title=ft.Text(f"Nombre Completo: {mi_cliente.get_nombre()} {mi_cliente.get_apellido()}", weight=ft.FontWeight.BOLD),
            subtitle=ft.Text(f"DNI: {mi_cliente.get_dni()}"),
        )
   
    page.update()
    # Campo de entrada para el importe

    cantidad_entrada = ft.TextField(
        label="Monto ($)", 
        width=150, 
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9.]"),
        keyboard_type=ft.KeyboardType.NUMBER
    )

    def actualizar_saldo():
        """"Actualiza el saldo de la cuenta y la lista de transacciones."."""
        current_balance_cc.value = f"${mi_cuenta.get_saldo():.2f}"
        
    # Reconstruir lista de transacciones

    transaction_list_cc.controls.clear()
        
    transactions = mi_cuenta.mostrar_transacciones()
    if not transactions:
            transaction_list_cc.controls.append(ft.Text("No hay transacciones aún.", italic=True, color=ft.Colors.BLACK54))
    else:
            for t in reversed(transactions): # Show most recent first
                color = ft.Colors.GREEN_700 if t.get_tipo() == 'deposito' else ft.Colors.RED_700
                transaction_list_cc.controls.append(
                    ft.Text(f"{t}", color=color, font_family="monospace")
                )

    page.update()

    # --- Sección cuenta ---

    # Componentes que se actualizan en tiempo real

    current_balance_cc = ft.Text(f"${mi_cuenta.get_saldo():.2f}", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_ACCENT_700)
    transaction_list_cc = ft.Column(scroll=ft.ScrollMode.AUTO, height=200, spacing=8)

    def manejar_operacion(tipo_operacion: str, e):
        """Gestiona las operaciones de depósito y retiro."""
        try:
            monto = float(cantidad_entrada.value)
            
            if tipo_operacion == "depositar":
                mi_cuenta.depositar(monto)
                show_alert("Éxito", f"Depósito de ${monto:.2f} realizado con éxito.", ft.Icons.CHECK_CIRCLE)
            elif tipo_operacion == "retirar":
                mi_cuenta.retirar(monto)
                show_alert("Éxito", f"Retiro de ${monto:.2f} realizado con éxito.", ft.Icons.CHECK_CIRCLE)
            
            cantidad_entrada.value = "" # Limpiar input
            actualizar_saldo() 
            
        except ValueError as ex:
            show_alert("Error de Monto", "Por favor, ingrese un monto positivo válido.", ft.Icons.WARNING_AMBER_ROUNDED)
        except SaldoInsuficienteError as ex:
            show_alert("Error de Saldo", str(ex), ft.Icons.ERROR)
        except Exception as ex:
            show_alert("Error Inesperado", f"Ocurrió un error: {ex}", ft.Icons.BUG_REPORT)

    cuenta_controles = ft.Container(
        content=ft.Column([
            ft.Text("Cuenta", size=24, weight=ft.FontWeight.W_600),
            ft.Text(f"Nro de Cuenta: {mi_cuenta.get_nro_cuenta()}", size=16, color=ft.Colors.BLACK54),
            ft.Card(
                content=ft.Container(
                    ft.Column([
                        ft.Text("Saldo Actual:", size=20, color=ft.Colors.BLACK87),
                        current_balance_cc
                    ]),
                    padding=15,
                    alignment=ft.alignment.center_left
                )
            ),
            ft.Row([
                cantidad_entrada,
                ft.ElevatedButton(
                    text="Depositar", 
                    icon=ft.Icons.ADD_CIRCLE, 
                    on_click=lambda e: manejar_operacion("depositar", e),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_500, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=10))
                ),
                ft.ElevatedButton(
                    text="Retirar", 
                    icon=ft.Icons.REMOVE_CIRCLE, 
                    on_click=lambda e: manejar_operacion("retirar", e),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.RED_500, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=10))
                ),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(height=25),
            ft.Text("Historial de Transacciones:", size=18, weight=ft.FontWeight.W_500),
            ft.Container(transaction_list_cc, border=ft.border.all(1, ft.Colors.BLACK26), border_radius=10, padding=10, expand=True)
        ], spacing=15),
        padding=20,
        width=600,
    )
    
    # --- Sección de cuenta de ahorros ---
    
    saldo_actual_ca = ft.Text(f"${mi_cuenta.get_saldo():.2f}", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.TEAL_ACCENT_700)
    texto_tasa_interes = ft.Text(f"Tasa de Interés: {mi_cuenta.get_interes() * 100:.2f}%", size=18, color=ft.Colors.TEAL_800)

    def click_aplicar_interes(e):
        """Applies interest to the savings account."""
        try:
            interes_ganado = mi_cuenta.aplicar_interes()
            saldo_actual_ca.value = f"${mi_cuenta.get_saldo():.2f}"
            
            if interes_ganado > 0:
                show_alert("Intereses Aplicados", f"¡Felicidades! Se aplicó un interés de ${interes_ganado:.2f} a la cuenta de ahorro.", ft.Icons.MONETIZATION_ON, ft.Colors.YELLOW_700)
            else:
                show_alert("Intereses Aplicados", "El saldo es cero o negativo, no se generaron intereses.", ft.Icons.INFO_OUTLINE)
            
            # Actualizamos el saldo de la cuenta y la lista de transacciones, ya que la transacción está registrada allí (en la clase base).
            actualizar_saldo() 
            page.update()
        except Exception as ex:
            show_alert("Error", f"Error al aplicar interés: {ex}", ft.Icons.BUG_REPORT)

    controles_ca = ft.Container(
        content=ft.Column([
            ft.Text("Cuenta de Ahorro", size=24, weight=ft.FontWeight.W_600),
            ft.Text(f"Nro de Cuenta: {mi_cuenta.get_nro_cuenta()}", size=16, color=ft.Colors.BLACK54),
            ft.Card(
                content=ft.Container(
                    ft.Column([
                       ft.Text("Saldo Actual:", size=20, color=ft.Colors.BLACK87),
                        saldo_actual_ca,
                        ft.Divider(),
                        texto_tasa_interes
                    ]),
                    padding=15,
                    alignment=ft.alignment.center_left
                )
            ),
            ft.ElevatedButton(
                text="Aplicar Intereses Ahora", 
                icon=ft.Icons.CALCULATE, 
                on_click=click_aplicar_interes,
                style=ft.ButtonStyle(bgcolor=ft.Colors.TEAL_300, color=ft.Colors.BLACK, shape=ft.RoundedRectangleBorder(radius=10)),
                width=300
            ),
        ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=20,
        width=600
    )

    #--- Sección tarjeta - operaciones ---

    #Componentes que se actualizan en tiempo real

    current_debt_card = ft.Text(f"${mi_tarjeta.get_saldo_actual():.2f}", size=32, weight=ft.FontWeight.BOLD)
    movement_list_card = ft.Column(scroll=ft.ScrollMode.AUTO, height=200, spacing=8)

    # Campo de entrada para el importe

    amount_input_card = ft.TextField(
        label="Monto ($)", 
        width=150, 
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9.]"),
        keyboard_type=ft.KeyboardType.NUMBER
    )
    
    def actualizar_tarjeta():
        """Actualiza la lista de deudas y movimientos de tarjetas."""
        
        # Color del texto de la deuda según el nivel de deuda
        debt_ratio = mi_tarjeta.get_saldo_actual() / mi_tarjeta.get_limite() if mi_tarjeta.get_limite() > 0 else 0
        
        if debt_ratio > 0.8:
            current_debt_card.color = ft.Colors.RED_800
        elif debt_ratio > 0.4:
            current_debt_card.color = ft.Colors.AMBER_800
        else:
            current_debt_card.color = ft.Colors.BLUE_GREY_700
            
        current_debt_card.value = f"${mi_tarjeta.get_saldo_actual():.2f}"

         # Lista de movimiento de reconstrucción

        movement_list_card.controls.clear()
        
        movements = mi_tarjeta.get_movimientos()
        if not movements:
            movement_list_card.controls.append(ft.Text("No hay movimientos aún.", italic=True, color=ft.Colors.BLACK54))
        else:
            for m in reversed(movements):
                color = ft.Colors.RED_700 if m.startswith('Compra') else ft.Colors.GREEN_700
                movement_list_card.controls.append(
                    ft.Text(f"{m}", color=color, font_family="monospace")
                )

        page.update()

    def manejar_operacion_tarjeta(tipo_operacion: str, e):
        """Gestiona las operaciones de compra y pago."""
        try:
            monto = float(actualizar_tarjeta.value)
            
            if tipo_operacion == "compra":
                mi_tarjeta.realizar_compra(monto)
                show_alert("Éxito", f"Compra de ${monto:.2f} registrada.", ft.Icons.SHOPPING_BAG, ft.Colors.RED_500)
            elif tipo_operacion == "pago":
                mi_tarjeta.pagar_tarjeta(monto)
                show_alert("Éxito", f"Pago de ${monto:.2f} aplicado. Deuda restante: ${mi_tarjeta.get_saldo_actual():.2f}", ft.Icons.RECEIPT, ft.Colors.GREEN_500)
            
            amount_input_card.value = "" # Limpiar input
            actualizar_tarjeta() # Actualizar la tarjeta
        except ValueError as ex:
            show_alert("Error de Monto", "Por favor, ingrese un monto positivo válido.", ft.Icons.WARNING_AMBER_ROUNDED)
        except LimiteExcedidoError as ex:
            show_alert("Límite Excedido", str(ex), ft.Icons.ERROR)
        except Exception as ex:
            show_alert("Error Inesperado", f"Ocurrió un error: {ex}", ft.Icons.BUG_REPORT)

    card_controls = ft.Container(
        content=ft.Column([
            ft.Text("Tarjeta de Crédito", size=24, weight=ft.FontWeight.W_600),
            ft.Text(f"Nro de Tarjeta: {mi_tarjeta.get_numero()}", size=16, color=ft.Colors.BLACK54),
            ft.Text(f"Límite de Crédito: ${mi_tarjeta.get_limite():.2f}", size=18, color=ft.Colors.BLUE_GREY_700),
            ft.Card(
                content=ft.Container(
                    ft.Column([
                        ft.Text("Deuda Actual:", size=20, color=ft.Colors.BLACK87),
                        current_debt_card
                    ]),
                    padding=15,
                    alignment=ft.alignment.center_left
                )
            ),
            ft.Row([
                amount_input_card,
                ft.ElevatedButton(
                    text="Realizar Compra", 
                    icon=ft.Icons.SHOPPING_CART, 
                    on_click=lambda e: manejar_operacion_tarjeta("compra", e),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.RED_500, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=10))
                ),
                ft.ElevatedButton(
                    text="Pagar Tarjeta", 
                    icon=ft.Icons.PAYMENT, 
                    on_click=lambda e: manejar_operacion_tarjeta("pago", e),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_500, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=10))
                ),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(height=25),
            ft.Text("Historial de Movimientos:", size=18, weight=ft.FontWeight.W_500),
            ft.Container(movement_list_card, border=ft.border.all(1, ft.Colors.BLACK26), border_radius=10, padding=10, expand=True)
        ], spacing=15),
        padding=20,
        width=600,
    )
    
    # --- Inicializar la interfaz de usuario y la carga de datos ---

    actualizar_saldo()
    actualizar_tarjeta()

    # --- Estructura de pestañas ---

    page.add(
        ft.Tabs(
            selected_index=0,
            animation_duration=300,
            expand=True,
            tabs=[
                ft.Tab(
                    text="Cliente",
                    icon=ft.Icons.ACCOUNT_CIRCLE,
                    content=ft.Container(cliente_info, alignment=ft.alignment.top_center, padding=20)
                ),
                ft.Tab(
                    text="Cuenta",
                    icon=ft.Icons.ACCOUNT_BALANCE,
                    content=ft.Container(cuenta_controles, alignment=ft.alignment.top_center)
                ),
                ft.Tab(
                    text="Cta. Ahorro",
                    icon=ft.Icons.SAVINGS,
                    content=ft.Container(controles_ca, alignment=ft.alignment.top_center)
                ),
                ft.Tab(
                    text="Tarjeta",
                    icon=ft.Icons.CREDIT_CARD,
                    content=ft.Container(card_controls, alignment=ft.alignment.top_center)
                ),
            ],
        )
    )
    
if __name__ == "__main__":
    ft.app(target=main)
    