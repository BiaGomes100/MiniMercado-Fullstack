import os
from Application.Service.Cadastro_service import CadastroService

class CadastroCliente:
    def __init__(self):
        self.service = CadastroService()

    def criar(self, dados):
        """Cria novo cliente com verificação de 2 fatores"""
        return self.service.adicionar_cliente(
            dados["nome"],
            dados["cnpj"],
            dados["email"],
            dados["celular"],
            dados["senha"]
        )

    def verificar(self, cnpj, token):
        """Verifica token de ativação"""
        return self.service.verificar_cliente(cnpj, token)

    def listar(self):
        """Lista todos os clientes"""
        return self.service.listar_clientes()

    def ativar(self, cnpj):
        """Ativa cliente manualmente (admin)"""
        return self.service.ativar_cliente(cnpj)

    def inativar(self, cnpj):
        """Inativa cliente"""
        return self.service.inativar_cliente(cnpj)

    def atualizar(self, cnpj, dados):
        """Atualiza dados do cliente"""
        return self.service.atualizar_cliente(cnpj, dados)

    def deletar(self, cnpj):
        """Remove cliente"""
        return self.service.deletar_cliente(cnpj)