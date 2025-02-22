import logging
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

# Задайте токен вашего бота и ID чата для пересылки сообщений
TOKEN = ''
FORWARD_CHAT_ID = '-1002485'  # ID группы, куда пересылаются сообщения

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Словарь сообщений для локализации
MESSAGES = {
    'ru': {
        'start': "👊 Привет!\nТут ты можешь предложить свою идею для нашего сервера/форума/ботов!\n\nПросто отправь свою идею боту в личные сообщения, и она будет рассмотрена.\nСпасибо!",
        'thanks': "🫡 Принято, спасибо!",
        'error': "❌ Произошла ошибка при отправке. Попробуйте позже.",
        'confirm': "Ваше предложение:\n{msg}\n\nОтправить?",
        'canceled': "❌ Отменено.",
        'lang_set': "Язык установлен: Русский",
        'lang_error': "Пожалуйста, выберите 'ru' или 'en'. Пример: /lang ru",
        'help': (
            "📖 **Помощь по боту**\n\n"
            "Этот бот позволяет предлагать идеи для нашего сервера, форума или ботов. "
            "Ваши предложения будут отправлены на рассмотрение администрации.\n\n"
            "**Как использовать:**\n"
            "1. Отправьте сообщение с вашей идеей (текст, фото, видео, голосовое сообщение или документ).\n"
            "2. Подтвердите отправку, нажав 'Отправить'.\n"
            "3. Дождитесь ответа (если администрация решит ответить).\n\n"
            "**Доступные команды:**\n"
            "- /start — Начать работу с ботом.\n"
            "- /help — Показать это сообщение.\n"
            "- /lang <ru или en> — Сменить язык (например, /lang en).\n\n"
            "Спасибо за ваши идеи!"
        )
    },
    'en': {
        'start': "👊 Hi!\nHere you can suggest your idea for our server/forum/bots!\n\nJust send your idea to the bot in private messages, and it will be reviewed.\nThanks!",
        'thanks': "🫡 Accepted, thanks!",
        'error': "❌ An error occurred while sending. Try again later.",
        'confirm': "Your suggestion:\n{msg}\n\nSend it?",
        'canceled': "❌ Canceled.",
        'lang_set': "Language set: English",
        'lang_error': "Please choose 'ru' or 'en'. Example: /lang en",
        'help': (
            "📖 **Bot Help**\n\n"
            "This bot allows you to suggest ideas for our server, forum, or bots. "
            "Your suggestions will be sent to the administration for review.\n\n"
            "**How to use:**\n"
            "1. Send a message with your idea (text, photo, video, voice message, or document).\n"
            "2. Confirm sending by clicking 'Send'.\n"
            "3. Wait for a response (if the administration decides to reply).\n\n"
            "**Available commands:**\n"
            "- /start — Start working with the bot.\n"
            "- /help — Show this message.\n"
            "- /lang <ru or en> — Change language (e.g., /lang ru).\n\n"
            "Thank you for your ideas!"
        )
    }
}

# Функция для получения или установки языка
def get_user_language(update: Update, context: CallbackContext) -> str:
    # Если язык уже сохранен в context.user_data, возвращаем его
    if 'language' in context.user_data:
        return context.user_data['language']
    
    # Иначе определяем язык по Telegram и сохраняем
    user_lang = update.message.from_user.language_code if update.message.from_user.language_code else 'ru'
    lang = user_lang[:2] if user_lang[:2] in MESSAGES else 'ru'
    context.user_data['language'] = lang
    return lang

# Команда /start
async def start(update: Update, context: CallbackContext) -> None:
    lang = get_user_language(update, context)
    await update.message.reply_text(MESSAGES[lang]['start'])

# Команда /help
async def help_command(update: Update, context: CallbackContext) -> None:
    lang = get_user_language(update, context)
    await update.message.reply_text(MESSAGES[lang]['help'])

# Команда /lang для переключения языка
async def set_language(update: Update, context: CallbackContext) -> None:
    if not context.args or context.args[0] not in MESSAGES:
        lang = get_user_language(update, context)
        await update.message.reply_text(MESSAGES[lang]['lang_error'])
        return
    
    new_lang = context.args[0]
    context.user_data['language'] = new_lang
    await update.message.reply_text(MESSAGES[lang]['lang_set'])

# Обработка сообщений и запрос подтверждения
async def handle_message(update: Update, context: CallbackContext) -> None:
    # Проверяем, что сообщение пришло из личного чата, а не из группы назначения
    if str(update.message.chat_id) == FORWARD_CHAT_ID:
        logger.info(f"Пропущено сообщение из группы {FORWARD_CHAT_ID}")
        return

    # Сохраняем сообщение для дальнейшей пересылки
    context.user_data['pending_message'] = update.message.message_id
    lang = get_user_language(update, context)

    # Формируем текст для подтверждения
    msg_content = update.message.text or update.message.caption or ("Медиа без текста" if lang == 'ru' else "Media without text")
    confirm_text = MESSAGES[lang]['confirm'].format(msg=msg_content)

    # Создаем кнопки "Отправить" и "Отменить" с учетом языка
    keyboard = [
        [InlineKeyboardButton("Отправить" if lang == 'ru' else "Send", callback_data='send'),
         InlineKeyboardButton("Отменить" if lang == 'ru' else "Cancel", callback_data='cancel')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем запрос на подтверждение
    await update.message.reply_text(confirm_text, reply_markup=reply_markup)

# Обработка нажатий на кнопки
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    lang = get_user_language(query, context)  # Используем сохраненный язык
    bot: Bot = context.bot

    if query.data == 'send':
        message_id = context.user_data.get('pending_message')
        try:
            # Пересылка сообщения в группу
            await bot.forward_message(
                chat_id=FORWARD_CHAT_ID,
                from_chat_id=query.message.chat_id,
                message_id=message_id
            )
            logger.info(f"Сообщение переслано в {FORWARD_CHAT_ID} от {query.message.chat_id}")
            await query.edit_message_text(MESSAGES[lang]['thanks'])
        except Exception as e:
            logger.error(f"Ошибка при пересылке сообщения: {e}")
            await query.edit_message_text(MESSAGES[lang]['error'])
    else:
        await query.edit_message_text(MESSAGES[lang]['canceled'])

def main() -> None:
    # Создание приложения
    application = Application.builder().token(TOKEN).build()

    # Добавление обработчиков команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("lang", set_language))
    # Обрабатываем текст, фото, видео, голосовые сообщения и документы
    application.add_handler(MessageHandler(
        filters.TEXT | filters.PHOTO | filters.VIDEO | filters.VOICE | filters.Document.ALL,
        handle_message
    ))
    application.add_handler(CallbackQueryHandler(button))

    # Запуск бота
    logger.info("Бот запущен!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
