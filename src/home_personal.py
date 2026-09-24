import os
import sys

import flet as ft

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.navegacion import ir_a
from src.sesion import Sesion

BG_FONDO = "#0a0a0f"
BG_TARJETA = "#181820"
BORDE_TARJETA = "#2d1b4e"
NEON_CLARO = "#a855f7"


def render_home_personal(page: ft.Page):
    page.title = "Capital Bank - Home Personal"
    page.window_width = 420
    page.window_height = 680
    page.window_resizable = False
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = BG_FONDO

    usuario = Sesion.actual()
    nombre = usuario.get("nombre", "Personal")

    def _cerrar_sesion(e):
        Sesion.cerrar()
        from src.login import render_login
        ir_a(page, render_login)

    card = ft.Container(
        width=340,
        padding=30,
        bgcolor=BG_TARJETA,
        border_radius=20,
        border=ft.border.all(1, BORDE_TARJETA),
        shadow=ft.BoxShadow(
            blur_radius=25,
            color="#8b2fc9",
            offset=ft.Offset(0, 0),
        ),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=14,
            controls=[
                ft.Text(
                    f"Hola, {nombre} 👋",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#ffffff",
                ),
                ft.Text(
                    "Bienvenido al panel del personal de Capital Bank.",
                    size=13,
                    color="#a0a0a0",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Vista en construcción (bloque de Personal).",
                    size=12,
                    italic=True,
                    color="#7a7a7a",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.OutlinedButton(
                    content=ft.Text("Cerrar sesión", size=12, color=NEON_CLARO),
                    style=ft.ButtonStyle(
                        side=ft.BorderSide(width=1, color="#8b2fc9"),
                        shape=ft.RoundedRectangleBorder(radius=18),
                        padding=ft.Padding(14, 6, 14, 6),
                    ),
                    on_click=_cerrar_sesion,
                ),
            ],
        ),
    )

    page.add(
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[card],
        )
    )


if __name__ == "__main__":
    from src.sesion import Sesion
    Sesion.iniciar({
        "dni": "22233344",
        "rol": "personal",
        "nombre": "Carlos",
        "apellido": "Gómez",
    })
    ft.run(render_home_personal)