from Application.Service.produto_service import ProdutoService

class ProdutoController:
    def __init__(self):
        self.service = ProdutoService()

    def criar(self,cnpj ,dados):
        return self.service.adicionar_produto(cnpj, dados)

    def listar(self, cnpj):
        return self.service.listar_produtos(cnpj)

    def atualizar(self, cnpj, id_produto, dados):
        return self.service.atualizar_produto(cnpj, id_produto, dados)

    def inativar(self, cnpj, id_produto):
        return self.service.inativar_produto(cnpj, id_produto)

    def detalhar(self, cnpj, id_produto):
        return self.service.detalhar_produto(cnpj, id_produto)

    def vender(self, cnpj, id_produto, dados):
        quantidade = dados.get("quantidade_vendida")
        return self.service.vender_produto(cnpj, id_produto, quantidade)