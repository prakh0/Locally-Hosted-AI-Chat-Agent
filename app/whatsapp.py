import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
import requests
import logging
from fastapi.responses import Response
from .model import generate_reply, reset_user

app = FastAPI()

logging.basicConfig(level=logging.INFO)

load_dotenv()
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")


@app.get("/webhook")
async def verify_webhook(request: Request):
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if token == VERIFY_TOKEN:
        return Response(content=challenge, media_type="text/plain")

    return Response(content="Verification failed", status_code=403)


ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")


def send_whatsapp_message(to, message):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    data = {"messaging_product": "whatsapp", "to": to, "text": {"body": message}}

    res = requests.post(url, headers=headers, json=data)
    print("STATUS:", res.status_code)
    print("RESPONSE:", res.text)


@app.get("/")
def home():
    return {"status": "WhatsApp AI Agent is running"}


@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    try:
        data = await request.json()

        entry = data.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})

        messages = value.get("messages")

        if not messages:
            logging.info("No message found (status update)")
            return {"status": "ignored"}

        message = messages[0]

        if "text" not in message:
            logging.info("Non-text message received")
            return {"status": "ignored"}

        user_msg = message["text"]["body"]
        user_id = message["from"]

        logging.info(f"Message from {user_id}: {user_msg}")

        if user_msg.lower() in ["reset", "clear", "start over"]:
            reset_user(user_id)
            reply = "Conversation reset. How can I help you now?"

        elif user_msg.lower() in ["hi", "hello", "hey"]:
            reply = "Hey! How can I help you today?"

        else:
            reply = generate_reply(user_id, user_msg)

        logging.info(f"Reply to {user_id}: {reply}")

        send_whatsapp_message(user_id, reply)

        return {"status": "ok"}

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return {"status": "error"}
