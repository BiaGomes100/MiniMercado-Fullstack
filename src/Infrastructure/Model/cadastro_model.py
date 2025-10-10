# src/infrastructure/model.py
from sqlalchemy import Column, Integer, String
from config.db import Base

# Classe do ORM
class ClienteModel(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    cnpj = Column(String(18), unique=True, nullable=False)
    email = Column(String(100), nullable=False)
    celular = Column(String(20), nullable=True)
    senha = Column(String(100), nullable=False)
    status = Column(String(20), default="Inativo", nullable=False)

    def __init__(self, nome, cnpj, email, celular, senha, status="Inativo"):
        self.nome = nome
        self.cnpj = cnpj
        self.email = email
        self.celular = celular
        self.senha = senha
        self.status = status

    # Converte objeto ORM para dicionário
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cnpj": self.cnpj,
            "email": self.email,
            "celular": self.celular,
            "senha": self.senha,
            "status": self.status,
        }
