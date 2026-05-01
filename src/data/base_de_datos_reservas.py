import sqlite3
import os
nombre_bd = "revite_reserva.db"
def crear_base_de_datos_reservas():
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                cedula TEXT UNIQUE NOT NULL,
                foto TEXT NOT NULL,
                hora TEXT NOT NULL,
                sector TEXT NOT NULL,
                taxi TEXT NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP       
                )
                ''')
        conexion.commit()
        print(f"Base de datos {nombre_bd} y tabla 'usuarios' creadas con exito")
    except sqlite3.Error as e:
        print(f"error al conectar error: {e}")
    finally:
        if conexion:
            conexion.close()


def insertar_reserva(nombre,apellido,cedula,foto,hora,sector,taxi):
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        # Usamos '?' como placeholders para las variables
        sql = "INSERT INTO reservas (nombre,apellido,cedula,foto,hora,sector,taxi) VALUES (?, ?, ?, ?, ?, ?, ?)"
        valores = (nombre,apellido,cedula,foto,hora,sector,taxi)
        cursor.execute(sql,valores)
        conexion.commit()
        print(f"Reserva para {nombre} guardada correctamente")
    except sqlite3.IntegrityError:
        print(f"Error: la cedula {cedula} ya esta registrada")
    except sqlite3.Error as e:
        print(f"Error al insertar los datos:{e}")
    finally:
        if conexion:
            conexion.close()
def consultar_usuarios():
    usuarios = []
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        sql = "SELECT id,nombre,apellido,cedula,foto,hora,sector,taxi,fecha_registro FROM reservas"
        cursor.execute(sql)
        usuarios = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al consultar {e}")
    finally:
        if conexion:
            conexion.close()
    return usuarios

#ACA CREAMOS LA TABLA EL ID SIEMPRE VA ES PARA QUE ME ORGANICE LA TABLA CON ELA UTOICREMENT PARA QUE SE
#ME INCREMENTE MEDIANTE LOS USUARIOS QUE LLEGUEN
# Y LA FECHA DE REGISTRO ES LA FECHA DE LO QUE SE ME CREARON