from Application.Service.cadastro_service import CadastroService
from Infrastructure.Repositories.vendas_repository import VendasRepository
from Infrastructure.Repositories.produto_repository import ProdutoRepository
from Infrastructure.http.jwt_service import JWTService
from Domain.vendas import VendaRealizadaModel

class VendasService:
    def __init__(self):
        self.repository = VendasRepository()
        self.produto_repository = ProdutoRepository()
        self.jwt_service = JWTService()
        self.cliente_service = CadastroService()

    # Registrar uma venda
    def registrar_venda(self, cnpj, id_produto, quantidade_vendida):
        seller = self.cliente_service.buscar_por_cnpj(cnpj)
        if not seller:
            return {"erro": "CNPJ inválido ou incorreto, tente novamente."}, 404

        if seller["status"].lower() == "inativo":
            return {"erro": "Seller inativo. Ative sua conta antes de vender."}, 204

        produto = self.produto_repository.buscar_por_id(id_produto)
        if not produto or produto.id_seller != seller["id"]:
            return {"erro": "Produto não encontrado ou não pertence ao seller"}, 404

        if produto.status == "Inativo":
            return {"erro": "Produtos inativados não podem ser vendidos."}, 204

        if produto.quantidade < quantidade_vendida:
            return {"erro": "Quantidade em estoque insuficiente."}, 204

        # Atualizar estoque
        produto.quantidade -= quantidade_vendida
        self.produto_repository.atualizar_produto(id_produto, {"quantidade": produto.quantidade})

        # Registrar venda
        venda = VendaRealizadaModel(
            id_produto=str(id_produto),
            quantidade_vendida=quantidade_vendida
        )

        venda_id = self.repository.registrar_venda(venda)

        return {
            "mensagem": "Venda registrada com sucesso!",
            "venda_id": venda_id,
            "produto": produto.nome,
            "quantidade_vendida": quantidade_vendida
        }, 200

    # Listar vendas por produto
    def listar_vendas_produto(self, id_produto):
        vendas = self.repository.listar_por_produto(str(id_produto))
        return vendas

    # Listar todas as vendas do seller
    def listar_vendas_seller(self, cnpj):
        seller = self.cliente_service.buscar_por_cnpj(cnpj)
        if not seller:
            return {"erro": "CNPJ inválido."}, 404

        return self.repository.listar_por_seller(seller["id"])

    # Cancelar venda
    def cancelar_venda_por_id(self, venda_id):

        # Buscar venda (objeto ORM)
        venda = self.repository.buscar_por_id(venda_id)
        if not venda:
            return {"erro": "Venda não encontrada."}, 404

        # Buscar produto relacionado
        produto = self.produto_repository.buscar_por_id(venda.id_produto)
        if not produto:
            return {"erro": "Produto relacionado à venda não encontrado."}, 404

        # Repor quantidade ao estoque
        nova_quantidade = produto.quantidade + venda.quantidade_vendida
        self.produto_repository.atualizar_produto(produto.id, {
            "quantidade": nova_quantidade
        })

        # Deletar venda do banco
        sucesso = self.repository.deletar_venda(venda_id)
        if not sucesso:
            return {"erro": "Erro ao cancelar venda."}, 500

        return {
            "mensagem": "Venda cancelada e removida com sucesso.",
            "venda_cancelada": venda_id,
            "produto": produto.nome,
            "quantidade_reposta": venda.quantidade_vendida
        }, 200
