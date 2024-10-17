from aiogram import F, Router
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode

from src.dialogs.states import Main


router = Router()


@router.message(F.text == "/start")
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        Main.MAIN,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND
    )

