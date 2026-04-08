from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard_phone_number = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Raqam yuborish", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)