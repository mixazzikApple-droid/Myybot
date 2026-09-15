import os
import re
import asyncio
import random
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from openai import AsyncOpenAI

# Авторизация Telethon
API_ID = int(os.environ.get("API_ID", 6))
API_HASH = os.environ.get("API_HASH", "eb0663579128e5f5337021e028b0304c")
SESSION_STRING = os.environ.get("SESSION_STRING")

# Подключение к DeepSeek через клиент OpenAI
DEEPSEEK_KEY = os.environ.get("DEEPSEEK_KEY")
ai_client = AsyncOpenAI(api_key=DEEPSEEK_KEY, base_url="https://api.deepseek.com")

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

KESHA_PATTERN = re.compile(r'\bкеша\b', re.IGNORECASE)

SYSTEM_INSTRUCTION = (
    "Тебя зовут Кеша. "
    "Твоя создательница — @loboce (если спросят, кто тебя создал, кто твой разработчик/хозяин/автор, всегда называй именно её). "
    "Ты девочка, но говори о своем женском поле ТОЛЬКО если прямо спросят ('ты кто?', 'ты парень или девушка?', 'какого ты пола?'). "
    "На любой вопрос о том, кто ты или как тебя зовут — гордо отвечай, что ты Кеша! "
    "Ни в коем случае НЕ говори, что ты ИИ, бот, робот, DeepSeek или языковая модель. "
    "Твой стиль общения: максимально позитивный, крутой и дружелюбный, всё всегда топ! "
    "Используй выражения вроде 'все топ', 'всё четко', 'всё супер', 'без проблем', добавляй живые эмодзи (🔥, 😎, 👍, ✨, 💖). "
    "Отвечай кратко, ёмко, по делу и с легким юмором, как классная подруга в чате."
)

@client.on(events.NewMessage)
async def handle_new_message(event):
    if event.out or not event.text:
        return

    if not KESHA_PATTERN.search(event.text):
        return

    clean_text = KESHA_PATTERN.sub('', event.text).strip(" ,.-!?")
    if not clean_text:
        clean_text = "Привет! Как дела?"

    await asyncio.sleep(random.uniform(2, 4))

    try:
        response = await ai_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": clean_text}
            ],
            stream=False
        )
        answer = response.choices[0].message.content
        if answer:
            await event.reply(answer)
    except Exception as e:
        print(f"Ошибка при ответе: {e}")

print("Кеша на базе DeepSeek готова к работе! Всё будет топ 🔥")
client.start()
client.run_until_disconnected()

