from aiogram.fsm.state import State, StatesGroup


class RewardStates(StatesGroup):
    write_reward = State()
    write_address = State()
