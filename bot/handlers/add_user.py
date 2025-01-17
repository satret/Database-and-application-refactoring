# bot/handlers/add_user.py

from bot.utils.database import execute_query

async def add_user(update, context):
    try:
        user_id = update.message.from_user.id
        args = update.message.text.split()[1:]  # Получаем аргументы команды

        if len(args) == 0:
            await update.message.reply_text("Ошибка: укажите имя пользователя. Пример: /add_user Satret")
            return

        username = args[0]  # Имя пользователя, указанное в команде

        # Добавляем нового пользователя
        execute_query(
            "INSERT INTO users (user_id, username) VALUES (%s, %s)",
            (user_id, username)
        )

        await update.message.reply_text(f"Пользователь {username} успешно зарегистрирован!")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")