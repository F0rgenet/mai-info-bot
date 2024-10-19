from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, ListGroup
from aiogram_dialog.widgets.text import Const, Format
from loguru import logger
from magic_filter import MagicFilter

from telegram_bot.dialogs import states
from telegram_bot.dialogs.states import Schedule
from telegram_bot.keyboards.buttons import CancelButton
from telegram_bot.middlewares import FastAPIMiddleware


async def groups_getter(dialog_manager: DialogManager, **kwargs):
    api_middleware: FastAPIMiddleware = dialog_manager.middleware_data.get("api_middleware")

    response = await api_middleware.make_api_request("groups/all", method="GET")

    return {
        "groups": response["groups"],
    }


async def on_group_press(callback: CallbackQuery, button: Button, manager: DialogManager):
    group = button.widget_id
    await callback.answer(group)


async def group_choice(message: Message, message_input: MessageInput, dialog_manager: DialogManager, schedule_dialog=None):
    groups = await groups_getter(dialog_manager)
    logger.info(groups)
    group_names = [group["name"] for group in groups["groups"]]
    user_input_group = message.text
    if user_input_group in group_names:
        await dialog_manager.start(state=Schedule.MAIN)
    else:
        api_middleware: FastAPIMiddleware = dialog_manager.middleware_data.get("api_middleware")
        response = await api_middleware.make_api_request(f"groups/closest/{user_input_group}", method="GET")

        dialog_manager.dialog_data["correct_group"] = response
        await dialog_manager.switch_to(states.GroupChoice.CONFIRM_MISSPELLED_GROUP)

dialog = Dialog(
    Window(
        Const(
            "Нужно выбрать твою группу"
            ),
        MessageInput(group_choice),
        Format("Groups: {groups}"),
        ListGroup(
            Button(
                Format("{item[name]}"),
                id="group_button",
                on_click=on_group_press
            ),
            id="group_buttons",
            item_id_getter=lambda item: item["id"],
            items="groups",
        ),
        CancelButton(),

        getter=groups_getter,
        state=states.GroupChoice.MAIN
    ),
    Window(
        Format("{dialog_data[correct_group]}"),
        Const("Это ваша группа?"),
        Button(
            Const("Да"),
            id="answer_yes_button",
        ),
        Button(
            Const("Нет"),
            id="answer_no_button",
        ),
        state=states.GroupChoice.CONFIRM_MISSPELLED_GROUP
    )
)

