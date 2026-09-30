import os
import sys

import flet as ft

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cuenta import Cuenta
from src.cuenta_ahorro import CuentaAhorro
from src.dao_cliente import DAOCliente
from src.navegacion import ir_a, crear_bottom_nav
from src.sesion import Sesion

# Temporal hasta BE-10/11 de Daniel (ver src/dao_cliente.py).
_dao = DAOCliente("sistema_bancario.db")

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

    # Controles de operaciones (key = id_cuenta para ubicar la cuenta elegida)
    dropdown_cuentas = ft.Dropdown(
        width=340,
        options=[
            ft.dropdown.Option(
                key=str(c.get_id_cuenta()),
                text=f"{_nombre_tipo(c)} - {c.get_nro_cuenta()}",
            )
            for c in cuentas
        ] if cuentas else [],
        hint_text="Seleccione una cuenta",
    )

    def _cuenta_elegida():
        if not cuentas:
            return None
        if dropdown_cuentas.value is None:
            return cuentas[0]
        for c in cuentas:
            if str(c.get_id_cuenta()) == dropdown_cuentas.value:
                return c
        return None

    txt_monto = ft.TextField(label="Monto", width=340, keyboard_type=ft.KeyboardType.NUMBER)
    btn_depositar = ft.FilledButton("Depositar", width=160)
    btn_retirar = ft.FilledButton("Retirar", width=160)

    def _mostrar_notificacion(texto, color=ft.Colors.GREEN_700):
        page.snack_bar = ft.SnackBar(ft.Text(texto), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    def _operar_deposito(e):
        try:
            cuenta = _cuenta_elegida()
            if cuenta is None:
                _mostrar_notificacion("No hay cuentas disponibles.", ft.Colors.RED_700)
                return
            monto = float(txt_monto.value)
            _dao.depositar(cuenta, monto)
            txt_monto.value = ""
            page.update()
            _mostrar_notificacion(f"Depósito de {_formatear_monto(monto)} realizado.")
        except Exception as ex:
            _mostrar_notificacion(f"Error: {ex}", ft.Colors.RED_700)

    def _operar_retiro(e):
        try:
            cuenta = _cuenta_elegida()
            if cuenta is None:
                _mostrar_notificacion("No hay cuentas disponibles.", ft.Colors.RED_700)
                return
            monto = float(txt_monto.value)
            _dao.retirar(cuenta, monto)
            txt_monto.value = ""
            page.update()
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

    bottom_nav = crear_bottom_nav(page, "operar")

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
