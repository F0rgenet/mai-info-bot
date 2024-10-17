from aiogram import MagicFilter
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.common.when import Predicate
from aiogram_dialog.widgets.kbd import Button, Back, Cancel
from aiogram_dialog.widgets.text import Const, Format

class BackButton(Back):
    def __init__(self, button_id: str = "__back__", on_click: (CallbackQuery, Button, DialogManager) = None,
                 show_mode: ShowMode | None = None, when: str | MagicFilter | Predicate | None = None):
        default_text = "◀️ Назад"
        super().__init__(Const(default_text), button_id, on_click, show_mode, when)

class CancelButton(Cancel):
    def __init__(self, button_id: str = "__back__", on_click: (CallbackQuery, Button, DialogManager) = None,
                 show_mode: ShowMode | None = None, when: str | MagicFilter | Predicate | None = None):
        default_text = "◀️ Назад"
        super().__init__(Const(default_text), button_id, on_click, show_mode, when)