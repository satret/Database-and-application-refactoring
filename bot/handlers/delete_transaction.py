from bot.utils.database import execute_query

async def delete_transaction(update, context):
    try:
        args = update.message.text.split()[1:]

        if len(args) != 1:
            await update.message.reply_text("Ошибка: неверный формат команды. Используй /delete <id_транзакции>")
            return

        transaction_id = int(args[0])  # ID транзакции, которую хотят удалить
        selected_user = context.user_data.get('selected_user')

        if not selected_user:
            await update.message.reply_text("Ошибка: пользователь не выбран. Сначала выберите пользователя.")
            return

        # Получаем информацию о транзакции
        transaction = execute_query(
            "SELECT user_id FROM transactions WHERE id = %s",
            (transaction_id,),
            fetchone=True
        )

        if not transaction:
            await update.message.reply_text("Ошибка: транзакция не найдена.")
            return

        transaction_user_id = transaction[0]  # user_id владельца транзакции

        # Получаем информацию о пользователе, который ввёл команду
        user = execute_query(
            "SELECT id, role FROM users WHERE id = %s",  # Используем id, а не user_id
            (selected_user,),
            fetchone=True
        )

        if not user:
            await update.message.reply_text("Ошибка: пользователь не найден в базе данных.")
            return

        user_id = user[0]  # id пользователя из таблицы users
        role = user[1]  # роль пользователя

        # Выводим информацию для отладки
        await update.message.reply_text(
            f"Информация:\n"
            f"ID пользователя: {user_id}\n"
            f"Роль пользователя: {role}\n"
            f"ID владельца транзакции: {transaction_user_id}"
        )

        # Проверяем, может ли пользователь удалить транзакцию
        if role == "admin":
            # Админ может удалить любую транзакцию
            execute_query(
                "DELETE FROM transactions WHERE id = %s",
                (transaction_id,)
            )
            await update.message.reply_text(f"Транзакция с ID {transaction_id} удалена.")
        elif transaction_user_id == user_id:
            # Пользователь может удалить только свои транзакции
            execute_query(
                "DELETE FROM transactions WHERE id = %s",
                (transaction_id,)
            )
            await update.message.reply_text(f"Транзакция с ID {transaction_id} удалена.")
        else:
            # Если user_id транзакции не совпадает с user_id пользователя и он не админ
            await update.message.reply_text("Ошибка: у вас нет прав на удаление этой транзакции.")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")