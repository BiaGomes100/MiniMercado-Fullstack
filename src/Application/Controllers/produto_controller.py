from Application.Service.produto_service import ProdutoService

class ProdutoController:
    def __init__(self):
        self.service = ProdutoService()

    def criar(self, token, dados):
        return self.service.adicionar_produto(token, **dados)

    def listar(self, token):
        return self.service.listar_produtos(token)

    def atualizar(self, token, id_produto, dados):
        return self.service.atualizar_produto(token, id_produto, dados)

    def inativar(self, token, id_produto):
        return self.service.inativar_produto(token, id_produto)

    def detalhar(self, token, id_produto):
        return self.service.detalhar_produto(token, id_produto)

    def vender(self, token, id_produto, dados):
        quantidade = dados.get("quantidade_vendida")
        return self.service.vender_produto(token, id_produto, quantidade)