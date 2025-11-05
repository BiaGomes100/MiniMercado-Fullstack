from Infrastructure.Model.produto_model import Produto
#falta colocar o baco de dados aqui que a thay vai me ajudar 
#falta validar tbnm o seller(codigo aq em baixo)

"""if produto.seller_id != seller_id_autenticado:
    raise PermissionError("Você só pode gerenciar seus próprios produtos")"""

class ProdutoRepository:
    def __init__(self):
        self._produtos = []
        self._proximo_id = 1

    def adicionar_produto(self, produto: Produto):
        produto.id = self._proximo_id
        self._produtos.append(produto)
        self._proximo_id += 1
        return produto.id

    def listar_produtos(self, incluir_inativos=False):
        if incluir_inativos:
            return self._produtos
        return [p for p in self._produtos if p.status]

    def buscar_por_id(self, id_produto):
        for produto in self._produtos:
            if produto.id == id_produto:
                return produto
        return None

    def atualizar_produto(self, produto_atualizado: Produto):
        for i, produto in enumerate(self._produtos):
            if produto.id == produto_atualizado.id:
                self._produtos[i] = produto_atualizado
                return True
        return False
