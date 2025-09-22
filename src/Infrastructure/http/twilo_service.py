from flask.cli import load_dotenv
from twilio.rest import Client
import os


load_dotenv()

class TwilioService:
    def __init__(self):
        self.account_sid = "AC3f7ab2232a16a90becaf86f3c9786a7a"
        self.auth_token = "8deed8ded9ded6849585e02fd4d95804"
        self.from_number = '+13262363042'
        self.client = Client(self.account_sid, self.auth_token)

    def enviar_mensagem(self, to_number, mensagem):
        """Envia mensagem via WhatsApp usando Twilio"""
        try:
            message = self.client.messages.create(
                body=mensagem,
                from_=f"whatsapp:{self.from_number}",
                to=f"whatsapp:{to_number}"
            )
            return {"status": "success", "message_sid": message.sid}
        except Exception as e:
            return {"status": "error", "erro": str(e)}