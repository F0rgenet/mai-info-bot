from aiogram.types import Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Start, Row, Back
from aiogram_dialog.widgets.text import Const, Format
from loguru import logger

from src.dialogs import states


async def get_user_name(dialog_manager: DialogManager, **kwargs):
    username = "гость"
    event = dialog_manager.event
    logger.debug(event.__class__.__name__)
    if isinstance(event, Message) and event.from_user.first_name:
        username = dialog_manager.event.from_user.first_name
    return {
        "username": username
    }



dialog = Dialog(
    Window(
        Format("Гамарджоба, {username}!"),
        Const("Я могу выполнить эти команды: \n"
              "👥 Выбрать свою группу \n"
              "❔ Как мной пользоваться? \n"
              "⚙️ Настройки бота \n"
              "📩 Экспорт в календарь \n"
              "🗓 Расписание пар"),
        Row(
            Start(
                Const("👥 Группа"),
                id="group_choice_button",
                state=states.GroupChoice.MAIN
            ),
            Start(
                Const("❔ Помощь"),
                id="guide_button",
                state=states.Guide.MAIN
            )
        ),
        Row(Start(
            Const("⚙️ Настройки"),
            id="settings_button",
            state=states.Settings.MAIN
            ),
            Start(
            Const("📩 Экспорт"),
            id="export_button",
            state=states.Export.MAIN
            )),
        Start(
            Const("🗓 Расписание"),
            id="schedule_button",
            state=states.Schedule.MAIN
        ),
        state = states.Main.MAIN,
        getter = get_user_name
    )
)