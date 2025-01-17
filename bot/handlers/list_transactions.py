from bot.utils.database import execute_query

async def list_transactions(update, context):
    try:
        selected_user = context.user_data.get('selected_user')
        if selected_user is None:
            await update.message.reply_text("Ошибка: выберите пользователя с помощью /select_user.")
            return

        transactions = execute_query(
            "SELECT id, amount, category, type, date FROM transactions WHERE user_id = %s ORDER BY id ASC",
            (selected_user,),
            fetchall=True
        )

        if transactions:
            response = "📝 *Ваши транзакции:*\n\n"
            for transaction in transactions:
                response += (
                    f"🆔 *ID:* {transaction[0]}\n"
                    f"💵 *Сумма:* {transaction[1]}\n"
                    f"🏷 *Категория:* {transaction[2]}\n"
                    f"📌 *Тип:* {transaction[3]}\n"
                    f"📅 *Дата:* {transaction[4]}\n"
                    "————————————\n"
                )
            await update.message.reply_text(response, parse_mode="Markdown")
        else:
            await update.message.reply_text("У вас пока нет транзакций.")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")