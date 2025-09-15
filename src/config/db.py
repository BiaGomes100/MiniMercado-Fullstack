import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",       # troque pelo seu usuário MySQL
        password="191077",     # troque pela sua senha
        database="mini_mercado"
    )
