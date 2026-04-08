from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from database.postgres import addUserInfo, user
from states.register import Register
from keyboard.keyboard import keyboard_phone_number

router = Router()



@router.message(CommandStart())
async def reg_command(message: types.Message, state: FSMContext):
    chatId = message.chat.id
    firstName = message.chat.first_name

    if user(chatId):
        await message.answer("Sizning ma'lumotlaringiz oldin saqlangan.")
        return

    await message.answer(f"Salom {firstName}")

    await message.answer(
        "Telefon raqamingizni yuboring:",
        reply_markup=keyboard_phone_number
    )

    await state.set_state(Register.phone)



@router.message(Register.phone)
async def get_phone(message: types.Message, state: FSMContext):

    if not message.contact:
        await message.answer("Raqamingizni yuboring tugma orqali")
        return

    phone = message.contact.phone_number
    await state.update_data(phone=phone)

    await message.answer("Ism kiriting:")
    await state.set_state(Register.name)



@router.message(Register.name)
async def get_name(message: types.Message, state: FSMContext):
    data = await state.update_data(name=message.text)

    name = data["name"]
    phone = data["phone"]
    chatId = message.chat.id

    addUserInfo(chatId, name, phone)

    await message.answer("Ma’lumotlaringiz muvaffaqiyatli saqlandi! ✅")

    await state.clear()