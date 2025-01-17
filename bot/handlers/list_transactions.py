# bot/handlers/list_transactions.py

from bot.utils.database import execute_query

async def list_transactions(update, context):
    try:
        # Получаем выбранного пользователя из user_data
        selected_user = context.user_data.get('selected_user')
        if selected_user is None:
            await update.message.reply_text("Ошибка: выберите пользователя с помощью /select_user.")
            return

        # Получаем список транзакций для выбранного пользователя
        transactions = execute_query(
            "SELECT * FROM transactions WHERE user_id = %s",
            (selected_user,),
            fetchall=True
        )

        if transactions:
            response = "Ваши транзакции:\n"
            for transaction in transactions:
                response += f"{transaction[2]} {transaction[3]} ({transaction[4]}) - {transaction[5]}\n"
            await update.message.reply_text(response)
        else:
            await update.message.reply_text("У вас пока нет транзакций.")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")