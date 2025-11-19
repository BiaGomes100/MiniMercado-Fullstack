from Application.Service.cadastro_service import CadastroService
from Domain.produto import Produto
from Infrastructure.Repositories.produto_repository import ProdutoRepository
from Infrastructure.http.jwt_service import JWTService

class ProdutoService:
    def __init__(self):
        self.repository = ProdutoRepository()
        self.jwt_service = JWTService()
        self.cliente_service = CadastroService()

    # Cadastrar produto
    def adicionar_produto(self, cnpj, dados):
        ##seller = self.jwt_service.validar_token(token)
        seller = self.cliente_service.buscar_por_cnpj(cnpj)
        # if not seller:
        #     return {"erro": "CNPJ inválido ou incorreto, tente novamente."}

        if seller["status"].lower() == "Inativo":
            return {"erro": "Seller inativo. Ative sua conta antes de cadastrar produtos."}

        produto = Produto(
            id_seller=seller["id"],
            nome=dados.get("nome"),
            preco=dados.get("preco"),
            quantidade=dados.get("quantidade"),
            imagem=dados.get("imagem")
        )
        produto_id = self.repository.adicionar_produto(produto)
        return {"mensagem": "Produto cadastrado com sucesso!", "id": produto_id},200

    # Listar produtos do seller
    def listar_produtos(self, cnpj):
        seller = self.cliente_service.buscar_por_cnpj(cnpj)
        if not seller:
            return {"erro": "Não existe produtos para o Cnpj enviado."},404

        produtos = self.repository.listar_por_seller(seller["id"])
        return produtos

    # Editar produto
    def atualizar_produto(self, cnpj, id_produto, dados):
        seller = self.cliente_service.buscar_por_cnpj(cnpj)
        if not seller:
            return {"erro": "Não existe produtos para o Cnpj enviado."},404

        produto = self.repository.buscar_por_id(id_produto)
        if not produto or produto.id_seller != seller["id"]:
            return {"erro": "Produto não encontrado ou não pertence ao seller"}, 404

        atualizado = self.repository.atualizar_produto(id_produto, dados)
        return {"mensagem": "Produto atualizado com sucesso!", "produto": atualizado.to_dict()}

    # Inativar produto
    def inativar_produto(self, cnpj, id_produto):
        inativo = self.repository.inativar_produto(id_produto)
        return {"mensagem": f"Produto '{inativo.nome}' inativado com sucesso."},201

    # Ver detalhes de produto
    def detalhar_produto(self, cnpj, id_produto):
        seller = self.cliente_service.buscar_por_cnpj(cnpj)
        if not seller:
            return {"erro": "Não existe produtos para o Cnpj enviado."},404

        produto = self.repository.buscar_por_id(id_produto)
        if not produto or produto.id_seller != seller["id"]:
            return {"erro": "Produto não encontrado"},404

        return produto.to_dict()

    # Realizar venda (regras dentro do mesmo módulo)
    def vender_produto(self, cnpj,id_produto, quantidade_vendida):

        produto = self.repository.buscar_por_id(id_produto)
        if produto.status == "Inativo":
            return {"erro": "Produtos inativados não podem ser vendidos."}, 401

        if produto.quantidade < quantidade_vendida:
            self.inativar_produto(cnpj,id_produto)
            return {"erro": "Quantidade em estoque insuficiente."},401

        # Atualiza o estoque
        produto.quantidade -= quantidade_vendida
        if produto.quantidade == 0:
            self.inativar_produto(cnpj,id_produto)

        self.repository.atualizar_produto(id_produto, {"quantidade": produto.quantidade})

        valor_total = quantidade_vendida * produto.preco

        return {
            "mensagem": "Venda realizada com sucesso!",
            "produto": produto.nome,
            "quantidade_vendida": quantidade_vendida,
            "valor_total": valor_total
        }