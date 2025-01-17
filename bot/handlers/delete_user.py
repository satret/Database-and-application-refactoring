from bot.utils.database import execute_query


async def delete_user(update, context):
    try:
        args = update.message.text.split()[1:]

        if len(args) == 0:
            await update.message.reply_text("Ошибка: укажите имя пользователя или ID. Пример: /delete_user Satret")
            return

        user_identifier = args[0]

        if user_identifier.isdigit():
            execute_query(
                "DELETE FROM users WHERE user_id = %s",
                (int(user_identifier),)
            )
        else:
            execute_query(
                "DELETE FROM users WHERE username = %s",
                (user_identifier,)
            )

        await update.message.reply_text(f"Пользователь {user_identifier} успешно удален!")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")
