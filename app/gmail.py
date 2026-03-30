import os
import base64
import time
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from .model import generate_reply
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
EMAIL = os.getenv("EMAIL")


def generate_gmail_token():
    flow = InstalledAppFlow.from_client_secrets_file(
        os.getenv("OAUTH_CREDENTIALS_FILE"),
        SCOPES,
    )

    creds = flow.run_local_server(port=0)
    print("Access token generated!")

    with open("token.json", "w") as token:
        token.write(creds.to_json())

    print("Token saved to token.json")


def get_gmail_service():
    try:
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        return build("gmail", "v1", credentials=creds)
    except Exception as e:
        print("Error loading credentials:", e)
        raise


def get_unread_messages(service):
    results = (
        service.users()
        .messages()
        .list(userId="me", labelIds=["UNREAD"], maxResults=5)
        .execute()
    )
    return results.get("messages", [])


def get_email_details(service, msg_id):
    message = service.users().messages().get(userId="me", id=msg_id).execute()
    headers = message["payload"]["headers"]

    subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
    sender = next((h["value"] for h in headers if h["name"] == "From"), "")

    body = ""

    try:
        if "parts" in message["payload"]:
            for part in message["payload"]["parts"]:
                if part["mimeType"] == "text/plain":
                    data = part["body"]["data"]
                    body = base64.urlsafe_b64decode(data).decode()
                    break
        else:
            data = message["payload"]["body"]["data"]
            body = base64.urlsafe_b64decode(data).decode()
    except Exception as e:
        print("Error decoding email body:", e)

    return sender, subject, body


def clean_email(text):
    cleaned = text.split("On ")[0]
    return cleaned.strip()[:1000]


def send_reply(service, to, subject, body):
    message = MIMEText(body)
    message["to"] = to
    message["subject"] = "Re: " + subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service.users().messages().send(userId="me", body={"raw": raw}).execute()


def auto_reply():
    service = get_gmail_service()
    messages = get_unread_messages(service)

    if not messages:
        print("No new emails")
        return

    for msg in messages:
        msg_id = msg["id"]

        sender, subject, body = get_email_details(service, msg_id)

        print(f"\n From: {sender}")
        print(f"Subject: {subject}")

        if "noreply" in sender.lower() or "no-reply" in sender.lower():
            print("Skipping no-reply email")
            continue

        if EMAIL and EMAIL.lower() in sender.lower():
            print("Skipping self email")
            continue

        if not body.strip():
            print("Empty email")
            continue

        cleaned_body = clean_email(body)

        try:
            reply = generate_reply(sender, cleaned_body)

            send_reply(service, sender, subject, reply)
            print("Replied successfully")

            service.users().messages().modify(
                userId="me", id=msg_id, body={"removeLabelIds": ["UNREAD"]}
            ).execute()

            time.sleep(2)

        except Exception as e:
            print("Error processing email:", e)


if __name__ == "__main__":
    while True:
        print("\n Checking for new emails...")
        auto_reply()
        time.sleep(20)
