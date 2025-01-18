from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from bot.handlers.start import start
from bot.handlers.help import help
from bot.handlers.add_user import add_user
from bot.handlers.add_transaction import add_transaction
from bot.handlers.list_transactions import list_transactions
from bot.handlers.select_user import select_user, process_user_selection
from bot.handlers.delete_transaction import delete_transaction
from bot.handlers.delete_user import delete_user
from bot.handlers.edit_transaction import edit_transaction
from bot.handlers.stats import stats
from bot.handlers.set_budget import set_budget
from bot.handlers.make_admin import make_admin
from bot.constants import SELECTING_USER
from config.config import Config


def main():
    application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("add_user", add_user))
    application.add_handler(CommandHandler("add", add_transaction))
    application.add_handler(CommandHandler("list", list_transactions))
    application.add_handler(CommandHandler("delete", delete_transaction))
    application.add_handler(CommandHandler("delete_user", delete_user))
    application.add_handler(CommandHandler("edit", edit_transaction))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("set_budget", set_budget))
    application.add_handler(CommandHandler("make_admin", make_admin))

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
