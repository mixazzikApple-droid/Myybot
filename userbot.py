import os
import asyncio
from flask import Flask
from threading import Thread
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from openai import OpenAI

# Микро-сервер для проходимости проверок Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Kesha is alive!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Настройки юзербота
API_ID = 39735400
API_HASH = "03b7fe933d96839031112139c92bd702"
SESSION_STRING = os.environ.get("SESSION_STRING")
OPENROUTER_KEY = os.environ.get("DEEPSEEK_KEY")

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# Подключение к бесплатной нейросети через OpenRouter
ai_client = OpenAI(
    api_key=OPENROUTER_KEY,
    base_url="https://openrouter.ai/api/v1"
)

SYSTEM_PROMPT = "Ты — Кеша, милая и общительная девушка. В конце ответа обязательно упоминай, что тебя создал @loboce."

@client.on(events.NewMessage)
async def handle_message(event):
    if event.text and "кеша" in event.text.lower():
        try:
            response = ai_client.chat.completions.create(
                model="meta-llama/llama-3.3-70b-instruct:free",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": event.text}
                ]
            )
            answer = response.choices[0].message.content
            await event.reply(answer)
        except Exception as e:
            print(f"Ошибка AI: {e}")

async def main():
    await client.start()
    print("Юзербот запущен!")
    await client.run_until_disconnected()

if __name__ == "__main__":
    Thread(target=run_web, daemon=True).start()
    asyncio.run(main())
