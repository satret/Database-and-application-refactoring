from bot.utils.database import execute_query
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def add_transaction(update, context):
    try:
        selected_user = context.user_data.get('selected_user')
        if selected_user is None:
            await update.message.reply_text("Ошибка: выберите пользователя с помощью /select_user.")
            return

        args = update.message.text.split()[1:]

        if len(args) != 3:
            await update.message.reply_text("Ошибка: неверный формат команды. Используй /add <сумма> <категория> <тип>")
            return

        amount = float(args[0])
        category = args[1]
        type_ = args[2]

        current_date = datetime.now()

        logger.info(
            f"Добавление транзакции: user_id={selected_user}, amount={amount}, category={category}, type={type_}")

        execute_query(
            "INSERT INTO transactions (user_id, amount, category, type, date) VALUES (%s, %s, %s, %s, %s)",
            (selected_user, amount, category, type_, current_date)
        )

        if type_ == "расход":
            # Логируем начало проверки бюджета
            logger.info(f"Проверка бюджета для категории: {category}")

            budget = execute_query(
                "SELECT budget_amount FROM budgets WHERE user_id = %s AND category = %s",
                (selected_user, category),
                fetchone=True
            )

            if budget:
                logger.info(f"Бюджет для категории '{category}': {budget[0]}")

                total_expenses = execute_query(
                    "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE user_id = %s AND category = %s AND type = 'расход'",
                    (selected_user, category),
                    fetchone=True
                )[0]

                logger.info(f"Общие расходы по категории '{category}': {total_expenses}")

                if total_expenses > budget[0]:
                    logger.info(f"Превышение бюджета: общие расходы {total_expenses} > лимит {budget[0]}")
                    await update.message.reply_text(
                        f"⚠️ Внимание: превышен бюджет для категории '{category}'!\n"
                        f"Лимит: {budget[0]:.2f}, текущие расходы: {total_expenses:.2f}"
                    )
                else:
                    logger.info(f"Бюджет не превышен: общие расходы {total_expenses} <= лимит {budget[0]}")
            else:
                logger.info(f"Бюджет для категории '{category}' не установлен.")

        await update.message.reply_text(f"Транзакция добавлена: {amount} {category} ({type_})")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text(f"Ошибка: {e}")
