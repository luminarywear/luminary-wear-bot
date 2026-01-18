# states.py
from aiogram.dispatcher.filters.state import State, StatesGroup

class Order(StatesGroup):
    model = State()
    size = State()
    city = State()
    name = State()
    contact = State()
    comment = State()
