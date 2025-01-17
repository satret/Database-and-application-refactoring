# bot/handlers/help.py

async def help(update, context):
    help_text = """
Доступные команды:
/add_user - зарегистрироваться в системе
/add <сумма> <категория> <тип> - добавить транзакцию (например, /add 100 Еда расход)
/list - посмотреть список транзакций
/select_user - поменять пользователя.
    """
    await update.message.reply_text(help_text)