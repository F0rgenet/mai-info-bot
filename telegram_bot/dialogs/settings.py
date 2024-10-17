from aiogram_dialog import Dialog, LaunchMode, Window, DialogManager
from aiogram_dialog.widgets.kbd import Start, SwitchTo, Row
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const

from telegram_bot.dialogs import states
from telegram_bot.keyboards.buttons import CancelButton

dialog = Dialog(
    Window(
        Const(
            "Settings"
        ),
        CancelButton(),
        state=states.Settings.MAIN
    )
)
