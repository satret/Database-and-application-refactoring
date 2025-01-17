from telegram.ext import ConversationHandler
from bot.constants import SELECTING_USER
from bot.utils.database import execute_query


async def select_user(update, context):
    try:
        user_id = update.message.from_user.id

        users = execute_query(
            "SELECT id, username FROM users WHERE user_id = %s",
            (user_id,),
            fetchall=True
        )

        if not users:
            await update.message.reply_text("У вас нет зарегистрированных пользователей. Используйте /add_user.")
            return ConversationHandler.END

        user_list = "Ваши пользователи:\n"
        for user in users:
            user_list += f"{user[0]} - {user[1]}\n"
        user_list += "Введите ID пользователя, которого хотите выбрать."

        await update.message.reply_text(user_list)

        return SELECTING_USER
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")
        return ConversationHandler.END


async def process_user_selection(update, context):
    try:
        user_id = update.message.from_user.id
        selected_id = int(update.message.text)

        user = execute_query(
            "SELECT id, username FROM users WHERE user_id = %s AND id = %s",
            (user_id, selected_id),
            fetchone=True
        )

        if user is None:
            await update.message.reply_text("Ошибка: пользователь не найден.")
            return ConversationHandler.END

        context.user_data['selected_user'] = user[0]
        await update.message.reply_text(f"Выбран пользователь: {user[1]} (ID: {user[0]})")
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("Ошибка: введите число (ID пользователя).")
        return SELECTING_USER
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")
        return ConversationHandler.END
