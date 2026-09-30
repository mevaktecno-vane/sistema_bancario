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


def _resolver_tipo(nombre_tipo):
    try:
        return _dao.guardar_tipo_cuenta(nombre_tipo)
    except ValueError:
        from sqlalchemy import select
        from src.models import TipoCuentaModel
        with _dao.connect() as s:
            row = s.scalar(select(TipoCuentaModel).where(
                TipoCuentaModel.nombre == nombre_tipo))
            return row.id_tipo_cuenta if row is not None else None


def render_home_personal(page: ft.Page):
    """Lista de usuarios. Sin diseño: controles por defecto."""
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


def render_gestion_cliente(page: ft.Page, dni=None):
    """Una sola pantalla: crear/editar cliente + sus cuentas. Sin diseño."""
    page.title = "Capital Bank - Gestión cliente"
    page.bgcolor = ft.Colors.WHITE
    page.scroll = ft.ScrollMode.ADAPTIVE

    if not _es_personal():
        _ir_login(page)
        return

    es_nuevo = dni is None
    datos = None if es_nuevo else _dao.obtener_cliente_por_dni(dni)
    if not es_nuevo and datos is None:
        _aviso(page, "No existe un cliente con ese DNI.", ok=False)
        ir_a(page, render_home_personal)
        return

    id_cliente = None if es_nuevo else datos[0]

    txt_nombre = ft.TextField(label="Nombre", value="" if es_nuevo else datos[1])
    txt_apellido = ft.TextField(label="Apellido", value="" if es_nuevo else datos[2])
    txt_dni = ft.TextField(label="DNI", value="" if es_nuevo else datos[3])
    txt_clave = ft.TextField(label="Clave nueva (vacío = no cambia)" if not es_nuevo else "Clave inicial",
                             password=True)

    def _guardar_cliente(e):
        nonlocal es_nuevo, id_cliente, datos
        try:
            nombre = (txt_nombre.value or "").strip()
            apellido = (txt_apellido.value or "").strip()
            nuevo_dni = (txt_dni.value or "").strip()
            clave = (txt_clave.value or "").strip() or None
            if es_nuevo:
                id_cliente = _dao.guardar_cliente(
                    Cliente(nombre, apellido, nuevo_dni, password=clave))
                _aviso(page, f"Cliente creado con id {id_cliente}.")
            else:
                Cliente(nombre, apellido, nuevo_dni)  # valida formato
                ok = _dao.actualizar_persona_por_dni(
                    datos[3], nombre.title(), apellido.title(), nuevo_dni,
                    password=clave)
                if not ok:
                    _aviso(page, "El cliente ya no existe.", ok=False)
                    return
                _aviso(page, "Cliente actualizado.")
            txt_clave.value = ""
            es_nuevo = False
            datos = _dao.obtener_cliente_por_dni(nuevo_dni)
            id_cliente = datos[0]
            _recargar_cuentas()
            page.update()
        except ValueError as ex:
            _aviso(page, str(ex), ok=False)

    # ---------- Cuentas del cliente ----------
    col_cuentas = ft.Column()
    txt_nro = ft.TextField(label="Número de cuenta")
    txt_saldo = ft.TextField(label="Saldo inicial")
    dd_tipo = ft.Dropdown(
        label="Tipo",
        options=[ft.dropdown.Option("Ahorro"), ft.dropdown.Option("Corriente")],
    )

    def _recargar_cuentas():
        col_cuentas.controls.clear()
        if id_cliente is None:
            col_cuentas.controls.append(ft.Text("Guardá el cliente para agregar cuentas."))
            return
        cuentas = _dao.obtener_cuentas_por_cliente(id_cliente)
        if not cuentas:
            col_cuentas.controls.append(ft.Text("Sin cuentas."))
        for id_cta, nro, _, id_tipo, saldo, tasa, _ in cuentas:
            col_cuentas.controls.append(ft.Text(f"{nro} - saldo {saldo}"))

    def _agregar_cuenta(e):
        try:
            if id_cliente is None:
                _aviso(page, "Guardá el cliente primero.", ok=False)
                return
            nro = (txt_nro.value or "").strip()
            nombre_tipo = dd_tipo.value
            if not nro or not nombre_tipo:
                _aviso(page, "Completá número y tipo.", ok=False)
                return
            try:
                saldo = float((txt_saldo.value or "0").strip() or 0)
            except ValueError:
                _aviso(page, "El saldo debe ser un número.", ok=False)
                return
            if saldo < 0:
                _aviso(page, "El saldo no puede ser negativo.", ok=False)
                return
            id_tipo = _resolver_tipo(nombre_tipo)
            if id_tipo is None:
                _aviso(page, "No se pudo resolver el tipo de cuenta.", ok=False)
                return
            id_cta = _dao.guardar_cuenta(nro, id_cliente, id_tipo, saldo=saldo)
            _aviso(page, f"Cuenta {nro} creada con id {id_cta}.")
            txt_nro.value = ""
            txt_saldo.value = ""
            dd_tipo.value = None
            _recargar_cuentas()
            page.update()
        except ValueError as ex:
            _aviso(page, str(ex), ok=False)

    def _volver(e):
        ir_a(page, render_home_personal)

    _recargar_cuentas()

    page.add(ft.Column(controls=[
        ft.Text("Nuevo cliente" if es_nuevo else f"Cliente {datos[1]} {datos[2]}"),
        txt_nombre,
        txt_apellido,
        txt_dni,
        txt_clave,
        ft.ElevatedButton("Guardar cliente", on_click=_guardar_cliente),
        ft.Text("Cuentas"),
        col_cuentas,
        txt_nro,
        dd_tipo,
        txt_saldo,
        ft.ElevatedButton("Agregar cuenta", on_click=_agregar_cuenta),
        ft.TextButton("Volver", on_click=_volver),
    ]))


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
