from aiogram_dialog import Dialog, LaunchMode, Window, DialogManager
from aiogram_dialog.widgets.kbd import Start, SwitchTo, Row
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const

from telegram_bot.dialogs import states
from telegram_bot.keyboards.buttons import CancelButton

dialog = Dialog(
    Window(
        StaticMedia(
            url="https://steamuserimages-a.akamaihd.net/ugc/1834658759566815787/659E58F605BD85CD554374B6A66C035A322BAB73/?imw=512&amp;imh=287&amp;ima=fit&amp;impolicy=Letterbox&amp;imcolor=%23000000&amp;letterbox=true"
        ),
        Const("Этот бот умеет импортировать расписание в любой календарь нах"),
        CancelButton(),
        state=states.Guide.MAIN
    )
)
