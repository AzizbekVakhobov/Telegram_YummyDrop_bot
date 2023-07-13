from aiogram.dispatcher.filters.state import State, StatesGroup


class NumberState(StatesGroup):
    phone = State()


class BirthState(StatesGroup):
    birth = State()


class FullNameState(StatesGroup):
    fullname = State()


class FeedbackState(StatesGroup):
    feedback = State()
