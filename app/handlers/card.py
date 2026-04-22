from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.types import CallbackQuery

from database.postgres import get_all_cards, create_card, get_card

from keyboards.type_card_inline_keyboard import type_card_inline_keyboard

router = Router()

@router.message(F.text == 'Cards')
async def card_handler(message: types.Message):
    cards = get_all_cards(message.chat.id)
    inline_keyboard = []
    for card in cards:
        inline_keyboard.append([InlineKeyboardButton(text=str(card[0]), callback_data=f"card_{card[0]}")])
    inline_keyboard.append([InlineKeyboardButton(text="Add Card", callback_data='add_card')])
    card_keyboard = InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )
    await message.answer("Cards", reply_markup=card_keyboard)

@router.callback_query(F.data == 'add_card')
async def add_card_query_handler(callback: types.CallbackQuery):
    await callback.message.answer("Karta turini kiriting:", reply_markup=type_card_inline_keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith('type_card_'))
async def type_card_query_handler(callback: types.CallbackQuery):
    create_card(callback.message.chat.id, callback.data.split('_')[2])
    await callback.message.answer("Kartangiz muvaffaqiyatli yaratildi!")
    await callback.answer()

@router.callback_query(F.data.startswith('card_'))
async def card_query_handler(callback: types.CallbackQuery):
    card_number = callback.data.replace('card_', '')
    card = get_card(card_number)
    response_text = (f"💳 Card Info:\n\n"
                     f"🔢 Number: {card[0]}\n"
                     f"💰 Balance: {card[1]}\n"
                     f"🏦 Type: {card[2]}\n"
                     f"📅 Valid: {card[3]}")
    keyb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Back", callback_data='back_to_cards')]
        ]
    )
    await callback.message.edit_text(response_text, reply_markup=keyb)

@router.callback_query(F.data == 'back_to_cards')
async def card_handler(callback: types.CallbackQuery):
    cards = get_all_cards(callback.message.chat.id)
    inline_keyboard = []
    for card in cards:
        inline_keyboard.append([InlineKeyboardButton(text=str(card[0]), callback_data=f"card_{card[0]}")])
    inline_keyboard.append([InlineKeyboardButton(text="Add Card", callback_data='add_card')])
    card_keyboard = InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )
    await callback.message.edit_text("Cards", reply_markup=card_keyboard)