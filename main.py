import flet as ft
from src.app_banco import main as app_main


def main():
    ft.app(target=app_main, view=ft.WEB_BROWSER)


if __name__ == "__main__":
    main()
