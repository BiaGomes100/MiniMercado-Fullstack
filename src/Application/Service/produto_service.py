import os
from Domain.produto import Produto
from Infrastructure.Repositories.produto_repository import PordutoRepository
from Infrastructure.http.jwt_service import JWTService
from Infrastructure.http.twilio_service import TwilioService


class ProdutoService:
    def __init__(self):
        self.repository = PordutoRepository()
        self.jwt_service = JWTService()
        self.twilio_service = TwilioService()

    def adicionar_produto(self, token_seller, nome, preco, quantidade, imagem):
        if not self.jwt_service.validar_token(token_seller):
            return {"erro": "Token inválido ou expirado"}

        produto = Produto(
            nome=nome,
            preco=preco,
            quantidade=quantidade,
            status="Ativo",
            imagem=imagem
        )

        produto_id = self.repository.adicionar_produto(produto)

        mensagem = f"Produto '{produto.nome}' cadastrado com sucesso! Preço: R$ {produto.preco}"
        self.twilio_service.enviar_mensagem(os.getenv("TWILIO_CELULAR_SELLER"), mensagem)

        return {
            "id": produto_id,
            "mensagem": "Produto cadastrado com sucesso e notificação enviada."
        }

    def listar_produtos(self, token_seller, incluir_inativos=False):
        if not self.jwt_service.validar_token(token_seller):
            return {"erro": "Token inválido ou expirado"}

        produtos = self.repository.listar_Produto()

        if not incluir_inativos:
            produtos = [p for p in produtos if p["status"] == "Ativo"]

        return produtos

    def buscar_por_nome(self, token_seller, nome):
        if not self.jwt_service.validar_token(token_seller):
            return {"erro": "Token inválido ou expirado"}

        produto = self.repository.session.query(self.repository.session.query_property().class_).filter_by(nome=nome).first()
        if not produto:
            return {"erro": "Produto não encontrado"}

        return produto.to_dict()

    def editar_produto(self, token_seller, nome, dados):
        if not self.jwt_service.validar_token(token_seller):
            return {"erro": "Token inválido ou expirado"}

        self.repository.editar_produto(nome, dados)
        return {"mensagem": f"Produto '{nome}' atualizado com sucesso."}

    def inativar_produto(self, token_seller, nome):
        if not self.jwt_service.validar_token(token_seller):
            return {"erro": "Token inválido ou expirado"}

        self.repository.inativar_produto(nome)
        return {"mensagem": f"O produto '{nome}' foi inativado com sucesso."}
