from config.db import Session
from Domain.vendas import VendaRealizadaModel
from Infrastructure.Model.produto_model import ProdutoModel

class VendasRepository:

    def registrar_venda(self, venda: VendaRealizadaModel):
        session = Session()
        session.add(venda)
        session.commit()
        session.refresh(venda)
        session.close()
        return venda.id

    def buscar_por_id(self, venda_id):
        session = Session()
        venda = session.query(VendaRealizadaModel).filter_by(id=venda_id).first()
        session.close()
        return venda

    def deletar_venda(self, venda_id):
        session = Session()
        venda = session.query(VendaRealizadaModel).filter_by(id=venda_id).first()

        if not venda:
            session.close()
            return False

        session.delete(venda)
        session.commit()
        session.close()
        return True

    def listar_por_produto(self, id_produto):
        session = Session()
        vendas = session.query(VendaRealizadaModel).filter_by(id_produto=id_produto).all()
        session.close()
        return [v.to_dict() for v in vendas]

    def listar_por_seller(self, id_seller):
        session = Session()
        vendas = (
            session.query(VendaRealizadaModel)
            .join(ProdutoModel, ProdutoModel.id == VendaRealizadaModel.id_produto)
            .filter(ProdutoModel.id_seller == id_seller)
            .all()
        )
        session.close()
        return [v.to_dict() for v in vendas]
