from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

# Команда /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я бот для учета финансов. Используй /help для списка команд.")

# Команда /help
def help(update: Update, context: CallbackContext):
    update.message.reply_text("Доступные команды:\n/add - добавить транзакцию\n/list - посмотреть транзакции")

# Команда /add
def add(update: Update, context: CallbackContext):
    try:
        user_id = update.message.from_user.id
        args = context.args
        amount = float(args[0])
        category = args[1]
        type_ = args[2]  # "доход" или "расход"

        # Отправляем запрос к API
        response = requests.post(
            "http://localhost:8000/add_transaction",
            json={"user_id": user_id, "amount": amount, "category": category, "type": type_}
        )
        update.message.reply_text(response.json()["message"])
    except Exception as e:
        update.message.reply_text(f"Ошибка: {e}")

# Команда /list
def list_transactions(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    response = requests.get(f"http://localhost:8000/get_transactions/{user_id}")
    transactions = response.json()["transactions"]
    if transactions:
        update.message.reply_text("\n".join([str(t) for t in transactions]))
    else:
        update.message.reply_text("Транзакций нет.")

# Запуск бота
updater = Updater("YOUR_TELEGRAM_BOT_TOKEN")
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("help", help))
updater.dispatcher.add_handler(CommandHandler("add", add))
updater.dispatcher.add_handler(CommandHandler("list", list_transactions))

updater.start_polling()
updater.idle()