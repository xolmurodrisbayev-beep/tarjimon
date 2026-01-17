# inline.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Dict

def make_lang_keyboard(languages: Dict[str, str], row_length: int = 3) -> InlineKeyboardMarkup:
    """
    Foydalanuvchi uchun til tanlash inline tugmalari.
    3 ta yonma-yon, qolganlari pastga tushadi.
    """
    rows = []
    row = []

    for name, code in languages.items():
        row.append(InlineKeyboardButton(text=name, callback_data=f"lang_{code}"))
        if len(row) == row_length:
            rows.append(row)
            row = []

    if row:
        rows.append(row)

    # Orqaga tugmasi
    rows.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="back")])

    return InlineKeyboardMarkup(inline_keyboard=rows)


def make_del_lang_keyboard(languages: Dict[str, str], row_length: int = 3) -> InlineKeyboardMarkup:
    """
    Admin uchun til o'chirish tugmalari.
    3 ta yonma-yon, qolganlari pastga tushadi.
    """
    rows = []
    row = []

    for name, code in languages.items():
        row.append(InlineKeyboardButton(text=name, callback_data=f"del_{code}"))
        if len(row) == row_length:
            rows.append(row)
            row = []

    if row:
        rows.append(row)

    # Orqaga tugmasi
    rows.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="back")])

    return InlineKeyboardMarkup(inline_keyboard=rows)


def make_admin_keyboard() -> InlineKeyboardMarkup:
    """
    Admin panelining asosiy tugmalari
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Til qo‘shish", callback_data="admin_add_lang")],
        [InlineKeyboardButton(text="➖ Til o‘chirish", callback_data="admin_del_lang")],
        [InlineKeyboardButton(text="📊 Statistika", callback_data="admin_stats")]
    ])
    return keyboard

# Global obyekti
admin_kb = make_admin_keyboard()
