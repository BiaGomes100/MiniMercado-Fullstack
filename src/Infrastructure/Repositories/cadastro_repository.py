# Infrastructure/repositories/cadastro_repository.py
from config.db import SessionLocal
from Infrastructure.Model.cadastro_model import ClienteModel

class CadastroRepository:
    def __init__(self):
        self.session = SessionLocal()

    def adicionar_cliente(self, cliente):
        novo =  ClienteModel(
            nome=cliente.nome,
            cnpj=cliente.cnpj,
            email=cliente.email,
            celular=cliente.celular,
            senha=cliente.senha,
            status=cliente.status
        )
        self.session.add(novo)
        self.session.commit()
        return novo.id

    def listar_clientes(self):
        clientes = self.session.query( ClienteModel).all()
        return [c.to_dict() for c in clientes]

    def buscar_por_cnpj(self, cnpj):
        cliente = self.session.query( ClienteModel).filter_by(cnpj=cnpj).first()
        return cliente.to_dict() if cliente else None

    def atualizar_cliente(self, cnpj, dados):
        cliente = self.session.query(ClienteModel).filter_by(cnpj=cnpj).first()
        if cliente:
            for chave, valor in dados.items():
                setattr(cliente, chave, valor)
            self.session.commit()

    def deletar_cliente(self, cnpj):
        cliente = self.session.query(ClienteModel).filter_by(cnpj=cnpj).first()
        if cliente:
            self.session.delete(cliente)
            self.session.commit()

    def listar_clientes_por_email(self, email):
        cliente = self.session.query( ClienteModel).filter_by(email=email).first()
        return cliente.to_dict() if cliente else None
