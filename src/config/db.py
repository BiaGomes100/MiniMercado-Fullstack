import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",       # ajuste seu usuário
        password="191077", # ajuste sua senha
        database="mini_mercado"
    )
