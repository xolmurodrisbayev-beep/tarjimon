import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from gtts import gTTS
from googletrans import Translator

from inline import make_lang_keyboard, make_del_lang_keyboard, admin_kb

logging.basicConfig(level=logging.INFO)

TOKEN = "8359480287:AAFCdEX3yE4JAVpRv8UKx9C6Pn0ODQBAC5k"
ADMIN_ID = 6586504067

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

translator = Translator()

# ======================
# FSM
# ======================
class AddLang(StatesGroup):
    name = State()
    code = State()

# ======================
# DATA
# ======================
user_texts = {}
users = set()

# BOSHLANG‘ICH TILLAR
languages = {
    "🇬🇧 English": "en",
    "🇷🇺 Русский": "ru",
    "🇺🇿 Uzbek": "uz"
}

# ======================
# /start
# ======================
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    users.add(message.from_user.id)
    await message.answer(f"Salom, {message.from_user.full_name}! 🌐\nTarjima qilmoqchi bo‘lgan matnni yuboring.")

# ======================
# /admin
# ======================
@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer("👨‍💻 Admin panel", reply_markup=admin_kb)

# ======================
# ADMIN → ADD LANG
# ======================
@dp.callback_query(F.data == "admin_add_lang")
async def admin_add_lang(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        return
    await callback.message.answer("Til nomini kiriting (masalan: 🇫🇷 French)")
    await state.set_state(AddLang.name)
    await callback.answer()

@dp.message(AddLang.name)
async def admin_lang_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Til kodini kiriting (masalan: fr)")
    await state.set_state(AddLang.code)

@dp.message(AddLang.code)
async def admin_lang_code(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data["name"]
    code = message.text.lower()

    languages[name] = code
    await state.clear()

    await message.answer(f"✅ Yangi til qo‘shildi: {name} ({code})")

# ======================
# ADMIN → DELETE LANG
# ======================
@dp.callback_query(F.data == "admin_del_lang")
async def admin_del_lang(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return
    await callback.message.answer("O‘chirish uchun tilni tanlang:", reply_markup=make_del_lang_keyboard(languages))
    await callback.answer()

@dp.callback_query(F.data.startswith("del_"))
async def delete_lang(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return
    code_to_del = callback.data.replace("del_", "")
    name_to_del = next((name for name, code in languages.items() if code == code_to_del), None)
    if name_to_del:
        languages.pop(name_to_del)
        await callback.message.answer(f"❌ Til o‘chirildi: {name_to_del}")
    await callback.answer()

# ======================
# USER TEXT
# ======================
@dp.message(F.text)
async def get_text(message: types.Message):
    user_texts[message.from_user.id] = message.text
    await message.answer(
        "🌐 Tilni tanlang:",
        reply_markup=make_lang_keyboard(languages)
    )

# ======================
# TRANSLATE
# ======================
@dp.callback_query(F.data.startswith("lang_"))
async def translate(callback: types.CallbackQuery):
    await callback.answer()

    lang = callback.data.replace("lang_", "")
    text = user_texts.get(callback.from_user.id)

    if not text:
        await callback.message.answer("Avval matn yuboring")
        return

    try:
        # ASYNC translate
        result = await translator.translate(text, dest=lang)
        translated = result.text
    except Exception:
        await callback.message.answer(f"Tarjima qilishda xatolik: {lang}")
        return

    try:
        filename = f"{callback.from_user.id}.mp3"
        # gTTS faqat qo‘llab-quvvatlanadigan tillarda ovoz beradi
        tts_lang = lang if lang in ["en", "ru", "fr", "es", "de"] else "en"
        gTTS(text=translated, lang=tts_lang).save(filename)
        await callback.message.answer_voice(
            voice=FSInputFile(filename),
            caption=translated
        )
        os.remove(filename)
    except Exception:
        await callback.message.answer(translated)

# ======================
# ADMIN STATS
# ======================
@dp.callback_query(F.data == "admin_stats")
async def admin_stats(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return
    await callback.message.answer(f"👥 Foydalanuvchilar: {len(users)}")
    await callback.answer()

# ======================
# MAIN
# ======================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
