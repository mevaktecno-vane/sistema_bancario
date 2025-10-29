import flet as ft
import src.cliente as cliente

def main(page: ft.Page):
    # Configuración básica de la página
    page.title = "Banco estudiantil San Martín"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.update()

    #Sección cliente

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


    #Sección tarjeta
    #Sección cuenta 
    if __name__ == "__main__":
        ft.app(target=main)
    