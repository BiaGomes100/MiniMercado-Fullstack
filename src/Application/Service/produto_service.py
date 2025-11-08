from Domain.produto import Produto
from Infrastructure.Repositories.produto_repository import ProdutoRepository
from Infrastructure.http.jwt_service import JWTService

class ProdutoService:
    def __init__(self):
        self.repository = ProdutoRepository()
        self.jwt_service = JWTService()

    # Cadastrar produto
    def adicionar_produto(self, token, nome, preco, quantidade, imagem):
        seller = self.jwt_service.validar_token(token)
        if not seller:
            return {"erro": "Token inválido ou expirado"}

        if not seller["ativo"]:
            return {"erro": "Seller inativo. Ative sua conta antes de cadastrar produtos."}

        produto = Produto(
            id_seller=seller["id"],
            nome=nome,
            preco=preco,
            quantidade=quantidade,
            imagem=imagem
        )
        produto_id = self.repository.adicionar_produto(produto)
        return {"mensagem": "Produto cadastrado com sucesso!", "id": produto_id}

    # Listar produtos do seller
    def listar_produtos(self, token):
        seller = self.jwt_service.validar_token(token)
        if not seller:
            return {"erro": "Token inválido ou expirado"}

        produtos = self.repository.listar_por_seller(seller["id"])
        return produtos

    # Editar produto
    def atualizar_produto(self, token, id_produto, dados):
        seller = self.jwt_service.validar_token(token)
        if not seller:
            return {"erro": "Token inválido"}

        produto = self.repository.buscar_por_id(id_produto)
        if not produto or produto.id_seller != seller["id"]:
            return {"erro": "Produto não encontrado ou não pertence ao seller"}

        atualizado = self.repository.atualizar_produto(id_produto, dados)
        return {"mensagem": "Produto atualizado com sucesso!", "produto": atualizado.to_dict()}

    # Inativar produto
    def inativar_produto(self, token, id_produto):
        seller = self.jwt_service.validar_token(token)
        if not seller:
            return {"erro": "Token inválido"}

        produto = self.repository.buscar_por_id(id_produto)
        if not produto or produto.id_seller != seller["id"]:
            return {"erro": "Produto não encontrado"}

        inativo = self.repository.inativar_produto(id_produto)
        return {"mensagem": f"Produto '{inativo.nome}' inativado com sucesso."}

    # Ver detalhes de produto
    def detalhar_produto(self, token, id_produto):
        seller = self.jwt_service.validar_token(token)
        if not seller:
            return {"erro": "Token inválido"}

        produto = self.repository.buscar_por_id(id_produto)
        if not produto or produto.id_seller != seller["id"]:
            return {"erro": "Produto não encontrado"}

        return produto.to_dict()

    # Realizar venda (regras dentro do mesmo módulo)
    def vender_produto(self, token, id_produto, quantidade_vendida):
        seller = self.jwt_service.validar_token(token)
        if not seller:
            return {"erro": "Token inválido ou expirado"}

        if not seller["ativo"]:
            return {"erro": "Sellers inativos não podem realizar vendas."}

        produto = self.repository.buscar_por_id(id_produto)
        if not produto or produto.id_seller != seller["id"]:
            return {"erro": "Produto não encontrado ou não pertence ao seller"}

        if produto.status == "Inativo":
            return {"erro": "Produtos inativados não podem ser vendidos."}

        if produto.quantidade < quantidade_vendida:
            return {"erro": "Quantidade em estoque insuficiente."}

        # Atualiza o estoque
        produto.quantidade -= quantidade_vendida
        self.repository.atualizar_produto(id_produto, {"quantidade": produto.quantidade})

        valor_total = quantidade_vendida * produto.preco

        return {
            "mensagem": "Venda realizada com sucesso!",
            "produto": produto.nome,
            "quantidade_vendida": quantidade_vendida,
            "valor_total": valor_total
        }