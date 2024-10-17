import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ErrorEvent
from aiogram.types import ReplyKeyboardRemove
from aiogram_dialog import setup_dialogs, DialogManager
from aiogram_dialog.api.exceptions import UnknownIntent
from loguru import logger

from config import BASE_DIR, TELEGRAM_BOT_TOKEN
from handlers import routers
from dialogs import dialogs
from telegram_bot.dialogs import states


def include_routers(dispatcher: Dispatcher):
    dispatcher.include_routers(*routers)
    dispatcher.include_routers(*dialogs)

async def on_startup(dispatcher: Dispatcher):
    logger.info("Запуск бота...")
    # TODO: Начать соединение с базой данных
    logger.success("Бот запущен")


async def on_shutdown(dispatcher: Dispatcher):
    logger.info("Остановка бота...")
    # TODO: Прекратить соединение с базой данных
    logger.success("Бот остановлен")


def setup_dispatcher() -> Dispatcher:
    storage = MemoryStorage()
    # TODO: Добавить redis
    dispatcher = Dispatcher(storage=storage)
    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)
    include_routers(dispatcher)
    setup_dialogs(dispatcher)

    dispatcher.errors.register(
        on_unknown_intent,
        ExceptionTypeFilter(UnknownIntent),
    )

    return dispatcher


async def main():
    logger.add(BASE_DIR / "logs" / "telegram_bot" / "bot.log", rotation="100MB", compression="zip")

    bot_token = TELEGRAM_BOT_TOKEN
    bot: Bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode='HTML'))

    dispatcher = setup_dispatcher()

    try:
        await dispatcher.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()

async def on_unknown_intent(event: ErrorEvent, dialog_manager: DialogManager):
    # Example of handling UnknownIntent Error and starting new dialog.
    logger.error(f"Restarting dialog: {event.exception}")
    if event.update.callback_query:
        await event.update.callback_query.answer(
            "Бот перезапущен, ввиду технической неполатки.\n"
            "Возврат в главное меню...",
        )
        if event.update.callback_query.message:
            try:
                await event.update.callback_query.message.delete()
            except TelegramBadRequest:
                pass  # whatever
    elif event.update.message:
        await event.update.message.answer(
            "Бот перезапущен, ввиду технической неполатки.\n"
            "Возврат в главное меню...",
            reply_markup=ReplyKeyboardRemove(),
        )
    from aiogram_dialog import StartMode
    from aiogram_dialog import ShowMode
    await dialog_manager.start(
        states.Main.MAIN,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Работа программы принудительно завершена")
