from aiogram.fsm.state import StatesGroup, State

class CardState(StatesGroup):
    GoodCard = State()


class RolePlayState(StatesGroup):
    Preparation = State()
    RolePlay = State()
    ResultsEvaluation = State()