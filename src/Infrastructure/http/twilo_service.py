from flask.cli import load_dotenv
from twilio.rest import Client
import os


load_dotenv()

class TwilioService:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.from_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
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