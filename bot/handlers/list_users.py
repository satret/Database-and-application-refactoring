# bot/handlers/list_users.py

from bot.utils.database import execute_query, is_admin
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def list_users(update, context):
    try:
        user_id = update.message.from_user.id

        # Проверяем, является ли пользователь администратором
        if not is_admin(user_id):
            logger.warning(f"Пользователь {user_id} не является администратором")
            await update.message.reply_text("Ошибка: у вас нет прав для выполнения этой команды.")
            return

        # Получаем список всех пользователей
        users = execute_query(
            "SELECT id, username, role FROM users",
            fetchall=True
        )

        if not users:
            await update.message.reply_text("В системе нет зарегистрированных пользователей.")
            return

        # Формируем сообщение со списком пользователей
        response = "📋 *Список пользователей:*\n\n"
        for user in users:
            response += f"🆔 ID: {user[0]}\n👤 Имя: {user[1]}\n🎖 Роль: {user[2]}\n————————————\n"

        await update.message.reply_text(response, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text(f"Ошибка: {e}")