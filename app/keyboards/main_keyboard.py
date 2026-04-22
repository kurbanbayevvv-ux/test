from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Balance')
        ],
        [
            KeyboardButton(text='Cards')
        ],
        [
            KeyboardButton(text="Otkazma")
        ]
    ],
    resize_keyboard=True
)