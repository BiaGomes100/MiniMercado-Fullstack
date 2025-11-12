# Application/Controllers/auth_controller.py
from Application.Service.login_service import Login_service

class Login_Controller:
    def __init__(self):
        self.service = Login_service()

    def login(self, dados):
        email = dados.get("email")
        senha = dados.get("senha")
        if not email or not senha:
            return {"erro": "CNPJ e senha são obrigatórios"}, 400
        return self.service.login(email, senha)