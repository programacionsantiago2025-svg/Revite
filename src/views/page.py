import flet as ft
import csv
import json
import os
from src.models.reservas import Reserva, guardar_json
from src.components.navbar import navbar
from src.views.page2 import vista_reservas
from src.models.carro import Carro, guardar_json_carro
from src.data.base_de_datos_reservas import crear_base_de_datos_reservas,insertar_reserva
from src.data.base_de_datos_cliente import crear_base_de_datos_cliente,insertar_cliente
from src.data.base_de_datos_carros import crear_base_de_datos_carros,insertar_carro,consultar_carros
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
def main(page: ft.Page):
    page.title = "Mi App Principal"
    page.bgcolor = ft.Colors.BLUE_GREY_500
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    horarios = ["6:00", "6:30", "7:00", "9:30"]
    titulo = ft.Text("AGENDA TU DESTINO", size=20, weight=ft.FontWeight.BOLD)
    checks = []
    sectores = []
    contenido = ft.Column()
    carros = ["ABC123", "DEF456", "GHI789", "JKL012"]
    input_cedula = ft.TextField(label="Cedula", hint_text="1070600370", width=300,bgcolor=ft.Colors.WHITE,border_radius=10,color=ft.Colors.BLACK,icon=ft.Icons.INFO_ROUNDED)
    input_nombre = ft.TextField(label="Nombre", hint_text="Santiago", width=300,bgcolor=ft.Colors.WHITE,border_radius=10,color=ft.Colors.BLACK,icon=ft.Icons.INFO_ROUNDED)
    input_direccion = ft.TextField(label="Direccion", hint_text="Calle... Barrio...", width=300,bgcolor=ft.Colors.WHITE,border_radius=10,color=ft.Colors.BLACK,icon=ft.Icons.INFO_ROUNDED)
    input_celular = ft.TextField(label="Celular", hint_text="3133017419", width=300,bgcolor=ft.Colors.WHITE,border_radius=10,color=ft.Colors.BLACK,icon=ft.Icons.INFO_ROUNDED)
    input_placa = ft.TextField(label="Placa", width=200, bgcolor=ft.Colors.WHITE,icon=ft.Icons.ABC)
    input_marca = ft.TextField(label="Marca", width=200, bgcolor=ft.Colors.WHITE, icon= ft.Icons.SEARCH)
    input_modelo = ft.TextField(label="Modelo", width=200, bgcolor=ft.Colors.WHITE, icon= ft.Icons.ABC)
    input_capacidad = ft.TextField(label="capacidad", width=200, bgcolor=ft.Colors.WHITE, icon= ft.Icons.ABC)
    check_mantenimiento = ft.Checkbox(label="En mantenimiento:")
    texto_taxi = ft.Text("NO CARRO SELECCIONADO")
    imagen = ft.Image(
        src = "./assets/persona.png",
        width= 200,
        height = 200
    )
    def seleccionar_taxi(e):
        texto_taxi.value = f"Carro seleccionado: {e.control.data}"
        page.update()
    def crear_reserva_args(*args):
        nueva = Reserva(
            args[0],
            args[1],
            args[2],
            args[3],
            args[4],
            args[5],
            args[6]
    )
        guardar_json(
            nombre=nueva.get_nombre(),
            apellido=nueva.get_apellido(),
            cedula=nueva.get_cedula(),
            foto=nueva.foto,
            hora=nueva.get_hora(),
            sector=nueva.get_sector(),
            taxi=nueva.get_taxi()
    )
    def crear_reserva():
        nombre = input_nombre.value
        cedula = input_cedula.value
        foto = imagen.src
        sector = radios.value
        hora = None
        taxi_seleccionado = texto_taxi.value

        for check in checks:
            if check.value:  
                hora = check.label
                break

        if not nombre or not cedula or not sector or not hora:
            page.snack_bar = ft.SnackBar(ft.Text("Complete todos los campos"))
            page.snack_bar.open = True
            page.update()
            return

        crear_reserva_args(
            nombre,
            "",  
            cedula,
            foto,
            hora,
            sector,
            taxi_seleccionado
        )
        insertar_cliente(nombre, "", cedula, foto)
        insertar_reserva(nombre, "", cedula, foto, hora, sector, taxi_seleccionado)
        page.snack_bar = ft.SnackBar(ft.Text(f"Reserva creada para {nombre}"))
        page.snack_bar.open = True
        page.update()
    async def handle_pick_files(e):
        picker = ft.FilePicker()
        files = await picker.pick_files(allow_multiple=False)
        if files:
            imagen.src = files[0].path
    def crear_carro():
        placa = input_placa.value
        marca = input_marca.value
        modelo = input_modelo.value
        mantenimiento = check_mantenimiento.value
        capacidad = input_capacidad.value
        nuevo_carro = Carro(placa, marca, modelo, mantenimiento, capacidad)
        guardar_json_carro(nuevo_carro)
        insertar_carro(placa, marca, modelo, mantenimiento, capacidad)
        nuevo_cuadro = ft.Container(
            width=150,
            height=100,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(color=ft.Colors.BLACK, blur_radius=20),
            border_radius=10,
            padding=10,
            data=placa,
            on_click=seleccionar_taxi,
            content=ft.Column(
                controls=[
                    ft.Text(f"{marca} - {placa} - Capacidad: {capacidad}", weight=ft.FontWeight.BOLD)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        contenedor_principal.controls.insert(-1, nuevo_cuadro)

        page.update()

    with open("src/data/destinos.json", "r", encoding="utf-8") as archivo:
        sectores = json.load(archivo)
    """
    with open("src/data/carros.json", "r", encoding="utf-8") as archivo:
        carros = json.load(archivo)
    """
    carros = []
    datos_bd = consultar_carros()

    for carro in datos_bd:
        carros.append({
            "placa": carro[1],
            "marca": carro[2],
            "capacidad": carro[5]
        })
    
    for hora in horarios:
        check = ft.Checkbox(label=hora)
        checks.append(check)
    col1 = ft.Column(
        controls=[
            input_cedula,
            input_nombre,
            input_direccion,
            input_celular,
        ],
    )
    col2 = ft.Container(
        width=200,
        height=250,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        shadow = ft.BoxShadow(color= ft.Colors.BLACK,blur_radius=20),
        content=ft.Column(
            controls=[
                imagen,
                ft.ElevatedButton("Cargar foto",on_click=handle_pick_files,),
            ],
            alignment=ft.MainAxisAlignment.END,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    lista_horarios = ft.Column(
        controls=[
            ft.Text("Horarios", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                bgcolor = ft.Colors.WHITE,
                padding=10,
                border_radius=10,
                content=ft.Column(controls=checks)
            )
        ],
        spacing=10
    )
    seccion_carros = ft.Container(
        margin= 50,
        content=ft.Column(
        controls=[
            ft.Text("REGISTRAR CARRO", size=18, weight=ft.FontWeight.BOLD),
            input_placa,
            input_marca,
            input_modelo,
            input_capacidad,
            check_mantenimiento,
            ft.ElevatedButton("Guardar carro", on_click=lambda e: crear_carro())
        ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment= ft.CrossAxisAlignment.CENTER
    ),
    bgcolor=ft.Colors.GREY_400,
    border_radius= 20,
    width= 250,
    padding= 10
    )

    radios = ft.RadioGroup(
        content=ft.ListView(
            controls=[ft.Radio(label=s, value=s) for s in sectores],
            spacing=5
        ),
        value=None  
    )

    cuadro_sectores = ft.Container(
        width=300,
        height=200,
        padding=10,
        border_radius=8,
        shadow = ft.BoxShadow(color= ft.Colors.BLACK,blur_radius=20),
        content=radios,
        bgcolor= ft.Colors.WHITE
        
    )
    cuadros = []

    for carro in carros:
        cuadro = ft.Container(
            width=150,
            height=100,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(color=ft.Colors.BLACK, blur_radius=20),
            border_radius=10,
            padding=10,
            data=f"{carro['marca']} - {carro['placa']}",
            on_click=seleccionar_taxi,
            content=ft.Column(
                controls=[
                    ft.Text(
                        f"{carro['marca']} - {carro['placa']}",
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Text(f"Capacidad: {carro['capacidad']}")
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        cuadros.append(cuadro)
    filas_carros = []

    for i in range(0, len(cuadros), 2):
        fila = ft.Row(
            controls=cuadros[i:i+2],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            spacing=10
        )
        filas_carros.append(fila)
    contenedor_principal = ft.Column(
        controls=filas_carros + [texto_taxi],
        spacing=10
    )
    

    def vista_inicio():
        return ft.Column(
            controls=[
                ft.Row(
                    controls=[titulo],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=[col1, col2],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                ft.Row(
                    controls=[lista_horarios, cuadro_sectores, contenedor_principal],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Base de datos clientes", on_click= lambda e: crear_base_de_datos_cliente()),
                        ft.ElevatedButton("Base de datos reservas", on_click= lambda e: crear_base_de_datos_reservas()),
                        ft.ElevatedButton("Base de datos carros", on_click= lambda e: crear_base_de_datos_carros()),
                        ft.ElevatedButton(
                            "Crear reserva",
                            on_click=lambda e: crear_reserva()
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                ),
            ]  
        )
    def vista_carro():
        return ft.Column(
            controls=[
                ft.Row(
                    controls=[seccion_carros],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ]
        )
    def cambiar_vista(vista):
        if vista == "inicio":
            contenido.controls = [vista_inicio()]
        elif vista == "reservas":
            contenido.controls = [vista_reservas()]
        elif vista == "carro":
            contenido.controls = [vista_carro()]
        
        page.update()
    page.add(
        ft.Column(
            controls=[
                navbar(cambiar_vista),
                contenido
            ]
        )
    )
    cambiar_vista("inicio")
ft.app(target=main)
#iniciar : python -m src.views.page
#GENERAR EJECUtABLE: pyinstaller --onefile --windowed --add-data "assets;assets" src/views/page.py