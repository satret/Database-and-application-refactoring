from bot.utils.database import execute_query


async def add_transaction(update, context):
    try:
        selected_user = context.user_data.get('selected_user')
        if selected_user is None:
            await update.message.reply_text("Ошибка: выберите пользователя с помощью /select_user.")
            return

        args = update.message.text.split()[1:]

        if len(args) != 3:
            await update.message.reply_text("Ошибка: неверный формат команды. Используй /add <сумма> <категория> <тип>")
            return

        amount = float(args[0])
        category = args[1]
        type_ = args[2]

        execute_query(
            "INSERT INTO transactions (user_id, amount, category, type) VALUES (%s, %s, %s, %s)",
            (selected_user, amount, category, type_)
        )

        await update.message.reply_text(f"Транзакция добавлена: {amount} {category} ({type_})")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")
