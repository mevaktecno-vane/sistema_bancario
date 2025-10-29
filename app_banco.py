import flet as ft
import src.cliente as cliente
import src.cuenta as cuenta
import src.tarjeta as tarjeta
import src.transaccion as transaccion

def main(page: ft.Page):
    # Configuración básica de la página
    page.title = "Banco estudiantil San Martín"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.update()

    # --- Sección cliente ---

    cliente_info = ft.Column(
        [
            ft.Text("Información del Cliente", size=24, weight=ft.FontWeight.W_600),
            ft.Card(
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLUE_GREY_700, size=30),
                    title=ft.Text(f"Nombre Completo: {cliente.get_nombre()} {cliente.get_apellido()}", weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(f"DNI: {cliente.get_dni()}"),
                ),
                elevation=4
            ),
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    # Campo de entrada para el importe

    cantidad_entrada = ft.TextField(
        label="Monto ($)", 
        width=150, 
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9.]"),
        keyboard_type=ft.KeyboardType.NUMBER
    )

    def actualizar_saldo():
        """"Actualiza el saldo de la cuenta y la lista de transacciones."."""
        current_balance_cc.value = f"${cuenta.get_saldo():.2f}"
        
    # Reconstruir lista de transacciones

    transaction_list_cc.controls.clear()
        
    transactions = cuenta.mostrar_transacciones()
    if not transactions:
            transaction_list_cc.controls.append(ft.Text("No hay transacciones aún.", italic=True, color=ft.colors.BLACK54))
    else:
            for t in reversed(transactions): # Show most recent first
                color = ft.Colors.GREEN_700 if t.get_tipo() == 'deposito' else ft.Colors.RED_700
                transaction_list_cc.controls.append(
                    ft.Text(f"{t}", color=color, font_family="monospace")
                )

    page.update()

    # --- Sección cuenta ---

    # Componentes que se actualizan en tiempo real
    current_balance_cc = ft.Text(f"${cuenta.get_saldo():.2f}", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_ACCENT_700)
    transaction_list_cc = ft.Column(scroll=ft.ScrollMode.AUTO, height=200, spacing=8)

    def manejar_operacion(tipo_operacion: str, e):
        """Gestiona las operaciones de depósito y retiro."""
        try:
            monto = float(cantidad_entrada.value)
            
            if tipo_operacion == "depositar":
                cuenta.depositar(monto)
                show_alert("Éxito", f"Depósito de ${monto:.2f} realizado con éxito.", ft.Icons.CHECK_CIRCLE)
            elif tipo_operacion == "retirar":
                cuenta.retirar(monto)
                show_alert("Éxito", f"Retiro de ${monto:.2f} realizado con éxito.", ft.Icons.CHECK_CIRCLE)
            
            cantidad_entrada.value = "" # Limpiar input
            actualizar_saldo() 
            
        except ValueError as ex:
            show_alert("Error de Monto", "Por favor, ingrese un monto positivo válido.", ft.Icons.WARNING_AMBER_ROUNDED)
        except SaldoInsuficienteError as ex:
            show_alert("Error de Saldo", str(ex), ft.icons.ERROR)
        except Exception as ex:
            show_alert("Error Inesperado", f"Ocurrió un error: {ex}", ft.Icons.BUG_REPORT)

    cuenta_controles = ft.Container(
        content=ft.Column([
            ft.Text("Cuenta", size=24, weight=ft.FontWeight.W_600),
            ft.Text(f"Nro de Cuenta: {cuenta.get_nro_cuenta()}", size=16, color=ft.Colors.BLACK54),
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
                    icon=ft.icons.ADD_CIRCLE, 
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
    
    saldo_actual_ca = ft.Text(f"${cuenta.get_saldo():.2f}", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.TEAL_ACCENT_700)
    texto_tasa_interes = ft.Text(f"Tasa de Interés: {cuenta.get_interes() * 100:.2f}%", size=18, color=ft.colors.TEAL_800)

    def click_aplicar_interes(e):
        """Applies interest to the savings account."""
        try:
            interes_ganado = cuenta.aplicar_interes()
            saldo_actual_ca.value = f"${cuenta.get_saldo():.2f}"
            
            if interes_ganado > 0:
                show_alert("Intereses Aplicados", f"¡Felicidades! Se aplicó un interés de ${interes_ganado:.2f} a la cuenta de ahorro.", ft.icons.MONETIZATION_ON, ft.colors.YELLOW_700)
            else:
                 show_alert("Intereses Aplicados", "El saldo es cero o negativo, no se generaron intereses.", ft.icons.INFO_OUTLINE)
            
            # Actualizamos el saldo de la cuenta y la lista de transacciones, ya que la transacción está registrada allí (en la clase base).
            actualizar_saldo() 
            page.update()
        except Exception as ex:
            show_alert("Error", f"Error al aplicar interés: {ex}", ft.icons.BUG_REPORT)

    controles_ca = ft.Container(
        content=ft.Column([
            ft.Text("Cuenta de Ahorro", size=24, weight=ft.FontWeight.W_600),
            ft.Text(f"Nro de Cuenta: {cuenta.get_nro_cuenta()}", size=16, color=ft.Colors.BLACK54),
            ft.Card(
                content=ft.Container(
                    ft.Column([
                        ft.Text("Saldo Actual:", size=20, color=ft.Colors.BLACK87),
                        actualizar_saldo,
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

    #Sección tarjeta
  
    if __name__ == "__main__":
        ft.app(target=main)
    