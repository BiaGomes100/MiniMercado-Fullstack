'''import os
from Application.Service.produto_service import ProdutoService

class CadastroProduto:
    def __init__(self):
        self.service = ProdutoService()

    def criar(self, dados):
        return self.service.adicionar_produto(
            dados["nome"],
            dados["preco"],
            dados["quantidade"],
            dados["imagem"],
            dados["status"]
        )

    def verificar(self, cnpj, token):
        return self.service.verificar_cliente(cnpj, token)

    def listar(self):
        return self.service.listar_clientes()

    def ativar(self, cnpj):
        return self.service.ativar_cliente(cnpj)

    def inativar(self, cnpj):
        return self.service.inativar_cliente(cnpj)

    def atualizar(self, cnpj, dados):
        return self.service.atualizar_cliente(cnpj, dados)

    def deletar(self, cnpj):
        return self.service.deletar_cliente(cnpj)

        ''' 