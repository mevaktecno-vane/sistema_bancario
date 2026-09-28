import os
import sys

import flet as ft

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cuenta import Cuenta
from src.cuenta_ahorro import CuentaAhorro
from src.navegacion import ir_a
from src.sesion import Sesion

BG_FONDO = "#0a0a0f"
BG_TARJETA = "#181820"
BORDE_NEON = "#8b2fc9"
NEON_CLARO = "#a855f7"
BORDE_TARJETA = "#2d1b4e"
GRIS = "#a0a0a0"
GRIS_OSCURO = "#7a7a7a"


def _formatear_monto(monto):
    valor = f"{monto:,.2f}"
    return "$ " + valor.replace(".", "X").replace(",", ".").replace("X", ",")


def render_home_historial(page: ft.Page):
    page.title = "Capital Bank - Historial"
    page.window_width = 420
    page.window_height = 680
    page.window_resizable = False
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = BG_FONDO

    usuario = Sesion.actual()
    nombre = usuario.get("nombre", "Cliente")
    cuentas = usuario.get("cuentas", [])

    historial_column = ft.Column(spacing=6)

    # Mock: en la app real se deben obtener transacciones de los objetos Cuenta
    historial_column.controls.extend([
        ft.Text("2026-01-01 | Depósito | $100.00"),
        ft.Text("2026-01-02 | Retiro   | $50.00", color=ft.Colors.RED_700),
        ft.Text("2026-01-10 | Interés  | $2.50", color=ft.Colors.GREEN_700),
    ])

    header = ft.Row(
        vertical_alignment=ft.CrossAxisAlignment.START,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Column(
                spacing=3,
                controls=[
                    ft.Text(f"Hola, {nombre} 👋", size=22, weight=ft.FontWeight.BOLD, color="#ffffff"),
                    ft.Text("Historial de transacciones recientes", size=13, color=GRIS),
                ],
            ),
            ft.Container(width=40, height=40),
        ],
    )

    historial_card = ft.Container(
        padding=ft.Padding(18, 14, 18, 14),
        bgcolor=BG_TARJETA,
        border_radius=15,
        border=ft.border.all(1, BORDE_TARJETA),
        content=ft.Column(spacing=10, controls=[historial_column]),
    )

    bottom_nav = ft.Container(
        padding=ft.Padding(8, 8, 8, 8),
        bgcolor="#121212",
        border=ft.border.all(1, BORDE_TARJETA),
        border_radius=20,
        content=ft.Row(
            spacing=8,
            controls=[
                ft.Container(expand=True, alignment=ft.Alignment(0, 0), padding=ft.Padding(10, 8, 10, 8), content=ft.Column(spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[ft.Icon(ft.Icons.HOME, color=GRIS_OSCURO, size=22), ft.Text("Inicio", size=10, color=GRIS_OSCURO)])),
                ft.Container(expand=True, alignment=ft.Alignment(0, 0), padding=ft.Padding(10, 8, 10, 8), content=ft.Column(spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[ft.Icon(ft.Icons.SYNC_ALT, color=GRIS_OSCURO, size=22), ft.Text("Operar", size=10, color=GRIS_OSCURO)] )),
                ft.Container(expand=True, alignment=ft.Alignment(0, 0), padding=ft.Padding(10, 8, 10, 8), bgcolor=BORDE_NEON, border_radius=12, content=ft.Column(spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[ft.Icon(ft.Icons.HISTORY, color="#ffffff", size=22), ft.Text("Historial", size=10, color="#ffffff")])),
            ],
        ),
    )

    layout = ft.Column(expand=True, spacing=18, controls=[header, historial_card, bottom_nav])
    page.add(ft.Container(content=layout, padding=24, expand=True))


if __name__ == "__main__":
    from src.sesion import Sesion
    Sesion.iniciar({
        "dni": "40345678",
        "rol": "cliente",
        "nombre": "María",
        "apellido": "Fernández",
        "cuentas": [],
    })
    ft.run(render_home_historial)
