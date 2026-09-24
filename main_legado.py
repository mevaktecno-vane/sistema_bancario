import flet as ft

from src.app_banco import main as app_gui


def main():
    ft.app(target=app_gui, view=ft.WEB_BROWSER, port=8551)


if __name__ == "__main__":
    main()