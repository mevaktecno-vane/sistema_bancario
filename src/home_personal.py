import os
import sys

import flet as ft

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.dao_personal import DAOPersonal
from src.home_crear_cliente import render_gestion_cliente
from src.navegacion import ir_a
from src.sesion import Sesion

# Temporal: subclase del DAO con lo que el panel necesita hasta que
# BE-07/08/09 se reescriban (ver src/dao_personal.py).
_dao = DAOPersonal("sistema_bancario.db")


def _es_personal():
    usuario = Sesion.actual()
    return usuario is not None and usuario.get("rol") == "personal"


def _ir_login(page):
    from src.login import render_login
    ir_a(page, render_login)


def _aviso(page, texto, ok=True):
    page.snack_bar = ft.SnackBar(
        ft.Text(texto),
        bgcolor=ft.Colors.GREEN_700 if ok else ft.Colors.RED_700,
    )
    page.snack_bar.open = True
    page.update()


def render_home_personal(page: ft.Page):
    """Home del personal: lista de usuarios. Sin diseño: controles por defecto."""
    page.title = "Capital Bank - Personal"
    page.bgcolor = ft.Colors.WHITE
    page.scroll = ft.ScrollMode.ADAPTIVE

    if not _es_personal():
        _ir_login(page)
        return
    nombre = Sesion.actual().get("nombre", "Personal")

    clientes = _dao.obtener_todos_clientes()

    filas = [ft.Text(f"Hola, {nombre} (personal)")]
    filas.append(ft.Text(f"Clientes: {len(clientes)}"))
    for id_cliente, nom, ape, dni, categoria, estado in clientes:
        try:
            n_cuentas = len(_dao.obtener_cuentas_por_cliente(id_cliente))
        except Exception:
            n_cuentas = "?"

        def _abrir(e, d=dni):
            ir_a(page, lambda p: render_gestion_cliente(p, dni=d))

        filas.append(ft.Row(controls=[
            ft.Text(f"{ape}, {nom} - DNI {dni} - {categoria}/{estado} - cuentas: {n_cuentas}"),
            ft.TextButton("Gestionar", on_click=_abrir),
        ]))

    def _nuevo(e):
        ir_a(page, render_gestion_cliente)

    def _cerrar(e):
        Sesion.cerrar()
        _ir_login(page)

    filas.append(ft.ElevatedButton("Crear cliente", on_click=_nuevo))
    filas.append(ft.TextButton("Cerrar sesión", on_click=_cerrar))

    page.add(ft.Column(controls=filas))


if __name__ == "__main__":
    from src.sesion import Sesion
    Sesion.iniciar({
        "dni": "22233344",
        "rol": "personal",
        "nombre": "Carlos",
        "apellido": "Gómez",
        "cuentas": [],
    })
    ft.run(render_home_personal)
