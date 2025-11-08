class Produto:
    def __init__(self, id_seller, nome, preco, quantidade, imagem, status="Ativo"):
        self.id_seller = id_seller
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.imagem = imagem
        self.status = status

    def to_dict(self):
        return {
            "id_seller": self.id_seller,
            "nome": self.nome,
            "preco": self.preco,
            "quantidade": self.quantidade,
            "imagem": self.imagem,
            "status": self.status
        }