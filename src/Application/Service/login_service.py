from Infrastructure.Repositories.cadastro_repository import CadastroRepository
from Infrastructure.http.jwt_service import JWTService
from Infrastructure.http.twilio_service import TwilioService

class Login_service:
    def __init__(self):
        self.repository = CadastroRepository()
        self.jwt_service = JWTService()
        self.twilio_service = TwilioService()

    def login(self, email, senha):
        cliente = self.repository.listar_clientes_por_email(email)
        if not cliente:
            return {"erro": "Cliente não encontrado"}, 404

        if cliente["senha"] != senha:
            return {"erro": "Senha incorreta"}, 401

        if cliente["status"] != "Ativo":
            # Gerar token de verificação para Twilio
            token = self.jwt_service.gerar_token(email)
            mensagem = f"Seu código de verificação: {token}"
            self.twilio_service.enviar_mensagem(cliente["celular"], mensagem)
            return {"erro": "Cliente inativo. Código enviado via WhatsApp."}, 403

        # Cliente ativo → gera JWT de autenticação
        auth_token = self.jwt_service.gerar_token(email)
        return {"mensagem": "Login bem-sucedido", "token": auth_token}, 200