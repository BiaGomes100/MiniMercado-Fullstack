import os
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

    def listar(self):
        return self.service.listar_produtos()

    def atualizar(self, id_produto, dados):
        return self.service.atualizar_produto(id_produto, dados)

    def deletar(self, id_produto):
        return self.service.deletar_produto(id_produto)

    def buscar(self, id_produto):
        return self.service.buscar_por_id(id_produto)   
    
