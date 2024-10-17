from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start, Row
from aiogram_dialog.widgets.text import Const

from telegram_bot.dialogs.states import Schedule
from telegram_bot.keyboards.buttons import CancelButton


SCHEDULE = {
}


dialog = Dialog(
    Window(
        Const(
            "Выбери формат расписания:",
        ),
        Row(
            Start(
                Const("По дням"),
                id="daily_schedule",
                state=Schedule.DAY
          ),
            Start(
                Const("По неделям"),
                id="weekly_schedule",
                state=Schedule.WEEK
          ),
        ),
        CancelButton(),
        state=Schedule.MAIN
    ),
    Window(
        Const("DAY"),
        CancelButton(),
        state=Schedule.DAY,
    ),
    Window(
        Const("WEEK"),
        CancelButton(),
        state=Schedule.WEEK,
    )
)
