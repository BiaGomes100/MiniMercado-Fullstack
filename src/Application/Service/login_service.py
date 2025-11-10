from Infrastructure.Repositories.cadastro_repository import CadastroRepository
from Infrastructure.http.jwt_service import JWTService
from Infrastructure.http.twilio_service import TwilioService

class Login_service:
    def __init__(self):
        self.repository = CadastroRepository()
        self.jwt_service = JWTService()
        self.twilio_service = TwilioService()

    def login(self, cnpj, senha):
        cliente = self.repository.buscar_por_cnpj(cnpj)
        if not cliente:
            return {"erro": "Cliente não encontrado"}, 404

        if cliente["senha"] != senha:
            return {"erro": "Senha incorreta"}, 401

        if cliente["status"] != "Ativo":
            # Gerar token de verificação para Twilio
            token = self.jwt_service.gerar_token(cnpj)
            mensagem = f"Seu código de verificação: {token}"
            self.twilio_service.enviar_mensagem(cliente["celular"], mensagem)
            return {"erro": "Cliente inativo. Código enviado via WhatsApp."}, 403

        # Cliente ativo → gera JWT de autenticação
        auth_token = self.jwt_service.gerar_token(cnpj)
        return {"mensagem": "Login bem-sucedido", "token": auth_token}, 200