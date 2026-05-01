import sqlite3
import os
nombre_bd = "revite_cliente.db"
def crear_base_de_datos_cliente():
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                cedula TEXT UNIQUE NOT NULL,
                foto TEXT UNIQUE NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP       
                )
                ''')
        conexion.commit()
        print(f"Base de datos {nombre_bd} y tabla 'clientes' creadas con exito")
    except sqlite3.Error as e:
        print(f"error al conectar error: {e}")
    finally:
        if conexion:
            conexion.close()


def insertar_cliente(nombre,apellido,cedula,foto):
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        # Usamos '?' como placeholders para las variables
        sql = "INSERT INTO clientes (nombre,apellido,cedula,foto) VALUES (?, ?, ?, ?)"
        valores = (nombre,apellido,cedula,foto)
        cursor.execute(sql,valores)
        conexion.commit()
        print(f"Usuario {nombre} guardado correctamente")
    except sqlite3.IntegrityError:
        print(f"Error: la cedula {cedula} ya esta registrada")
    except sqlite3.Error as e:
        print(f"Error al insertar los datos:{e}")
    finally:
        if conexion:
            conexion.close()
def consultar_clientes():
    clientes = []
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        sql = "SELECT id,nombre,apellido,cedula,foto,fecha_registro FROM clientes"
        cursor.execute(sql)
        clientes = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al consultar {e}")
    finally:
        if conexion:
            conexion.close()
    return clientes


"""
    insertar_usuario("Santiago", "santiagomoralesmorales08@gmail.com", "1070600370", "3133017419")
    insertar_usuario("Nicolas", "nicolasmoralesmorales08@gmail.com", "1070600371", "3133017415")
    insertar_usuario("Pepo", "pedrosanchez@gmail.com", "1070600372", "3133017413")"""
#ACA CREAMOS LA TABLA EL ID SIEMPRE VA ES PARA QUE ME ORGANICE LA TABLA CON ELA UTOICREMENT PARA QUE SE
#ME INCREMENTE MEDIANTE LOS USUARIOS QUE LLEGUEN
# Y LA FECHA DE REGISTRO ES LA FECHA DE LO QUE SE ME CREARON