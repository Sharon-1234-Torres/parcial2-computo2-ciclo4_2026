import mysql.connector
from mysql.connector import Error


class Conexion:
    def __init__(self):
        self.config = dict(host="localhost", user="root", password="", database="db_academica_parcial-2")
        self.conexion = None
        self.conectar()

    def conectar(self):
        try:
            self.conexion = mysql.connector.connect(**self.config)
            print("Conexion exitosa a db_academica_parcial-2")
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def _asegurar(self):
        
        if self.conexion is None or not self.conexion.is_connected():
            self.conectar()
        else:
            self.conexion.ping(reconnect=True)

    def consultar(self, sql, datos=()):
        try:
            self._asegurar()
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute(sql, datos)
            filas = cursor.fetchall()
            cursor.close()
            return filas
        except Error as e:
            print(f"Error al consultar la base de datos: {e}")
            return None

    def ejecutar(self, sql, datos=()):
        try:
            self._asegurar()
            cursor = self.conexion.cursor()
            cursor.execute(sql, datos)
            self.conexion.commit()
            cursor.close()
            return 'ok'
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return f'Error: {e}'
