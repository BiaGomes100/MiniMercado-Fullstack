import os
from config.db import get_db_connection
from Domain.cadastro import Cadastro
class CadastroRepository_class:
    def adicionar_cliente(self, cliente):
        """Salva o cliente no banco de dados"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """INSERT INTO clientes (nome, cnpj, email, celular, senha, status)
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (
            cliente.nome, 
            cliente.cnpj, 
            cliente.email, 
            cliente.celular, 
            cliente.senha, 
            cliente.status
        ))
        conn.commit()
        cliente_id = cursor.lastrowid

        cursor.close()
        conn.close()
        return cliente_id

    def buscar_por_cnpj(self, cnpj):
        """Busca cliente por CNPJ"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes WHERE cnpj=%s", (cnpj,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    def listar_clientes(self):
        """Lista todos os clientes"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def atualizar_cliente(self, cnpj, dados):
        """Atualiza dados do cliente"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Constrói a query dinamicamente baseada nos dados fornecidos
        set_clause = ", ".join([f"{key}=%s" for key in dados.keys()])
        values = list(dados.values())
        values.append(cnpj)
        
        sql = f"UPDATE clientes SET {set_clause} WHERE cnpj=%s"
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()

    def deletar_cliente(self, cnpj):
        """Remove cliente do banco"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE cnpj=%s", (cnpj,))
        conn.commit()
        cursor.close()
        conn.close()