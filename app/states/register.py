from aiogram.fsm.state import State, StatesGroup
from aiogram import Router
router = Router()

class Register(StatesGroup):
    name = State()
    phone = State()