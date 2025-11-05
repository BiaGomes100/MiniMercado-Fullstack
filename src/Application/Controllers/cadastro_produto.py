from Domain.produto import Produto

class ProdutoController:
    def __init__(self):
        self.produtos = []

    def criar(self, nome, preco, quantidade, imagem, status="Inativo"):
        produto = Produto(nome, preco, quantidade, imagem, status)
        self.produtos.append(produto)
        return "Produto criado com sucesso!"

    def listar(self):
        return [p.to_dict() for p in self.produtos]

    def atualizar(self, nome, novos_dados):
        for produto in self.produtos:
            if produto.nome == nome:
                produto.preco = novos_dados.get("preco", produto.preco)
                produto.quantidade = novos_dados.get("quantidade", produto.quantidade)
                produto.imagem = novos_dados.get("imagem", produto.imagem)
                produto.status = novos_dados.get("status", produto.status)
                return f"Produto '{nome}' atualizado com sucesso!"
        return "Produto não encontrado."

    def deletar(self, nome):
        for produto in self.produtos:
            if produto.nome == nome:
                self.produtos.remove(produto)
                return f"Produto '{nome}' deletado com sucesso!"
        return "Produto não encontrado."
