import logging
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Задайте токен вашего бота и ID чата для пересылки сообщений
TOKEN = 'bot-token'
FORWARD_CHAT_ID = '-123456789'

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Команда /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "👊 Привет!\n"
        "Тут ты можешь предложить свою новость для нашего канала: @byxarek\n\n"
        "Просто отправь свой мем/статью/любой другой материал боту и он будет рассмотрен.\n"
        "Спасибо!"
    )

# Обработка сообщений и пересылка в отдельный чат
async def handle_message(update: Update, context: CallbackContext) -> None:
    # Пересылка сообщения в отдельный чат
    bot: Bot = context.bot
    await bot.forward_message(chat_id=FORWARD_CHAT_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
    
    # Ответ пользователю
    await update.message.reply_text("🫡 Принято, спасибо!")

def main() -> None:
    # Создание приложения
    application = Application.builder().token(TOKEN).build()
    
    # Добавление обработчиков команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_message))
    
    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
