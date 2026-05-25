from aiogram.fsm.state import StatesGroup, State

class GameStates(StatesGroup):
    game_in_progress = State()