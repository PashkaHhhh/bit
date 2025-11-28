import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Логи, чтобы видеть что происходит
logging.basicConfig(level=logging.INFO)

# ВСЕ КЛЮЧИ ВШИТЫ ЖЁСТКО (чтобы точно работало)
BOT_TOKEN = "7470711434:AAFEZYoH2S1gM05j74z4OSr3jGYwFQLy9cI"
CHANNEL_ID = "@kinoshizik"        
ADMIN_ID = 862771912                  
GROQ_API_KEY = "gsk_i8E6osaEhGAEnltq69pmWGdyb3FYW 20gTPb31U4LfHQXDo42cZuD"  
REPLICATE_TOKEN = "r8_5jMeWoscEOV X5YP7abk25gllw F0cB7BF"  

# Инициализация бота (aiogram 3.13+)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

async def start_message():
    print("Бот запущен! Посты в 10:00, 16:00 и 21:00 по МСК")
    logging.info("Бот успешно запущен")

async def main():
    await start_message()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
