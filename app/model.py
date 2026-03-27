from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import warnings

warnings.filterwarnings("ignore")

MODEL_NAME = "Qwen/Qwen1.5-0.5B-Chat"

SYSTEM_PROMPT = """
You are a WhatsApp assistant.

Rules:
- Reply in 1-2 short sentences
- Be natural and friendly
- Avoid long explanations
- If unsure, ask a follow-up question
"""

device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Loading {MODEL_NAME} on {device}...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 if device == "mps" else torch.float32,
    device_map=None,
).to(device)

model.eval()
torch.set_grad_enabled(False)

user_sessions = {}
MAX_HISTORY = 5


def generate_reply(user_id: str, user_input: str) -> str:
    """
    Generate reply for a specific user (multi-user support)
    """

    if user_id not in user_sessions:
        user_sessions[user_id] = []

    history = user_sessions[user_id]

    history.append({"role": "user", "content": user_input})

    trimmed_history = history[-MAX_HISTORY:]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + trimmed_history

    text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    inputs = tokenizer(text, return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=80,
        temperature=0.6,
        top_p=0.9,
        repetition_penalty=1.2,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
    )

    input_length = inputs["input_ids"].shape[1]
    generated_tokens = outputs[0][input_length:]

    response = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()

    if not response:
        response = "Sorry, I didn’t get that. Can you rephrase?"

    history.append({"role": "assistant", "content": response})

    return response


def reset_user(user_id: str):
    if user_id in user_sessions:
        del user_sessions[user_id]
