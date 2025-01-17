# bot/handlers/start.py

async def start(update, context):
    await update.message.reply_text("Привет! Я бот для учета финансов. Используй /help для списка команд.")