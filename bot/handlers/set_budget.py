from bot.utils.database import execute_query


async def set_budget(update, context):
    try:
        selected_user = context.user_data.get('selected_user')
        if selected_user is None:
            await update.message.reply_text("Ошибка: выберите пользователя с помощью /select_user.")
            return

        args = update.message.text.split()[1:]

        if len(args) != 2:
            await update.message.reply_text(
                "Ошибка: неверный формат команды. Используй /set_budget <категория> <лимит>")
            return

        category = args[0]
        budget_amount = float(args[1])

        existing_budget = execute_query(
            "SELECT * FROM budgets WHERE user_id = %s AND category = %s",
            (selected_user, category),
            fetchone=True
        )

        if existing_budget:
            execute_query(
                "UPDATE budgets SET budget_amount = %s WHERE user_id = %s AND category = %s",
                (budget_amount, selected_user, category)
            )
            await update.message.reply_text(f"Бюджет для категории '{category}' обновлён: {budget_amount:.2f}")
        else:
            execute_query(
                "INSERT INTO budgets (user_id, category, budget_amount) VALUES (%s, %s, %s)",
                (selected_user, category, budget_amount)
            )
            await update.message.reply_text(f"Бюджет для категории '{category}' установлен: {budget_amount:.2f}")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")
