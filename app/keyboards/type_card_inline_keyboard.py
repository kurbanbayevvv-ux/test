from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

type_card_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Visa", callback_data='type_card_visa')],
        [InlineKeyboardButton(text="UzCard", callback_data='type_card_uzcard')],
        [InlineKeyboardButton(text="Humo", callback_data='type_card_humo')],
    ]
)