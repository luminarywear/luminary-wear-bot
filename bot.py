# bot.py
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from config import TOKEN, ADMIN_ID
from states import Order
from keyboards import models_kb

# допустимые размеры
VALID_SIZES = {"XS", "S", "M", "L", "XL"}

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands="start")
async def start(msg: types.Message):
    await msg.answer(
        "Добро пожаловать в *Luminary Wear* ✨\n"
        "Одежда про свет внутри, свободу и любовь.\n\n"
        "Выбери футболку 🤍",
        reply_markup=models_kb(),
        parse_mode="Markdown"
    )

@dp.callback_query_handler()
async def choose_model(call: types.CallbackQuery, state: FSMContext):
    # сохраняем выбранную модель
    await state.update_data(model=call.data)
    await Order.size.set()
    await call.message.answer(
        "Выбери размер: XS / S / M / L / XL"
    )

@dp.message_handler(state=Order.size)
async def get_size(msg: types.Message, state: FSMContext):
    size = msg.text.strip().upper()
    if size not in VALID_SIZES:
        await msg.answer(
            "Неверный размер. Пожалуйста, выбери один из: XS / S / M / L / XL"
        )
        return
    await state.update_data(size=size)
    await Order.city.set()
    await msg.answer("Город доставки?")

@dp.message_handler(state=Order.city)
async def get_city(msg: types.Message, state: FSMContext):
    await state.update_data(city=msg.text.strip())
    await Order.name.set()
    await msg.answer("Как тебя зовут?")

@dp.message_handler(state=Order.name)
async def get_name(msg: types.Message, state: FSMContext):
    await state.update_data(name=msg.text.strip())
    await Order.contact.set()
    await msg.answer("Контакт для связи (@username или телефон)")

@dp.message_handler(state=Order.contact)
async def get_contact(msg: types.Message, state: FSMContext):
    await state.update_data(contact=msg.text.strip())
    await Order.comment.set()
    await msg.answer(
        "Комментарий к заказу? (если нет — напиши «—»)"
    )

@dp.message_handler(state=Order.comment)
async def finish(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    comment = msg.text.strip()

    text = (
        "🧾 *НОВЫЙ ЗАКАЗ — Luminary Wear*\n\n"
        f"👕 Модель: {data['model']}\n"
        f"📏 Размер: {data['size']}\n"
        f"📍 Город: {data['city']}\n"
        f"👤 Имя: {data['name']}\n"
        f"📱 Контакт: {data['contact']}\n"
        f"💬 Комментарий: {comment}"
    )

    # пересылаем заказ тебе
    await bot.send_message(ADMIN_ID, text, parse_mode="Markdown")
    await msg.answer("Спасибо 🤍 Я передал заказ дизайнеру Luminary Wear.")
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
