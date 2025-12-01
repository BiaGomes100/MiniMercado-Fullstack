from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from config.db import Base

class VendaRealizadaModel(Base):
    __tablename__ = "vendas_realizadas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_produto = Column(String(100), nullable=False)
    quantidade_vendida = Column(Integer, nullable=False)
    data_venda = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, id_produto, quantidade_vendida):
        self.id_produto = id_produto
        self.quantidade_vendida = quantidade_vendida

    def to_dict(self):
        return {
            "id": self.id,
            "id_produto": self.id_produto,
            "quantidade_vendida": self.quantidade_vendida,
            "data_venda": str(self.data_venda)
        }
