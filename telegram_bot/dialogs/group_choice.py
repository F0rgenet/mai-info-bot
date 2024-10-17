from tokenize import group
from typing import Any

from aiogram.types import Message
from aiogram_dialog import Dialog, LaunchMode, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Start, SwitchTo, Row
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const

from telegram_bot.dialogs import states
from telegram_bot.dialogs.states import Schedule
from telegram_bot.keyboards.buttons import CancelButton

async def group_choice(message: Message, message_input: MessageInput, manager: DialogManager, schedule_dialog=None):
    groups = ['1', 'М3О-221Б-23', 'М3О-213Б-23', 'М3О-214Б-23', 'М3О-212Б-23']
    if message.text in groups:
            await manager.start(state=Schedule.MAIN)
    else:
        await message.answer("Неверная группа")

dialog = Dialog(
    Window(
        Const(
            "Нужно выбрать твою группу"
                ),
        MessageInput(group_choice),
        CancelButton(),
        state=states.GroupChoice.MAIN
))

