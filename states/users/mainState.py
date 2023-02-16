from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStates(StatesGroup):
    AddToken = State()
    User_id = State()

    Newsletters = State()
    BlockedUser = State()

    AddWelcomeTxt = State()