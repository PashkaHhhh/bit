import asyncio
import random
import datetime
import requests
from io import BytesIO

from aiogram import Bot, Dispatcher, types

# ──────────────────── ВСТАВЬ СЮДА СВОИ ДАННЫЕ ────────────────────
BOT_TOKEN = "7470711434:AAFEZYOH2S1gM05j74z4OSr 3jGYwFQLy9cl"          # от @BotFather
CHANNEL_ID = "@kinoshizik"                            # или -1001234567890
ADMIN_ID = 862771912                                      # твой ID от @userinfobot

REPLICATE_TOKEN = "r8_5jMeWoscEOV X5YP7abk25gllw F0cB7BF"       # от replicate.com

GROQ_API_KEY    = "gsk_i8E6osaEhGAEnltq69pmWGdyb3FYW 20gTPb31U4LfHQXDo42cZuD"         # https://console.groq.com/keys
# ─────────────────────────────────────────────────────────────────────

from aiogram import Bot, Dispatcher
from aiogram.types import DefaultBotProperties

bot = Bot(token="7470711434:AAFEZYoH2S1gM05j74z4OSr3jGYwFQLy9cI")
dp = Dispatcher(bot=bot, default=DefaultBotProperties(parse_mode="HTML"))

# Темы постов про кино, сериалы и аниме (можно добавлять свои)
THEMES = [
    "Интерстеллар в стиле аниме Макото Синкай",
    "Джокер 2019 как герой тёмного фэнтези",
    "Дюна в японской гравюре укиё-э",
    "Бегущий по лезвию 2049 в неоновом ретро-вейве",
    "Начало (Inception) в эстетике Studio Ghibli",
    "Матрица в стиле синтивейв 80-х",
    "Аркейн как гиперреалистичная картина",
    "Тёмный рыцарь в самурайской эстетике",
    "Аватар в жанре хоррор-аниме",
    "Одни из нас в киберпанк Токио ночью",
    "Оппенгеймер в стиле ретро-футуризма 50-х",
    "Ведьмак Netflix как классическое аниме 90-х",
]

# Генерация картинки Flux.1-schnell через Replicate
async def make_image(theme: str) -> BytesIO:
    r = requests.post("https://api.replicate.com/v1/predictions",
        json={
            "version": "c6c2b1f312b0d135e4750b2779e1c158e1e7e7204a65f43f9c9c6f5e17c88c3b",
            "input": {
                "prompt": f"{theme}, cinematic masterpiece, ultra detailed, sharp focus, 8k",
                "num_outputs": 1,
                "aspect_ratio": "1:1",
                "output_format": "png"
            }
        },
        headers={"Authorization": f"Token {REPLICATE_TOKEN}"}
    ).json()

    prediction_id = r["id"]
    
    while True:
        result = requests.get(
            f"https://api.replicate.com/v1/predictions/{prediction_id}",
            headers={"Authorization": f"Token {REPLICATE_TOKEN}"}
        ).json()
        
        if result["status"] == "succeeded":
            img_url = result["output"][0]
            return BytesIO(requests.get(img_url).content)
        elif result["status"] in ["failed", "canceled"]:
            raise Exception("Картинка не сгенерировалась")
        await asyncio.sleep(2)

# Генерация подписи через Groq
async def make_caption(theme: str) -> str:
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            json={
                "model": "llama-3.1-70b-versatile",
                "messages": [
                    {"role": "system", "content": "Ты пишешь супер-вирусные посты для Telegram-канала про кино и аниме. Пиши на русском, добавляй эмодзи, максимум 300 символов, в конце вопрос или призыв + хэштеги."},
                    {"role": "user", "content": theme}
                ],
                "temperature": 0.9,
                "max_tokens": 250
            },
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            timeout=25
        ).json()
        return r["choices"][0]["message"]["content"].strip()
    except:
        return f"А что если… {theme} ?..\n\n#кино #аниме #aiart #flux"

# Если ты пишешь боту в личку — он сразу делает пост
@dp.message()
async def manual_post(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer("Генерирую шедевр… (10–20 сек)")

    theme = random.choice(THEMES)
    image = await make_image(theme)
    caption = await make_caption(theme)

    await bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=types.BufferedInputFile(image.getvalue(), "cinema.png"),
        caption=caption
    )
    await message.answer("Пост отправлен в канал!")

# Автоматические посты 3 раза в день
async def auto_post():
    while True:
        now = datetime.datetime.now()
        if now.hour in [10, 16, 21] and now.minute == 0:
            theme = random.choice(THEMES)
            image = await make_image(theme)
            caption = await make_caption(theme)
            
            await bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=types.BufferedInputFile(image.getvalue(), "art.png"),
                caption=caption
            )
            print(f"Автопост {now.strftime('%d.%m %H:%M')} — {theme[:50]}…")
        
        await asyncio.sleep(55)

async def main():
    print("Бот запущен! Посты в 10:00, 16:00 и 21:00 по МСК")
    asyncio.create_task(auto_post())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
