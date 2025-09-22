import os
from Domain.cadastro import Cadastro
from Infrastructure.Repositories.cadastro_repository import CadastroRepository

from Infrastructure.http.jwt_service import JWTService
from Infrastructure.http.twilio_service import TwilioService

class CadastroService:
    def __init__(self):            #aqui ele puxa as clases que vao ser usadas
        self.repository = CadastroRepository()
        self.jwt_service = JWTService()                 
        self.twilio_service = TwilioService()

    def adicionar_cliente(self, nome, cnpj, email, celular, senha):
        """Cria novo cliente e envia código de verificação"""
        # Cria objeto de domínio
        cliente = Cadastro(nome, cnpj, email, celular, senha, "Inativo")
        
        # Salva no banco
        cliente_id = self.repository.adicionar_cliente(cliente)    #salva o cliente no banco e retorna o id
        
        # Gera token JWT para verificação
        token = self.jwt_service.gerar_token(cnpj)
        
        # Envia código via WhatsApp
        mensagem = f"Seu código de verificação: {token}"
        self.twilio_service.enviar_mensagem(celular, mensagem)
        
        return {
            "id": cliente_id,
            "mensagem": "Cliente criado. Verifique seu WhatsApp para ativar.",
            "token_verificacao": token
        }

    def verificar_cliente(self, cnpj, token):
        """Verifica token e ativa cliente"""
        if self.jwt_service.validar_token(token):
            self.repository.atualizar_cliente(cnpj, {"status": "Ativo"})
            return {"mensagem": "Cliente ativado com sucesso"}
        return {"erro": "Token inválido ou expirado"}

    def listar_clientes(self):
        """Lista todos os clientes"""
        return self.repository.listar_clientes()
  

    def buscar_por_cnpj(self, cnpj):
       """Busca cliente específico"""
       cliente = self.repository.buscar_por_cnpj(cnpj)
       return cliente  # já é dict, não precisa do to_dict()


    def atualizar_cliente(self, cnpj, dados):
        """Atualiza dados do cliente"""
        self.repository.atualizar_cliente(cnpj, dados)
        return self.buscar_por_cnpj(cnpj)

    def deletar_cliente(self, cnpj):
        """Remove cliente"""
        cliente = self.buscar_por_cnpj(cnpj)
        if cliente:
            self.repository.deletar_cliente(cnpj)
        return cliente

    def ativar_cliente(self, cnpj):
        """Ativa cliente manualmente"""
        return self.atualizar_cliente(cnpj, {"status": "Ativo"})

    def inativar_cliente(self, cnpj):
        """Inativa cliente"""
        return self.atualizar_cliente(cnpj, {"status": "Inativo"})