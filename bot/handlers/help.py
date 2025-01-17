async def help(update, context):
    help_text = """
Доступные команды:
/add_user - зарегистрироваться в системе
/add <сумма> <категория> <тип> - добавить транзакцию (например, /add 100 Еда расход)
/list - посмотреть список транзакций
/select_user - поменять пользователя.
/delete <id_транзакции> - удалить транзакцию
/delete_user <user> - удалить пользователя
    """
    await update.message.reply_text(help_text)
