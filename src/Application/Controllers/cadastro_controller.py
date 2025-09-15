from config.db import get_db_connection
from Infrastructure.Model.cadastro_model import ClienteModel

class CadastroCliente:
    
    def adicionarCliente(self, nome, cnpj, email, celular, senha):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "INSERT INTO clientes (nome, cnpj, email, celular, senha) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (nome, cnpj, email, celular, senha))
        conn.commit()
        cliente_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return ClienteModel(cliente_id, nome, cnpj, email, celular, senha, "Inativo", None).to_dict()

    def listarCliente(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes")
        clientes = [ClienteModel(**row).to_dict() for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return clientes

    def buscar_cliente_por_cnpj(self, cnpj):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes WHERE cnpj=%s", (cnpj,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return ClienteModel(**row).to_dict() if row else None

    def atualizarPerfil(self, cnpj, nome=None, email=None, celular=None, senha=None, status=None):
        cliente = self.buscar_cliente_por_cnpj(cnpj)
        if not cliente:
            return None
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "UPDATE clientes SET nome=%s, email=%s, celular=%s, senha=%s, status=%s WHERE cnpj=%s"
        cursor.execute(sql, (
            nome if nome else cliente['nome'],
            email if email else cliente['email'],
            celular if celular else cliente['celular'],
            senha if senha else cliente['senha'],
            status if status else cliente['status'],
            cnpj
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return self.buscar_cliente_por_cnpj(cnpj)

    def deletar_cliente(self, cnpj):
        cliente = self.buscar_cliente_por_cnpj(cnpj)
        if not cliente:
            return None
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE cnpj=%s", (cnpj,))
        conn.commit()
        cursor.close()
        conn.close()
        return cliente

    def ativar_cliente(self, cnpj):
        return self.atualizarPerfil(cnpj, status="Ativo")

    def inativar_cliente(self, cnpj):
        return self.atualizarPerfil(cnpj, status="Inativo")
