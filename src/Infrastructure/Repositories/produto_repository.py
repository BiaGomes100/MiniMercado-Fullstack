from config.db import SessionLocal
from Infrastructure.Model.produto_model import ProdutoModel

class ProdutoRepository:
    def __init__(self):
        self.session = SessionLocal()

    def adicionar_produto(self, produto):
        novo = ProdutoModel(
            id_seller=produto.id_seller,
            nome=produto.nome,
            preco=produto.preco,
            quantidade=produto.quantidade,
            imagem=produto.imagem,
            status=produto.status
        )
        self.session.add(novo)
        self.session.commit()
        return novo.id

    def listar_por_seller(self, id_seller):
        produtos = self.session.query(ProdutoModel).filter_by(id_seller=id_seller).all()
        return [p.to_dict() for p in produtos]

    def buscar_por_id(self, id_produto):
        return self.session.query(ProdutoModel).filter_by(id=id_produto).first()

    def atualizar_produto(self, id_produto, dados):
        produto = self.buscar_por_id(id_produto)
        if produto:
            for chave, valor in dados.items():
                setattr(produto, chave, valor)
            self.session.commit()
            return produto
        return None

    def inativar_produto(self, id_produto):
        produto = self.buscar_por_id(id_produto)
        if produto:
            produto.status = "Inativo"
            self.session.commit()
            return produto
        return None