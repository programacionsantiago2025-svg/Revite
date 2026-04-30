import flet as ft
import json
from src.models.reservas import Reserva


def procesar_reservas(funcion):
    def funcion_modificada():
        try:
            with open("src/data/reservas.json", "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            carros = []
            for fila in datos:
                nueva = Reserva(
                    fila["nombre"],
                    fila["apellido"],
                    fila["cedula"],
                    fila["foto"],
                    fila["hora"],
                    fila["sector"],
                    fila["taxi"]
                )
                agregado = False
                for carro in carros:
                    if carro["hora"] == fila["hora"] and carro["sector"] == fila["sector"]:
                        if len(carro["pasajeros"]) < 4:
                            carro["pasajeros"].append(nueva)
                            agregado = True
                            break

                if not agregado:
                    carros.append({
                        "hora": fila["hora"],
                        "sector": fila["sector"],
                        "pasajeros": [nueva]
                    })

            return funcion(carros)

        except:
            return ft.Column(
                controls=[ft.Text("No hay reservas")]
            )
    return funcion_modificada


@procesar_reservas
def vista_reservas(carros):
    cards = []
    for i, carro in enumerate(carros):
        card = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK),
            content=ft.Column(
                controls=[
                    ft.Text(f"Carro {i+1}", weight=ft.FontWeight.BOLD),
                    ft.Text(f"Hora: {carro['hora']}"),
                    ft.Text(f"Sector: {carro['sector']}"),
                    ft.Text(f"Pasajeros: {len(carro['pasajeros'])}/4"),

                    ft.Column(
                        controls=[
                            ft.Text(
                                f"- {p.get_nombre()} {p.get_apellido()} | CC: {p.get_cedula()} | Taxi: {p.get_taxi()}"
                            )
                            for p in carro["pasajeros"]
                        ]
                    )
                ]
            )
        )

        cards.append(card)

    return ft.Column(
        controls=[
            ft.Text("📋 LISTA DE RESERVAS", size=20, weight=ft.FontWeight.BOLD),

            ft.GridView(
                controls=cards,
                expand=True,
                max_extent=300,
                spacing=10,
                run_spacing=10
            )
        ],
        scroll=ft.ScrollMode.AUTO
    )