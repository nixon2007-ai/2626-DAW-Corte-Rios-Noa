import mysql.connector

def get_conexion():
    return mysql.connector.connect(
        host="localhost",
        port=3307,
        user="admin",
        password="admin",
        database="gastrobar_db"
    )
