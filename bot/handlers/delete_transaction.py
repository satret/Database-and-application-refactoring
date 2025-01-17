from bot.utils.database import execute_query


async def delete_transaction(update, context):
    try:
        args = update.message.text.split()[1:]

        if len(args) != 1:
            await update.message.reply_text("Ошибка: неверный формат команды. Используй /delete <id_транзакции>")
            return

        transaction_id = int(args[0])

        execute_query(
            "DELETE FROM transactions WHERE id = %s",
            (transaction_id,)
        )

        await update.message.reply_text(f"Транзакция с ID {transaction_id} удалена.")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")
