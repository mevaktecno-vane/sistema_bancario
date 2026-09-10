import os
import flet as ft

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO_PATH = os.path.join(BASE_DIR, "img", "logo_clean.png")

def render_login(page: ft.Page):
    page.title = "Capital Bank - Login"
    page.window_width = 420
    page.window_height = 680
    page.window_resizable = False
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = "#0a0a0f"

    dni_input = ft.TextField(
        hint_text="DNI",
        hint_style=ft.TextStyle(color="#7a7a7a"),
        text_style=ft.TextStyle(color="#ffffff"),
        bgcolor="#121212",
        border_color="#8b2fc9",
        focused_border_color="#a855f7",
        border_radius=25,
        content_padding=ft.Padding(20, 12, 20, 12),
        text_align=ft.TextAlign.CENTER,
    )

    clave_input = ft.TextField(
        hint_text="CLAVE",
        password=True,
        can_reveal_password=True,
        hint_style=ft.TextStyle(color="#7a7a7a"),
        text_style=ft.TextStyle(color="#ffffff"),
        bgcolor="#121212",
        border_color="#8b2fc9",
        focused_border_color="#a855f7",
        border_radius=25,
        content_padding=ft.Padding(20, 12, 20, 12),
        text_align=ft.TextAlign.CENTER,
    )

    def on_login_click(e):
        dni = dni_input.value
        clave = clave_input.value

        if not dni or not clave:
            mostrar_mensaje("Por favor ingresa tu DNI y Clave", es_error=True)
            return

        mostrar_mensaje(f"Iniciando sesión con DNI: {dni}...", es_error=False)

    def mostrar_mensaje(texto, es_error=False):
        page.snack_bar = ft.SnackBar(
            ft.Text(texto),
            bgcolor="red" if es_error else "green"
        )
        page.snack_bar.open = True
        page.update()

    btn_ingresar = ft.Button(
        content=ft.Text("INGRESAR", size=15, weight=ft.FontWeight.BOLD, color="#ffffff"),
        on_click=on_login_click,
        style=ft.ButtonStyle(
            bgcolor="#8b2fc9",
            padding=ft.Padding(0, 15, 0, 15),
            shape=ft.RoundedRectangleBorder(radius=25),
            elevation=5
        ),
        width=300
    )

    btn_olvido = ft.TextButton(
        content=ft.Text("¿Olvidaste tu clave?", size=12, color="#a855f7"),
        on_click=lambda _: mostrar_mensaje("Contacta a soporte técnico", es_error=False)
    )

    login_card = ft.Container(
        width=340,
        padding=30,
        bgcolor="#181820",
        border_radius=20,
        border=ft.Border.all(1, "#2d1b4e"),
        shadow=ft.BoxShadow(
            blur_radius=25,
            color="#8b2fc9",
            offset=ft.Offset(0, 0)
        ),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=18,
            controls=[
                ft.Container(
                    content=ft.Image(
                        src=LOGO_PATH,
                        width=140,
                        height=140,
                        fit="contain",
                    ),
                    alignment=ft.Alignment(0, 0),
                    width=280
                ),
                ft.Container(height=2),
                dni_input,
                clave_input,
                ft.Container(height=2),
                btn_ingresar,
                btn_olvido
            ]
        )
    )

    footer = ft.Text(
        "© 2026 Capital Bank • Sistema Bancario Seguro",
        size=11,
        color="#555566",
        text_align=ft.TextAlign.CENTER
    )

    main_layout = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=25,
        controls=[
            login_card,
            footer
        ]
    )

    page.add(main_layout)

if __name__ == "__main__":
    ft.run(render_login)