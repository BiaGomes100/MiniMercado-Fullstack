from config.db import SessionLocal
from Infrastructure.Model.produto_model import ProdutoModel

class PordutoRepository:
    def __init__(self):
        self.session = SessionLocal()

    def adicionar_produto(self, produto):
        novo = ProdutoModel(
            nome=produto.nome,
            preco=produto.preco,
            quantidade=produto.quantidade,
            imagem=produto.imagem,
            status=produto.status
        )
        self.session.add(novo)
        self.session.commit()
        return novo.id

    def listar_produtos(self):
        produtos = self.session.query(ProdutoModel).all()
        return [c.to_dict() for c in produtos]

    def buscar_por_nome(self, nome):
        produto = self.session.query(ProdutoModel).filter_by(nome=nome).first()
        return produto.to_dict() if produto else None

    def editar_produto(self, nome, dados):
        produto = self.session.query(ProdutoModel).filter_by(nome=nome).first()
        if produto:
            for chave, valor in dados.items():
                setattr(produto, chave, valor)
            self.session.commit()

    def inativar_produto(self, nome):
        produto = self.session.query(ProdutoModel).filter_by(nome=nome).first()
        if produto:
            self.session.delete(produto)
            self.session.commit()

    def detalhar_produto(self, nome):
        produto = self.session.query(ProdutoModel).filter_by(nome=nome).first()
        return produto.to_dict() if produto else None
