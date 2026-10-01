import os
import sys

import flet as ft

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cliente import Cliente
from src.dao_personal import DAOPersonal
from src.navegacion import ir_a
from src.sesion import Sesion


# Temporal: subclase del DAO con lo que el panel necesita hasta que
# BE-07/08/09 se reescriban (ver src/dao_personal.py).
_dao = DAOPersonal("sistema_bancario.db")


def _resolver_tipo(nombre_tipo):
    try:
        return _dao.guardar_tipo_cuenta(nombre_tipo)
    except ValueError:
        from sqlalchemy import select
        from src.models import TipoCuentaModel

        with _dao.connect() as s:
            row = s.scalar(
                select(TipoCuentaModel).where(
                    TipoCuentaModel.nombre == nombre_tipo
                )
            )
            return row.id_tipo_cuenta if row is not None else None


def render_gestion_cliente(page: ft.Page, dni=None):
    """
    Crear/editar cliente con sus cuentas.
    Mantiene la lógica original y aplica el diseño visual de Capital Bank.
    """

    # Imports diferidos: home_personal importa este módulo a nivel superior,
    # así se evita el ciclo home_personal <-> home_crear_cliente.
    from src.home_personal import _aviso, _es_personal, _ir_login

    # =====================================================
    # CONFIGURACIÓN GENERAL
    # =====================================================

    page.title = "Capital Bank - Gestión cliente"
    page.bgcolor = "#0a0a0f"
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    if not _es_personal():
        _ir_login(page)
        return

    es_nuevo = dni is None
    datos = None if es_nuevo else _dao.obtener_cliente_por_dni(dni)

    if not es_nuevo and datos is None:
        _aviso(page, "No existe un cliente con ese DNI.", ok=False)
        from src.home_personal import render_home_personal
        ir_a(page, render_home_personal)
        return

    id_cliente = None if es_nuevo else datos[0]

    # =====================================================
    # ESTILO CAPITAL BANK
    # =====================================================

    def campo(label, value="", password=False):
        return ft.TextField(
            label=label,
            value=value,
            password=password,
            can_reveal_password=password,
            label_style=ft.TextStyle(color="#a0a0a0"),
            text_style=ft.TextStyle(color="#ffffff"),
            bgcolor="#121212",
            border_color="#8b2fc9",
            focused_border_color="#a855f7",
            border_radius=18,
            content_padding=ft.Padding(
                18,
                12,
                18,
                12,
            ),
        )

    def boton_principal(texto, funcion):
        return ft.ElevatedButton(
            texto,
            on_click=funcion,
            bgcolor="#8b2fc9",
            color="#ffffff",
            width=400,
            height=45,
        )

    def texto_secundario(texto, size=13):
        return ft.Text(
            texto,
            size=size,
            color="#a0a0a0",
        )

    # =====================================================
    # DATOS DEL CLIENTE
    # =====================================================

    txt_nombre = campo(
        "Nombre",
        value="" if es_nuevo else datos[1],
    )

    txt_apellido = campo(
        "Apellido",
        value="" if es_nuevo else datos[2],
    )

    txt_dni = campo(
        "DNI",
        value="" if es_nuevo else datos[3],
    )

    txt_clave = campo(
        "Clave nueva (vacío = no cambia)"
        if not es_nuevo
        else "Clave inicial",
        password=True,
    )

    titulo_cliente = ft.Text(
        "Nuevo cliente"
        if es_nuevo
        else f"Cliente {datos[1]} {datos[2]}",
        size=28,
        weight=ft.FontWeight.BOLD,
        color="#ffffff",
        text_align=ft.TextAlign.CENTER,
    )

    def _guardar_cliente(e):
        nonlocal es_nuevo, id_cliente, datos

        try:
            nombre = (txt_nombre.value or "").strip()
            apellido = (txt_apellido.value or "").strip()
            nuevo_dni = (txt_dni.value or "").strip()
            clave = (txt_clave.value or "").strip() or None

            if es_nuevo:
                id_cliente = _dao.guardar_cliente(
                    Cliente(
                        nombre,
                        apellido,
                        nuevo_dni,
                        password=clave,
                    )
                )
                _aviso(
                    page,
                    f"Cliente creado con id {id_cliente}.",
                )

            else:
                Cliente(
                    nombre,
                    apellido,
                    nuevo_dni,
                )  # valida formato

                ok = _dao.actualizar_persona_por_dni(
                    datos[3],
                    nombre.title(),
                    apellido.title(),
                    nuevo_dni,
                    password=clave,
                )

                if not ok:
                    _aviso(
                        page,
                        "El cliente ya no existe.",
                        ok=False,
                    )
                    return

                _aviso(
                    page,
                    "Cliente actualizado.",
                )

            txt_clave.value = ""
            es_nuevo = False
            datos = _dao.obtener_cliente_por_dni(nuevo_dni)
            id_cliente = datos[0]

            titulo_cliente.value = (
                f"Cliente {datos[1]} {datos[2]}"
            )
            txt_clave.label = "Clave nueva (vacío = no cambia)"

            _recargar_cuentas()
            page.update()

        except ValueError as ex:
            _aviso(
                page,
                str(ex),
                ok=False,
            )

    # =====================================================
    # CUENTAS DEL CLIENTE
    # =====================================================

    col_cuentas = ft.Column(
        spacing=8,
    )

    txt_nro = campo(
        "Número de cuenta",
    )

    txt_saldo = campo(
        "Saldo inicial",
    )

    dd_tipo = ft.Dropdown(
        label="Tipo",
        options=[
            ft.dropdown.Option("Ahorro"),
            ft.dropdown.Option("Corriente"),
        ],
        bgcolor="#121212",
        border_color="#8b2fc9",
        focused_border_color="#a855f7",
        border_radius=18,
        color="#ffffff",
    )

    def _recargar_cuentas():
        col_cuentas.controls.clear()

        if id_cliente is None:
            col_cuentas.controls.append(
                texto_secundario(
                    "Guardá el cliente para agregar cuentas."
                )
            )
            return

        cuentas = _dao.obtener_cuentas_por_cliente(
            id_cliente
        )

        if not cuentas:
            col_cuentas.controls.append(
                texto_secundario(
                    "Sin cuentas registradas."
                )
            )
            return

        for id_cta, nro, _, id_tipo, saldo, tasa, _ in cuentas:
            col_cuentas.controls.append(
                ft.Container(
                    padding=12,
                    bgcolor="#121212",
                    border_radius=12,
                    border=ft.border.all(
                        1,
                        "#2d1b4e",
                    ),
                    content=ft.Row(
                        controls=[
                            ft.Text(
                                str(nro),
                                color="#ffffff",
                                weight=ft.FontWeight.BOLD,
                                expand=True,
                            ),
                            ft.Text(
                                f"Saldo: {saldo}",
                                color="#a855f7",
                            ),
                        ]
                    ),
                )
            )

    def _agregar_cuenta(e):
        try:
            if id_cliente is None:
                _aviso(
                    page,
                    "Guardá el cliente primero.",
                    ok=False,
                )
                return

            nro = (txt_nro.value or "").strip()
            nombre_tipo = dd_tipo.value

            if not nro or not nombre_tipo:
                _aviso(
                    page,
                    "Completá número y tipo.",
                    ok=False,
                )
                return

            try:
                saldo = float(
                    (txt_saldo.value or "0").strip()
                    or 0
                )

            except ValueError:
                _aviso(
                    page,
                    "El saldo debe ser un número.",
                    ok=False,
                )
                return

            if saldo < 0:
                _aviso(
                    page,
                    "El saldo no puede ser negativo.",
                    ok=False,
                )
                return

            id_tipo = _resolver_tipo(
                nombre_tipo
            )

            if id_tipo is None:
                _aviso(
                    page,
                    "No se pudo resolver el tipo de cuenta.",
                    ok=False,
                )
                return

            id_cta = _dao.guardar_cuenta(
                nro,
                id_cliente,
                id_tipo,
                saldo=saldo,
            )

            _aviso(
                page,
                f"Cuenta {nro} creada con id {id_cta}.",
            )

            txt_nro.value = ""
            txt_saldo.value = ""
            dd_tipo.value = None

            _recargar_cuentas()
            page.update()

        except ValueError as ex:
            _aviso(
                page,
                str(ex),
                ok=False,
            )

    def _volver(e):
        from src.home_personal import render_home_personal
        ir_a(
            page,
            render_home_personal,
        )

    _recargar_cuentas()

    # =====================================================
    # TARJETAS
    # =====================================================

    tarjeta_cliente = ft.Container(
        width=450,
        padding=25,
        bgcolor="#181820",
        border_radius=20,
        border=ft.border.all(
            1,
            "#2d1b4e",
        ),
        content=ft.Column(
            spacing=15,
            controls=[
                ft.Text(
                    "Datos del cliente",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="#ffffff",
                ),
                ft.Text(
                    "CAPITAL BANK",
                    size=12,
                    color="#a855f7",
                ),
                txt_nombre,
                txt_apellido,
                txt_dni,
                txt_clave,
                boton_principal(
                    "GUARDAR CLIENTE",
                    _guardar_cliente,
                ),
            ],
        ),
    )

    tarjeta_cuentas = ft.Container(
        width=450,
        padding=25,
        bgcolor="#181820",
        border_radius=20,
        border=ft.border.all(
            1,
            "#2d1b4e",
        ),
        content=ft.Column(
            spacing=15,
            controls=[
                ft.Text(
                    "Cuentas",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="#ffffff",
                ),
                ft.Text(
                    "CUENTAS DEL CLIENTE",
                    size=12,
                    color="#a855f7",
                ),
                col_cuentas,
                ft.Divider(
                    color="#2d1b4e",
                    height=20,
                ),
                txt_nro,
                dd_tipo,
                txt_saldo,
                boton_principal(
                    "AGREGAR CUENTA",
                    _agregar_cuenta,
                ),
            ],
        ),
    )

    # =====================================================
    # PANTALLA
    # =====================================================

    page.add(
        ft.Container(
            padding=30,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    titulo_cliente,
                    ft.Text(
                        "Capital Bank",
                        size=14,
                        color="#a855f7",
                    ),
                    tarjeta_cliente,
                    tarjeta_cuentas,
                    ft.TextButton(
                        content=ft.Text(
                            "← VOLVER",
                            color="#a855f7",
                            weight=ft.FontWeight.BOLD,
                        ),
                        on_click=_volver,
                    ),
                    ft.Text(
                        "© 2026 Capital Bank",
                        size=11,
                        color="#555566",
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    Sesion.iniciar(
        {
            "dni": "22233344",
            "rol": "personal",
            "nombre": "Carlos",
            "apellido": "Gómez",
            "cuentas": [],
        }
    )

    ft.run(render_gestion_cliente)
