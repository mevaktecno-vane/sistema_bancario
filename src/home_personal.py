import os
import sys

import flet as ft

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.dao_personal import DAOPersonal
from src.home_crear_cliente import render_gestion_cliente
from src.navegacion import ir_a
from src.sesion import Sesion

# Paleta de colores - Capital Bank Dark Neon
BG_FONDO = "#0a0a0f"
BG_TARJETA = "#181820"
BORDE_NEON = "#8b2fc9"
NEON_CLARO = "#a855f7"
BORDE_TARJETA = "#2d1b4e"
GRIS = "#a0a0a0"
GRIS_OSCURO = "#7a7a7a"

# Temporal: DAO para el panel de personal
_dao = DAOPersonal("sistema_bancario.db")


def _es_personal():
    usuario = Sesion.actual()
    return usuario is not None and usuario.get("rol") == "personal"


def _ir_login(page):
    from src.login import render_login
    ir_a(page, render_login)


def _aviso(page, texto, ok=True):
    page.snack_bar = ft.SnackBar(
        ft.Text(texto, color="#ffffff"),
        bgcolor=BORDE_TARJETA if ok else "#5c1d2e",
    )
    page.snack_bar.open = True
    page.update()


def render_home_personal(page: ft.Page):
    """Panel de administración y gestión de clientes con diseño neón oscuro."""
    page.title = "Capital Bank - Panel Personal"
    page.window_width = 420
    page.window_height = 680
    page.window_resizable = False
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = BG_FONDO

    if not _es_personal():
        _ir_login(page)
        return

    nombre = Sesion.actual().get("nombre", "Personal")
    clientes = _dao.obtener_todos_clientes()

    def _cerrar_sesion(e):
        Sesion.cerrar()
        _ir_login(page)

    def _nuevo_cliente(e):
        ir_a(page, render_gestion_cliente)

    # ---- Encabezado superior ----
    header = ft.Row(
        vertical_alignment=ft.CrossAxisAlignment.START,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Column(
                spacing=3,
                controls=[
                    ft.Text(
                        f"Hola, {nombre} 💼",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color="#ffffff",
                    ),
                    ft.Text(
                        "Panel de Gestión y Clientes",
                        size=13,
                        color=GRIS,
                    ),
                ],
            ),
            ft.OutlinedButton(
                content=ft.Text("Cerrar sesión", size=12, color=NEON_CLARO),
                style=ft.ButtonStyle(
                    side=ft.BorderSide(width=1, color=BORDE_NEON),
                    shape=ft.RoundedRectangleBorder(radius=18),
                    padding=ft.Padding(14, 6, 14, 6),
                ),
                on_click=_cerrar_sesion,
            ),
        ],
    )

    # ---- Resumen / Control superior ----
    resumen_control = ft.Container(
        padding=ft.Padding(18, 14, 18, 14),
        bgcolor=BG_TARJETA,
        border_radius=15,
        border=ft.border.all(1, BORDE_TARJETA),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Clientes registrados", size=14, color=GRIS),
                ft.Container(
                    content=ft.Text(
                        f"{len(clientes)}",
                        size=15,
                        weight=ft.FontWeight.BOLD,
                        color=NEON_CLARO,
                    ),
                    padding=ft.Padding(12, 4, 12, 4),
                    bgcolor=BORDE_TARJETA,
                    border_radius=12,
                ),
            ],
        ),
    )

    # ---- Constructor de tarjetas de clientes ----
    def _construir_tarjeta_cliente(id_cliente, nom, ape, dni, categoria, estado):
        try:
            n_cuentas = len(_dao.obtener_cuentas_por_cliente(id_cliente))
        except Exception:
            n_cuentas = "?"

        es_activo = str(estado).strip().lower() == "activo"

        return ft.Container(
            padding=16,
            bgcolor=BG_TARJETA,
            border_radius=15,
            border=ft.border.all(1, BORDE_TARJETA),
            shadow=ft.BoxShadow(
                blur_radius=12,
                color=BORDE_NEON,
                offset=ft.Offset(0, 0),
            ),
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(
                                f"{ape}, {nom}",
                                size=15,
                                weight=ft.FontWeight.BOLD,
                                color="#ffffff",
                            ),
                            ft.Container(
                                content=ft.Text(
                                    str(estado).lower(),
                                    size=10,
                                    weight=ft.FontWeight.BOLD,
                                    color=NEON_CLARO if es_activo else GRIS,
                                ),
                                padding=ft.Padding(8, 2, 8, 2),
                                bgcolor=BORDE_TARJETA,
                                border_radius=10,
                            ),
                        ],
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text(f"DNI: {dni}", size=12, color=GRIS),
                                    ft.Text(
                                        f"Categoría: {categoria} · Cuentas: {n_cuentas}",
                                        size=11,
                                        color=GRIS_OSCURO,
                                    ),
                                ],
                            ),
                            ft.OutlinedButton(
                                content=ft.Text("Gestionar", size=11, color=NEON_CLARO),
                                style=ft.ButtonStyle(
                                    side=ft.BorderSide(width=1, color=BORDE_NEON),
                                    shape=ft.RoundedRectangleBorder(radius=14),
                                    padding=ft.Padding(10, 4, 10, 4),
                                ),
                                on_click=lambda e, d=dni: ir_a(
                                    page, lambda p: render_gestion_cliente(p, dni=d)
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        )

    # ---- Lista o estado vacío ----
    if clientes:
        lista_clientes = ft.Column(
            spacing=12,
            controls=[_construir_tarjeta_cliente(*c) for c in clientes],
        )
    else:
        lista_clientes = ft.Container(
            padding=30,
            alignment=ft.alignment.center,
            content=ft.Text(
                "No hay clientes registrados en el sistema.",
                size=13,
                color=GRIS_OSCURO,
                text_align=ft.TextAlign.CENTER,
            ),
        )

    # ---- Botón de acción principal ----
    btn_crear = ft.ElevatedButton(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.PERSON_ADD_ALT_1_ROUNDED, color="#ffffff", size=18),
                ft.Text("Crear nuevo cliente", color="#ffffff", weight=ft.FontWeight.BOLD),
            ],
        ),
        bgcolor=BORDE_NEON,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=16),
            padding=ft.Padding(0, 14, 0, 14),
        ),
        on_click=_nuevo_cliente,
    )

    # ---- Scroll central ----
    contenido_central = ft.Column(
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True,
        spacing=14,
        controls=[lista_clientes],
    )

    layout = ft.Column(
        expand=True,
        spacing=16,
        controls=[
            header,
            resumen_control,
            contenido_central,
            btn_crear,
        ],
    )

    page.add(ft.Container(content=layout, padding=24, expand=True))


if __name__ == "__main__":
    from src.sesion import Sesion
    Sesion.iniciar({
        "dni": "22233344",
        "rol": "personal",
        "nombre": "Carlos",
        "apellido": "Gómez",
        "cuentas": [],
    })
    ft.app(target=render_home_personal)