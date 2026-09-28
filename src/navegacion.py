import flet as ft


def ir_a(page: ft.Page, render_vista):
    """Limpia la página y renderiza la vista indicada (navegación entre vistas)."""
    page.clean()
    page.update()
    render_vista(page)
    page.update()


def _item_navegacion(icono, etiqueta, activo=False, on_click=None, BORDE_NEON="#8b2fc9", GRIS_OSCURO="#7a7a7a"):
    color = "#ffffff" if activo else GRIS_OSCURO
    return ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        padding=ft.Padding(10, 8, 10, 8),
        bgcolor=BORDE_NEON if activo else None,
        border_radius=12,
        on_click=on_click,
        content=ft.Column(
            spacing=3,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(icono, color=color, size=22),
                ft.Text(etiqueta, size=10, color=color),
            ],
        ),
    )


def crear_bottom_nav(page: ft.Page, activo: str):
    """Crea la barra de navegación inferior con navegación funcional."""
    def ir_inicio(e):
        from src.home_cliente import render_home_cliente
        ir_a(page, render_home_cliente)
    def ir_operar(e):
        from src.home_operaciones import render_home_operaciones
        ir_a(page, render_home_operaciones)
    def ir_historial(e):
        from src.home_historial import render_home_historial
        ir_a(page, render_home_historial)

    return ft.Container(
        padding=ft.Padding(8, 8, 8, 8),
        bgcolor="#121212",
        border=ft.border.all(1, "#2d1b4e"),
        border_radius=20,
        content=ft.Row(
            spacing=8,
            controls=[
                _item_navegacion(ft.Icons.HOME, "Inicio", activo == "inicio", on_click=ir_inicio),
                _item_navegacion(ft.Icons.SYNC_ALT, "Operar", activo == "operar", on_click=ir_operar),
                _item_navegacion(ft.Icons.HISTORY, "Historial", activo == "historial", on_click=ir_historial),
            ],
        ),
    )