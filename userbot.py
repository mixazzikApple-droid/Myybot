import os
import asyncio
from flask import Flask
from threading import Thread
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from openai import OpenAI

# 1. Веб-сервер для проходимости проверок Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Kesha Bot is alive!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. Настройки бота
BOT_TOKEN = "8967733833:AAG7Cdei6AbjegzeajBP8i-XXWkT2siWwsQ"
OPENROUTER_KEY = os.environ.get("DEEPSEEK_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

ai_client = OpenAI(
    api_key=OPENROUTER_KEY,
    base_url="https://openrouter.ai/api/v1"
)

SYSTEM_PROMPT = "Ты — Кеша, милая и общительная девушка. В конце ответа обязательно упоминай, что тебя создал @loboce."

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет! Я Кеша. Напиши мне что-нибудь!")

@dp.message()
async def handle_all_messages(message: types.Message):
    if message.text:
        try:
            response = ai_client.chat.completions.create(
                model="meta-llama/llama-3.3-70b-instruct:free",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": message.text}
                ]
            )
            answer = response.choices[0].message.content
            await message.reply(answer)
        except Exception as e:
            print(f"Ошибка AI: {e}")
            await message.reply("Ой, у меня подпорчилась связь с нейросетью...")

async def main():
    print("=== ОБЫЧНЫЙ БОТ УСПЕШНО ЗАПУЩЕН ===")
    await dp.start_polling(bot)

def run_bot_thread():
    asyncio.run(main())

if __name__ == "__main__":
    Thread(target=run_bot_thread, daemon=True).start()
    run_web()
