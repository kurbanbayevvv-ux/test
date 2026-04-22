from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

card_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Add Card", callback_data='add_card'),
        ],
    ]
)