import flet as ft


def ir_a(page: ft.Page, render_vista):
    """Limpia la página y renderiza la vista indicada (navegación entre vistas)."""
    page.clean()
    page.update()
    render_vista(page)
    page.update()