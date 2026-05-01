import sqlite3
import os
nombre_bd = "revite_carros.db"
def crear_base_de_datos_carros():
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS carros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                placa TEXT UNIQUE NOT NULL,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                mantenimiento TEXT NOT NULL,
                capacidad TEXT NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP       
                )
                ''')
        conexion.commit()
        print(f"Base de datos {nombre_bd} y tabla 'carros' creadas con exito")
    except sqlite3.Error as e:
        print(f"error al conectar error: {e}")
    finally:
        if conexion:
            conexion.close()


def insertar_carro(placa,marca,modelo,mantenimiento,capacidad):
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        # Usamos '?' como placeholders para las variables
        sql = "INSERT INTO carros (placa,marca,modelo,mantenimiento,capacidad) VALUES (?, ?, ?, ?, ?)"
        valores = (placa,marca,modelo,mantenimiento,capacidad)
        cursor.execute(sql,valores)
        conexion.commit()
        print(f"Carro {placa} guardado correctamente")
    except sqlite3.IntegrityError:
        print(f"Error: la placa {placa} ya esta registrada")
    except sqlite3.Error as e:
        print(f"Error al insertar los datos:{e}")
    finally:
        if conexion:
            conexion.close()
def consultar_carros():
    carros = []
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        sql = "SELECT id,placa,marca,modelo,mantenimiento,capacidad,fecha_registro FROM carros"
        cursor.execute(sql)
        carros = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al consultar {e}")
    finally:
        if conexion:
            conexion.close()
    return carros
   

"""
    insertar_usuario("Santiago", "santiagomoralesmorales08@gmail.com", "1070600370", "3133017419")
    insertar_usuario("Nicolas", "nicolasmoralesmorales08@gmail.com", "1070600371", "3133017415")
    insertar_usuario("Pepo", "pedrosanchez@gmail.com", "1070600372", "3133017413")"""
#ACA CREAMOS LA TABLA EL ID SIEMPRE VA ES PARA QUE ME ORGANICE LA TABLA CON ELA UTOICREMENT PARA QUE SE
#ME INCREMENTE MEDIANTE LOS USUARIOS QUE LLEGUEN
# Y LA FECHA DE REGISTRO ES LA FECHA DE LO QUE SE ME CREARON