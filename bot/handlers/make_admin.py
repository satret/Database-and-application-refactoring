# bot/handlers/make_admin.py

from bot.utils.database import execute_query, is_admin
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def make_admin(update, context):
    try:
        user_id = update.message.from_user.id
        logger.info(f"Пользователь {user_id} пытается выполнить команду /make_admin")

        # Проверяем, является ли пользователь администратором
        if not is_admin(user_id):
            logger.warning(f"Пользователь {user_id} не является администратором")
            await update.message.reply_text("Ошибка: у вас нет прав для выполнения этой команды.")
            return

        args = update.message.text.split()[1:]

        if len(args) == 0:
            logger.warning("Не указано имя пользователя")
            await update.message.reply_text("Ошибка: укажите имя пользователя. Пример: /make_admin Саша")
            return

        target_username = args[0]  # Имя пользователя, которого нужно сделать администратором
        logger.info(f"Назначение пользователя {target_username} администратором")

        # Ищем пользователя по username
        user_data = execute_query(
            "SELECT id FROM users WHERE username = %s",
            (target_username,),
            fetchone=True
        )

        if not user_data:
            logger.warning(f"Пользователь {target_username} не найден")
            await update.message.reply_text(f"Ошибка: пользователь {target_username} не найден.")
            return

        target_id = user_data[0]  # Получаем id пользователя

        # Назначаем пользователя администратором
        execute_query(
            "UPDATE users SET role = 'admin' WHERE id = %s",
            (target_id,)
        )

        logger.info(f"Пользователь {target_username} (id: {target_id}) успешно назначен администратором")
        await update.message.reply_text(f"Пользователь {target_username} теперь администратор!")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text(f"Ошибка: {e}")