from aiogram import Router, types, F

from app.database.postgres import get_all_balance

router = Router()

@router.message(F.text == 'Balance')
async def balance_handler(message: types.Message):
    balance = get_all_balance(message.chat.id)
    await message.answer(str(balance))