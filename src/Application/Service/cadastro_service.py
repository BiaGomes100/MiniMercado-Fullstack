import os
from Domain.cadastro import Cadastro
from infrastructure.Repositories.cadastro_repository import CadastroRepository

from infrastructure.http.jwt_service import JWTService
from infrastructure.http.twilio_service import TwilioService

class CadastroService:
    def __init__(self):           
        self.repository = CadastroRepository()
        self.jwt_service = JWTService()                 
        self.twilio_service = TwilioService()

    def adicionar_cliente(self, nome, cnpj, email, celular, senha):
        cliente = Cadastro(nome, cnpj, email, celular, senha, "Inativo")
        
        cliente_id = self.repository.adicionar_cliente(cliente)    
        
        token = self.jwt_service.gerar_token(cnpj)
        
        mensagem = f"Seu código de verificação: {token}"
        self.twilio_service.enviar_mensagem(celular, mensagem)
        
        return {
            "id": cliente_id,
            "mensagem": "Cliente criado. Verifique seu WhatsApp para ativar.",
            "token_verificacao": token
        }

    def verificar_cliente(self, cnpj, token):
        if self.jwt_service.validar_token(token):
            self.repository.atualizar_cliente(cnpj, {"status": "Ativo"})
            return {"mensagem": "Cliente ativado com sucesso"}
        return {"erro": "Token inválido ou expirado"}

    def listar_clientes(self):
        return self.repository.listar_clientes()
  

    def buscar_por_cnpj(self, cnpj):
       cliente = self.repository.buscar_por_cnpj(cnpj)
       return cliente  

    def atualizar_cliente(self, cnpj, dados):
        self.repository.atualizar_cliente(cnpj, dados)
        return self.buscar_por_cnpj(cnpj)

    def deletar_cliente(self, cnpj):
        cliente = self.buscar_por_cnpj(cnpj)
        if cliente:
            self.repository.deletar_cliente(cnpj)
        return cliente

    def ativar_cliente(self, cnpj):
        return self.atualizar_cliente(cnpj, {"status": "Ativo"})

    def inativar_cliente(self, cnpj):
        return self.atualizar_cliente(cnpj, {"status": "Inativo"})