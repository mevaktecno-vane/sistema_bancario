import flet as ft

from src.app_banco import main as app_gui
from src.login import render_login


def ir_a_vista_principal(page: ft.Page, dni: str, clave: str):
    """Navegación provisional (INT-05): sin autenticación real todavía,
    cualquier DNI/clave lleva a la vista principal para ir integrando las vistas."""
    page.clean()
    page.bgcolor = ft.Colors.WHITE
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    app_gui(page)


def main(page: ft.Page):
    render_login(page, on_login_submit=ir_a_vista_principal)


if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=8550)