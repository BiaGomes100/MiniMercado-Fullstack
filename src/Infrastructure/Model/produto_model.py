from sqlalchemy import Column, Integer, String, Float, ForeignKey
from config.db import Base

class ProdutoModel(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_seller = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    nome = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)
    quantidade = Column(Integer, nullable=False)
    imagem = Column(String(255))
    status = Column(String(20), default="Ativo")

    def __init__(self, id_seller, nome, preco, quantidade, imagem=None, status="Ativo"):
        self.id_seller = id_seller
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.imagem = imagem
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "id_seller": self.id_seller,
            "nome": self.nome,
            "preco": self.preco,
            "quantidade": self.quantidade,
            "imagem": self.imagem,
            "status": self.status
        }
