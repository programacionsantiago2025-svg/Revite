import flet as ft
from src.models.reservas import Reserva
from src.data.base_de_datos_reservas import consultar_usuarios


def procesar_reservas(funcion):
    def funcion_modificada():
        try:
            datos = consultar_usuarios()

            if not datos:
                return ft.Column(
                    controls=[ft.Text("No hay reservas")]
                )

            carros = []

            for fila in datos:
                nueva = Reserva(
                    fila[1],  
                    fila[2],  
                    fila[3],  
                    fila[4],  
                    fila[5],  
                    fila[6], 
                    fila[7],  
                )

                agregado = False

                for carro in carros:
                    if (
                        carro["hora"] == fila[5]
                        and carro["sector"] == fila[6]
                        and carro["taxi"] == fila[7]
                    ):
                        if len(carro["pasajeros"]) < 4:
                            carro["pasajeros"].append(nueva)
                            agregado = True
                            break

                if not agregado:
                    carros.append({
                        "hora": fila[5],
                        "sector": fila[6],
                        "taxi": fila[7],
                        "pasajeros": [nueva]
                    })

            return funcion(carros)

        except Exception as e:
            print("Error:", e)
            return ft.Column(
                controls=[ft.Text("Error al cargar reservas")]
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
                    ft.Text(f"🚖 Carro {i+1}", weight=ft.FontWeight.BOLD),
                    ft.Text(f"Hora: {carro['hora']}"),
                    ft.Text(f"Sector: {carro['sector']}"),
                    ft.Text(f"Taxi: {carro['taxi']}"),
                    ft.Text(f"Pasajeros: {len(carro['pasajeros'])}/4"),

                    ft.Divider(),

                    ft.Column(
                        controls=[
                            ft.Text(
                                f"- {p.get_nombre()} {p.get_apellido()} | CC: {p.get_cedula()}"
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
            ft.Text("📋 LISTA DE RESERVAS (BD)", size=20, weight=ft.FontWeight.BOLD),

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