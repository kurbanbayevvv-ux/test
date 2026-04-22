from aiogram import Router, types
from aiogram.filters import CommandStart

from app.database.postgres import Register, setPage

from app.keyboards.main_keyboard import main_keyboard

router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message):
    Register(message.chat.id, message.chat.first_name)
    setPage(message.chat.id, 'main')
    await message.answer(
        'Assalomu alaykum! Botga xush kelibsiz!',
        reply_markup=main_keyboard
    )