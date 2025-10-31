"""
Telegram Bot для AI Image Generator Bot.

Основные функции:
- Команда /start — приветствие и кнопка "Открыть App"
- Inline button с URL на Web App
"""

import logging
from typing import Optional
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class TelegramBot:
    """Telegram Bot для AI Image Generator Bot"""

    def __init__(self, bot_token: str, web_app_url: str):
        """
        Инициализация бота.

        Args:
            bot_token: Telegram Bot API token
            web_app_url: URL Web App (например, https://your-domain.com)
        """
        self.bot_token = bot_token
        self.web_app_url = web_app_url
        self.application: Optional[Application] = None

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Обработчик команды /start.

        Отправляет приветственное сообщение с кнопкой "Открыть App".
        """
        user = update.effective_user

        # Формируем приветственное сообщение
        welcome_message = (
            f"👋 Привет, {user.mention_html()}!\n\n"
            "🎨 Добро пожаловать в AI Image Generator Bot!\n\n"
            "✨ Что я умею:\n"
            "• Виртуальная примерка одежды и аксессуаров\n"
            "• Редактирование изображений с помощью AI\n"
            "• Генерация изображений по вашим запросам\n\n"
            "🎁 Бонус:\n"
            "• 10 бесплатных действий в месяц для новых пользователей\n"
            "• Реферальная программа — приглашай друзей и получай кредиты\n\n"
            "Нажмите кнопку ниже, чтобы открыть приложение! 👇"
        )

        # Создаём inline кнопку с Web App
        keyboard = [
            [
                InlineKeyboardButton(
                    text="🚀 Открыть App",
                    web_app=WebAppInfo(url=self.web_app_url)
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Отправляем сообщение
        await update.message.reply_html(
            text=welcome_message,
            reply_markup=reply_markup
        )

        logger.info(
            f"User {user.id} (@{user.username}) started the bot"
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Обработчик команды /help.

        Отправляет справочную информацию о боте.
        """
        help_message = (
            "ℹ️ <b>Справка по AI Image Generator Bot</b>\n\n"
            "<b>Доступные команды:</b>\n"
            "/start - Открыть приложение\n"
            "/help - Показать эту справку\n\n"
            "<b>Как пользоваться:</b>\n"
            "1. Нажмите кнопку «Открыть App» в сообщении /start\n"
            "2. Выберите режим: примерка или редактирование\n"
            "3. Загрузите изображения и следуйте инструкциям\n\n"
            "<b>Монетизация:</b>\n"
            "• Freemium: 10 действий/месяц (с водяным знаком)\n"
            "• Подписки: 299₽/50, 499₽/150, 899₽/500 действий\n"
            "• Кредиты: 199₽/100 кредитов\n\n"
            "<b>Реферальная программа:</b>\n"
            "• Приглашайте друзей через реферальную ссылку в профиле\n"
            "• Получайте +10 кредитов за каждого активного друга\n\n"
            "По вопросам: @support_bot"
        )

        await update.message.reply_html(text=help_message)
        logger.info(f"User {update.effective_user.id} requested help")

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Обработчик ошибок.

        Логирует ошибки и отправляет уведомление пользователю.
        """
        logger.error(f"Exception while handling an update: {context.error}", exc_info=context.error)

        # Если есть update с сообщением, отправляем уведомление пользователю
        if isinstance(update, Update) and update.effective_message:
            error_message = (
                "⚠️ Произошла ошибка при обработке запроса.\n\n"
                "Попробуйте позже или обратитесь в поддержку."
            )
            await update.effective_message.reply_text(error_message)

    async def post_init(self, application: Application) -> None:
        """
        Выполняется после инициализации бота.

        Устанавливает описание и команды бота.
        """
        # Устанавливаем описание бота
        await application.bot.set_my_description(
            description="🎨 AI Image Generator Bot — виртуальная примерка одежды и редактирование изображений с помощью AI"
        )

        # Устанавливаем короткое описание
        await application.bot.set_my_short_description(
            short_description="🎨 Виртуальная примерка и редактирование с AI"
        )

        logger.info("Bot initialized successfully")

    def setup_handlers(self) -> None:
        """Настройка обработчиков команд"""
        if not self.application:
            raise RuntimeError("Application is not initialized")

        # Команды
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))

        # Обработчик ошибок
        self.application.add_error_handler(self.error_handler)

        logger.info("Handlers registered successfully")

    def run(self) -> None:
        """
        Запуск бота.

        Создаёт Application, регистрирует handlers и запускает polling.
        """
        # Создаём Application
        self.application = (
            Application.builder()
            .token(self.bot_token)
            .post_init(self.post_init)
            .build()
        )

        # Настраиваем обработчики
        self.setup_handlers()

        # Запускаем polling
        logger.info("Starting bot polling...")
        self.application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True  # Игнорируем старые обновления при перезапуске
        )


def create_bot(bot_token: str, web_app_url: str) -> TelegramBot:
    """
    Фабричная функция для создания экземпляра бота.

    Args:
        bot_token: Telegram Bot API token
        web_app_url: URL Web App

    Returns:
        Экземпляр TelegramBot
    """
    return TelegramBot(bot_token=bot_token, web_app_url=web_app_url)
