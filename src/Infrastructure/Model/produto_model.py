from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from config import Base  


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)
    quantidade = Column(Integer, nullable=False)
    status = Column(Boolean, default=True) 
    imagem = Column(String(255))
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)

    
    seller = relationship("Seller", back_populates="produtos")

    def __init__(self, nome, preco, quantidade, seller_id, imagem=None, status=True):
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.status = status
        self.imagem = imagem
        self.seller_id = seller_id

    def to_dict(self): #retorna as informacoes em json 
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
            "quantidade": self.quantidade,
            "status": "Ativo" if self.status else "Inativo",
            "imagem": self.imagem,
            "seller_id": self.seller_id
        }
