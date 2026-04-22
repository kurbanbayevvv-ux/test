from aiogram import Router, types, F

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.postgres import setPage, getPage, get_card, get_card_owner, get_all_cards, card_to_card

router = Router()

@router.message(F.text == 'Otkazma')
async def otkazma_handler(message: types.Message):
    keyb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Karta raqam", callback_data="with_card_number")
            ],
            [
                InlineKeyboardButton(text="Chat ID", callback_data="with_chat_id")
            ]
        ]
    )
    await message.answer("O'tkazma usulini tanlang:", reply_markup=keyb)

@router.callback_query(F.data == 'with_card_number')
async def with_card_number_query_handler(callback: types.CallbackQuery):
    await callback.message.answer("Karta raqamini yuboring:")
    setPage(callback.message.chat.id, 'with_card_number')

@router.callback_query(F.data == 'with_chat_id')
async def with_chat_id_query_handler(callback: types.CallbackQuery):
    await callback.message.answer("Chat ID ni yuboring:")
    setPage(callback.message.chat.id, 'with_chat_id_awaiting')

@router.message(lambda message: getPage(message.chat.id) == 'with_chat_id_awaiting')
async def with_chat_id_message_handler(message: types.Message):
    chat_id = message.text
    await message.answer("Summa kiriting:")
    setPage(message.chat.id, f"with_chat_id_{chat_id}")

@router.message(lambda message: getPage(message.chat.id).startswith('with_chat_id_'))
async def with_chat_id_summa_handler(message: types.Message):
    page = getPage(message.chat.id).split('_')
    cards = get_all_cards(page[3])
    inline_keyboard = []
    for card in cards:
        inline_keyboard.append([InlineKeyboardButton(text=str(card[0]), callback_data=f"chat_id_summa_{card[0]}")])
    card_keyboard = InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )
    page = getPage(message.chat.id)
    setPage(message.chat.id, page + f"_{message.text}")
    await message.answer("Qabul qiluvchi kartasi tanlang:", reply_markup=card_keyboard)

@router.callback_query(F.data.startswith('chat_id_summa_'))
async def sdkjfchbkdsj(callback: types.CallbackQuery):
    cards = get_all_cards(callback.message.chat.id)
    inline_keyboard = []
    for card in cards:
        inline_keyboard.append([InlineKeyboardButton(text=str(card[0]), callback_data=f"yuboruvchi_karta_{card[0]}")])
    card_keyboard = InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )
    page = getPage(callback.message.chat.id)
    setPage(callback.message.chat.id, f"summa_{callback.data.split('_')[3]}_{page.split('_')[4]}")
    await callback.message.edit_text("Qaysi kartangizdan yuborasiz:", reply_markup=card_keyboard)

@router.callback_query(F.data.startswith('yuboruvchi_karta_'))
async def yuboruvchi_karta_query_handler(callback: types.CallbackQuery):
    yuboruvchi = callback.data.replace('yuboruvchi_karta_', '')
    page = getPage(callback.message.chat.id).split('_')
    oluvchi = page[1]
    summa = page[2]
    card_to_card(yuboruvchi, oluvchi, summa)
    response_text = (f"Muvaffaqiyatli bajarildi:\n\n"
                     f"Card: {oluvchi}\n"
                     f"O'tkazilgan summa: {summa}\n")
    await callback.message.edit_text(response_text)

@router.message(lambda message: getPage(message.chat.id) == 'with_card_number')
async def with_card_number_page_handler(message: types.Message):
    card = get_card(message.text)
    card_own = get_card_owner(message.text)
    response_text = (f"Owner: {card_own}\n"
                     f"Card: {card[0]}\n\n"
                     f"Summani kiriting:")
    setPage(message.chat.id, f"summa_{card[0]}")
    await message.answer(response_text)

@router.message(lambda message: getPage(message.chat.id).startswith('summa_'))
async def summa_handler(message: types.Message):
    cards = get_all_cards(message.chat.id)
    inline_keyboard = []
    for card in cards:
        inline_keyboard.append([InlineKeyboardButton(text=str(card[0]), callback_data=f"yuboruvchi_karta_{card[0]}")])
    card_keyboard = InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )
    page = getPage(message.chat.id)
    setPage(message.chat.id, page + f"_{message.text}")
    await message.answer("Tanlang", reply_markup=card_keyboard)
