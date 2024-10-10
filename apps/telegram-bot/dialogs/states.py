from aiogram.fsm.state import State, StatesGroup

class Main(StatesGroup):
    MAIN = State()

class Guide(StatesGroup):
    MAIN = State()

class GroupChoice(StatesGroup):
    MAIN = State()

class Schedule(StatesGroup):
    MAIN = State()
    DAY = State()
    WEEK = State()

class Export(StatesGroup):
    MAIN = State()

class Feedback(StatesGroup):
    MAIN = State()

class Admin_panel(StatesGroup):
    MAIN = State()