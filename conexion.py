import sqlite3
from PyQt5 import QtSql

class Conexion():

    def crearBD(filename):
        try:
            con = sqlite3.connect(database=filename)
            cursor = con.cursor()
            cursor.execute('CREATE TABLE if not exists puntuacion (max_puntos INTEGER NOT NULL, fecha TEXT NOT NULL)')
            con.commit()
            con.close()
        except Exception as error:
            print('Error al crear la base de datos ',error)

    def conectarBD(filedb):
        try:
            db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName(filedb)
            if not db.open():
                print('Error al conectarse')
                return False
            else:
                print('Conexión establecida')
                return True

        except Exception as error:
            print('Error conectando a la BD ',error)

    def guardar_puntuacion(puntuacion):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('INSERT INTO puntuacion(max_puntos,fecha) VALUES (:puntuacion_maxima,:fecha_conseguido)')
            query.bindValue(":puntuacion_maxima",int(puntuacion[0]))
            query.bindValue(":fecha_conseguido",str(puntuacion[1]))
            if query.exec():
                print('valores actualizados')
        except Exception as error:
            print('Error guardando la puntuación', error)