from bot.utils.database import execute_query


async def edit_transaction(update, context):
    try:
        args = update.message.text.split()[1:]

        if len(args) != 4:
            await update.message.reply_text(
                "Ошибка: неверный формат команды. Используй /edit <id_транзакции> <сумма> <категория> <тип>")
            return

        transaction_id = int(args[0])
        amount = float(args[1])
        category = args[2]
        type_ = args[3]

        result = execute_query(
            "SELECT * FROM transactions WHERE id = %s",
            (transaction_id,),
            fetchone=True
        )

        if not result:
            await update.message.reply_text(f"Ошибка: транзакция с ID {transaction_id} не найдена.")
            return

        execute_query(
            "UPDATE transactions SET amount = %s, category = %s, type = %s WHERE id = %s",
            (amount, category, type_, transaction_id)
        )

        await update.message.reply_text(f"Транзакция с ID {transaction_id} успешно обновлена!")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")
