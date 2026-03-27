# Qwen WhatsApp AI Agent

This folder contains a FastAPI-based AI agent that connects to Twilio's WhatsApp Sandbox, allowing you to chat with a locally running Qwen Large Language Model right from your phone!

## Prerequisites
- A **Twilio** account (free tier is fine).
- **ngrok** installed (to expose your local server to the web).

## Setup Instructions

### 1. Install Dependencies
Make sure you are in your project directory (`/Users/prakhar/llmplay/qwen-demo`) and activate your virtual environment:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Start the FastAPI Server
Run the local webhook server. It will download/load the Qwen model into your Mac's Memory on startup, so the first run takes a moment:
```bash
python whatsapp_agent.py
```
*The server will start on `http://127.0.0.1:8000`.*

### 3. Expose the Local Server using ngrok
In a **new terminal tab**, run:
```bash
ngrok http 8000
```
Copy the **Forwarding URL** provided by ngrok (it looks like `https://xxxx-xx-xx-xx.ngrok-free.app`).

### 4. Configure Twilio WhatsApp Sandbox
1. Log into your Twilio Console and navigate to **Messaging > Try it out > Send a WhatsApp message**.
2. Follow the prompt to connect your mobile number to the Sandbox (e.g., sending `join <sandbox-word>` to their number).
3. Go to **Sandbox Settings** (usually under Messaging > Settings > WhatsApp Sandbox Settings).
4. Under the **"WHEN A MESSAGE COMES IN"** section, paste your ngrok URL with `/webhook` at the end.
   - Example: `https://xxxx-xx-xx-xx.ngrok-free.app/webhook`
5. Save the configuration.

### 5. Chat with the AI! 🤖
Simply send a WhatsApp message to the Twilio Sandbox number, and your local Qwen model will read it, generate a response, and text it right back!
