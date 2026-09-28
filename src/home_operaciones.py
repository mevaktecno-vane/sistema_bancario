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


def _nombre_tipo(cuenta):
    if isinstance(cuenta, CuentaAhorro):
        return "Caja de Ahorro"
    if isinstance(cuenta, Cuenta):
        return "Corriente"
    return "Cuenta"


def render_home_operaciones(page: ft.Page):
    page.title = "Capital Bank - Operaciones"
    page.window_width = 420
    page.window_height = 680
    page.window_resizable = False
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = BG_FONDO

    usuario = Sesion.actual()
    nombre = usuario.get("nombre", "Cliente")
    cuentas = usuario.get("cuentas", [])

    def _aviso_construccion(mensaje):
        page.snack_bar = ft.SnackBar(
            ft.Text(mensaje, color="#ffffff"),
            bgcolor=BORDE_TARJETA,
        )
        page.snack_bar.open = True
        page.update()

    # Controles de operaciones
    dropdown_cuentas = ft.Dropdown(
        width=340,
        options=[ft.dropdown.Option(f"{_nombre_tipo(c)} - {c.get_nro_cuenta()}") for c in cuentas] if cuentas else [],
        hint_text="Seleccione una cuenta",
    )

    txt_monto = ft.TextField(label="Monto", width=340, keyboard_type=ft.KeyboardType.NUMBER)
    btn_depositar = ft.FilledButton("Depositar", width=160)
    btn_retirar = ft.FilledButton("Retirar", width=160)

    def _mostrar_notificacion(texto, color=ft.Colors.GREEN_700):
        page.snack_bar = ft.SnackBar(ft.Text(texto), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    def _operar_deposito(e):
        try:
            if not cuentas:
                _mostrar_notificacion("No hay cuentas disponibles.", ft.Colors.RED_700)
                return
            idx = dropdown_cuentas.options.index(dropdown_cuentas.value) if dropdown_cuentas.value else 0
            cuenta = cuentas[idx]
            monto = float(txt_monto.value)
            cuenta.depositar(monto)
            _mostrar_notificacion(f"Depósito de {_formatear_monto(monto)} realizado.")
        except Exception as ex:
            _mostrar_notificacion(f"Error: {ex}", ft.Colors.RED_700)

    def _operar_retiro(e):
        try:
            if not cuentas:
                _mostrar_notificacion("No hay cuentas disponibles.", ft.Colors.RED_700)
                return
            idx = dropdown_cuentas.options.index(dropdown_cuentas.value) if dropdown_cuentas.value else 0
            cuenta = cuentas[idx]
            monto = float(txt_monto.value)
            cuenta.retirar(monto)
            _mostrar_notificacion(f"Retiro de {_formatear_monto(monto)} realizado.")
        except Exception as ex:
            _mostrar_notificacion(f"Error: {ex}", ft.Colors.RED_700)

    btn_depositar.on_click = _operar_deposito
    btn_retirar.on_click = _operar_retiro

    header = ft.Row(
        vertical_alignment=ft.CrossAxisAlignment.START,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Column(
                spacing=3,
                controls=[
                    ft.Text(f"Hola, {nombre} 👋", size=22, weight=ft.FontWeight.BOLD, color="#ffffff"),
                    ft.Text("Aquí puedes realizar depósitos y retiros", size=13, color=GRIS),
                ],
            ),
            ft.Container(width=40, height=40),
        ],
    )

    operaciones_card = ft.Container(
        padding=ft.Padding(18, 14, 18, 14),
        bgcolor=BG_TARJETA,
        border_radius=15,
        border=ft.border.all(1, BORDE_TARJETA),
        content=ft.Column(spacing=12, controls=[dropdown_cuentas, txt_monto, ft.Row([btn_depositar, btn_retirar], spacing=12)]),
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
                ft.Container(expand=True, alignment=ft.Alignment(0, 0), padding=ft.Padding(10, 8, 10, 8), bgcolor=BORDE_NEON, border_radius=12, content=ft.Column(spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[ft.Icon(ft.Icons.SYNC_ALT, color="#ffffff", size=22), ft.Text("Operar", size=10, color="#ffffff")] )),
                ft.Container(expand=True, alignment=ft.Alignment(0, 0), padding=ft.Padding(10, 8, 10, 8), content=ft.Column(spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[ft.Icon(ft.Icons.HISTORY, color=GRIS_OSCURO, size=22), ft.Text("Historial", size=10, color=GRIS_OSCURO)])),
            ],
        ),
    )

    layout = ft.Column(expand=True, spacing=18, controls=[header, operaciones_card, bottom_nav])
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
    ft.run(render_home_operaciones)
