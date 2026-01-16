from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
from aiogram.client.default import DefaultBotProperties

import asyncio
import logging
from gtts import gTTS
from inline import lang_btn
from tarnslator import tarjimon

logging.basicConfig(level=logging.INFO)

TOKEN = "8359480287:AAFCdEX3yE4JAVpRv8UKx9C6Pn0ODQBAC5k"

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    full_name = message.from_user.full_name
    await message.answer(f"lasom <b>{full_name}</b> botga xush kelibsiz\nTarjima qilmoqchi bo'lgan matnigizni kiriting")

user_data = {

}

@dp.message(F.text)
async def get_text(message:types.Message):
    user_text = message.text
    user_data[message.from_user.id] = user_text
    await message.answer("qaysi tilga tarjima qilmoqchisiz", reply_markup=lang_btn)

@dp.callback_query()
async def get_user_lang(callback: types.CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id
    user_lang = callback.data
    user_text = user_data.get(user_id)

    if not user_text:
        await callback.message.answer("Avval matn yuboring")
        return

    tarjima_matn = await tarjimon(user_text,user_lang)

    file_name = f"voice_{user_id}.mp3"
    tts = gTTS(text=tarjima_matn, lang=user_lang)
    tts.save(file_name)

    voice = FSInputFile(file_name)
    await callback.message.answer_voice(
        voice=voice,
        caption=tarjima_matn
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())