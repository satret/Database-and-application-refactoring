# bot/bot.py

from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from bot.handlers.start import start
from bot.handlers.help import help
from bot.handlers.add_user import add_user
from bot.handlers.add_transaction import add_transaction
from bot.handlers.list_transactions import list_transactions
from bot.handlers.select_user import select_user, process_user_selection
from bot.constants import SELECTING_USER  # Импортируем константу

def main():
    # Создаем Application
    application = Application.builder().token("YOUR_BOT_TOKEN").build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("add_user", add_user))
    application.add_handler(CommandHandler("add", add_transaction))
    application.add_handler(CommandHandler("list", list_transactions))

    # ConversationHandler для выбора пользователя
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("select_user", select_user)],  # Точка входа
        states={
            SELECTING_USER: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_user_selection)],
        },
        fallbacks=[],  # Обработчики для отмены или завершения
    )
    application.add_handler(conv_handler)

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()