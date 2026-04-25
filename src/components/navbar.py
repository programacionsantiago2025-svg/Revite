import flet as ft

def navbar(on_change):
    return ft.Container(
        bgcolor=ft.Colors.BLUE_GREY_700,
        padding=10,
        border_radius=10,
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.TextButton(
                            content="Inicio",
                            icon=ft.Icons.SEARCH_ROUNDED,
                            style=ft.TextStyle(color="black"),
                            on_click=lambda e: on_change("inicio"),
                            
                        ),
                        ft.TextButton(
                            content="Ver reservas",
                            icon=ft.Icons.SEARCH_ROUNDED,
                            style = ft.TextStyle(color="black"),
                            on_click=lambda e: on_change("reservas"),
                        ),
                        ft.TextButton(
                            content="Crear carro",
                            icon=ft.Icons.SEARCH_ROUNDED,
                            style = ft.TextStyle(color="black"),
                            on_click=lambda e: on_change("carro"),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    expand=True
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    )