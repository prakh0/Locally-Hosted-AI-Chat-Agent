#Locally Hosted AI Communication Assistant (WhatsApp + Gmail)

An end-to-end AI automation system that **reads, understands, and replies** to messages from:

-  WhatsApp (via webhook API)  
-  Gmail (via Gmail API)  

Powered by a locally running **Qwen LLM**, this system generates intelligent, human-like replies without relying on external paid APIs.

---

## Overview

This project demonstrates how to build a **real-world AI assistant** that integrates with:

- WhatsApp (via Meta Cloud API + Webhooks)
- Gmail (via Gmail API + OAuth)
- Local LLM (Qwen via Hugging Face)

Unlike typical AI apps, this runs **fully locally** without paid APIs.

---

# KEY Features

- Real-time WhatsApp auto-replies  
- Automated Gmail responses  
- Multi-user session memory  
- Local LLM inference (Qwen 0.5B)  
- Email cleaning & truncation  
- Secure environment variable handling  

---

# Architecture

## WhatsApp Flow (Webhook-based)

    ┌──────────────┐
    │ WhatsApp API │
    └──────┬───────┘
           │  (Webhook via ngrok)
           ▼
    ┌──────────────┐
    │  FastAPI App │   ← main.py
    └──────┬───────┘
           ▼
    ┌──────────────┐
    │  LLM Model   │   ← model.py
    └──────────────┘

---

## Gmail Flow (Independent Script)

    ┌──────────────┐
    │  Gmail API   │
    └──────┬───────┘
           ▼
    ┌──────────────┐
    │ Gmail Script │   ← gmail.py
    └──────┬───────┘
           ▼
    ┌──────────────┐
    │  LLM Model   │   ← model.py
    └──────────────┘

---

## Setup Guide
1. Clone Repo
```
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO 
```
2. Environment Setup
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
3. Configure Environment Variables

Create .env:
```
EMAIL=your_email@gmail.com
OAUTH_CREDENTIALS_FILE=Oauth_cred_chatbot_gmail.json
VERIFY_TOKEN=your_verify_token
ACCESS_TOKEN=your_whatsapp_access_token
PHONE_NUMBER_ID=your_phone_number_id
```

---

## API Setup
1. WhatsApp (Meta Cloud API)
-Create app → Add WhatsApp
```Get ACCESS_TOKEN, PHONE_NUMBER_ID```
-Set webhook:
```https://your-ngrok-url/webhook```
- ngrok
```ngrok config add-authtoken YOUR_TOKEN
ngrok http 8000
```
2. Gmail API
Enable Gmail API in Google Cloud
Setup OAuth Consent Screen
Download credentials JSON

---

## Environment Setup

- Create a .env file:
  ```
  EMAIL=your_email@gmail.com
  OAUTH_CREDENTIALS_FILE=Oauth_cred_chatbot_gmail.json
  VERIFY_TOKEN=your_verify_token
  ACCESS_TOKEN=your_whatsapp_access_token
  PHONE_NUMBER_ID=your_phone_number_id
  ```

  ---
  
## Running the Application
-- Running the App
```
uvicorn main:app --reload
ngrok http 8000
python gmail.py
```
## Core Components

### [main.py](./app/main.py)

- FastAPI webhook server  
- Handles WhatsApp events  
- Routes messages to LLM  

### [gmail.py](./app/gmail.com)

- Fetches unread emails  
- Cleans + truncates content  
- Sends AI-generated replies  

### [model.py](./app/model.py)

- Loads Qwen LLM  
- Maintains session memory  
- Generates responses using chat templates  

| File      | Responsibility                     |
|----------|-----------------------------------|
| main.py  | WhatsApp webhook handler          |
| gmail.py | Email processing & replies        |
| model.py | LLM + session memory              |

---

## Performance Notes

- First run loads model into memory (~5–10 sec)  
- CPU inference: ~2–4 sec per response  
- Input size significantly affects latency  

---

## Tech Stack

- FastAPI
- Qwen 0.5B 
- Flask
- Gmail API
- WhatsApp API
- ngrok

---
