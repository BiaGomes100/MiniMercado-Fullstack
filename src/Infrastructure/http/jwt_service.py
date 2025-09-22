from flask.cli import load_dotenv
import jwt
import datetime
import os

load_dotenv()

class JWTService:
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY", "chave_secreta_padrao")

    def gerar_token(self, cnpj):
        """Gera token JWT para verificação de 2 fatores"""
        payload = {
            "cnpj": cnpj,
            "exp": datetime.datetime.today() + datetime.timedelta(minutes=10)
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def validar_token(self, token):
        """Valida token JWT"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload["cnpj"]
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None