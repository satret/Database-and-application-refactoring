from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from bot.handlers.start import start
from bot.handlers.help import help
from bot.handlers.add_user import add_user
from bot.handlers.add_transaction import add_transaction
from bot.handlers.list_transactions import list_transactions
from bot.handlers.select_user import select_user, process_user_selection
from bot.handlers.delete_transaction import delete_transaction
from bot.handlers.delete_user import delete_user
from bot.constants import SELECTING_USER


def main():
    application = Application.builder().token("").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("add_user", add_user))
    application.add_handler(CommandHandler("add", add_transaction))
    application.add_handler(CommandHandler("list", list_transactions))
    application.add_handler(CommandHandler("delete", delete_transaction))
    application.add_handler(CommandHandler("delete_user", delete_user))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("select_user", select_user)],
        states={
            SELECTING_USER: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_user_selection)],
        },
        fallbacks=[],
    )
    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
