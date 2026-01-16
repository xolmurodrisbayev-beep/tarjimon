from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

lang_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="uz Uzb", callback_data="uz")
        ],
        [
            InlineKeyboardButton(text="ru Rus", callback_data="ru")
        ],
        [
            InlineKeyboardButton(text="us Eng", callback_data="en")
        ]
    ]
)