import mysql.connector
from config.db import get_db_connection

class CadastroRepository:

    def buscar_por_cnpj(self, cnpj):
        """Busca um cliente pelo CNPJ"""
        conn = get_db_connection()
        with conn.cursor(dictionary=True, buffered=True) as cursor:
            cursor.execute("SELECT * FROM clientes WHERE cnpj=%s", (cnpj,))
            row = cursor.fetchone()
        conn.close()
        return row

    def listar_clientes(self):
        """Lista todos os clientes"""
        conn = get_db_connection()
        with conn.cursor(dictionary=True, buffered=True) as cursor:
            cursor.execute("SELECT * FROM clientes")
            rows = cursor.fetchall()
        conn.close()
        return rows

    def adicionar_cliente(self, cliente):
        """Adiciona um cliente e retorna o id inserido"""
        conn = get_db_connection()
        with conn.cursor(buffered=True) as cursor:
            cursor.execute(
                "INSERT INTO clientes (cnpj, nome, email, celular, senha, status) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (cliente.cnpj, cliente.nome, cliente.email, cliente.celular, cliente.senha, cliente.status)
            )
            conn.commit()
            cliente_id = cursor.lastrowid  # pega o id do cliente inserido
        conn.close()
        return cliente_id

    def atualizar_cliente(self, cnpj, dados):
        """Atualiza dados do cliente pelo CNPJ"""
        conn = get_db_connection()
        with conn.cursor(buffered=True) as cursor:
            cursor.execute(
                "UPDATE clientes SET nome=%s, status=%s WHERE cnpj=%s",
                (dados.get("nome"), dados.get("status", "Inativo"), cnpj)
            )
            conn.commit()
        conn.close()

    def deletar_cliente(self, cnpj):
        """Deleta um cliente pelo CNPJ"""
        conn = get_db_connection()
        with conn.cursor(buffered=True) as cursor:
            cursor.execute("DELETE FROM clientes WHERE cnpj=%s", (cnpj,))
            conn.commit()
        conn.close()
