from bot.utils.database import execute_query


async def stats(update, context):
    try:
        selected_user = context.user_data.get('selected_user')
        if selected_user is None:
            await update.message.reply_text("Ошибка: выберите пользователя с помощью /select_user.")
            return

        total_income = execute_query(
            "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE user_id = %s AND type = 'доход'",
            (selected_user,),
            fetchone=True
        )[0]

        total_expense = execute_query(
            "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE user_id = %s AND type = 'расход'",
            (selected_user,),
            fetchone=True
        )[0]

        categories = execute_query(
            "SELECT category, SUM(amount) FROM transactions WHERE user_id = %s GROUP BY category",
            (selected_user,),
            fetchall=True
        )

        response = (
            "📊 *Статистика:*\n\n"
            f"💵 *Общий доход:* {total_income:.2f}\n"
            f"💸 *Общий расход:* {total_expense:.2f}\n\n"
            "📂 *Распределение по категориям:*\n"
        )

        for category, amount in categories:
            response += f"- {category}: {amount:.2f}\n"

        await update.message.reply_text(response, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")
