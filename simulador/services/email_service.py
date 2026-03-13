import requests
from decouple import config

RESEND_API_KEY = config("RESEND_API_KEY")

def enviar_email(destinatario, asunto, html):

    response = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "from": "Finanzas Raíz <onboarding@resend.dev>",
            "to": [destinatario],
            "subject": asunto,
            "html": html,
        },
    )

    return response