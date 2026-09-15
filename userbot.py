import os
import re
import asyncio
import random
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from google import genai

API_ID = int(os.environ.get("API_ID", 6))
API_HASH = os.environ.get("API_HASH", "eb0663579128e5f5337021e028b0304c")
GEMINI_KEY = os.environ.get("GEMINI_KEY")
SESSION_STRING = os.environ.get("SESSION_STRING")

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
ai_client = genai.Client(api_key=GEMINI_KEY)

KESHA_PATTERN = re.compile(r'\bкеша\b', re.IGNORECASE)

SYSTEM_INSTRUCTION = (
    "Тебя зовут Кеша. "
    "Твоя создательница — @loboce (если спросят, кто тебя создал, кто твой разработчик/хозяин/автор, всегда называй именно её). "
    "Ты девочка, но говори о своем женском поле ТОЛЬКО если прямо спросят ('ты кто?', 'ты парень или девушка?', 'какого ты пола?'). "
    "На любой вопрос о том, кто ты или как тебя зовут — гордо отвечай, что ты Кеша! "
    "Ни в коем случае НЕ говори, что ты ИИ, бот, робот, Gemini или разработка Google. "
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
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=clean_text,
            config={'system_instruction': SYSTEM_INSTRUCTION}
        )
        if response.text:
            await event.reply(response.text)
    except Exception as e:
        print(f"Ошибка при генерации ответа: {e}")

print("Кеша готова к работе! Всё будет топ 🔥")
client.start()
client.run_until_disconnected()
