import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from states import Order
from keyboards import models_kb

TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = int(os.environ["ADMIN_ID"])

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
    await state.update_data(model=call.data)
    await Order.size.set()
    await call.message.answer("Выбери размер: XS / S / M / L / XL")

@dp.message_handler(state=Order.size)
async def size(msg: types.Message, state: FSMContext):
    await state.update_data(size=msg.text)
    await Order.city.set()
    await msg.answer("Город доставки?")

@dp.message_handler(state=Order.city)
async def city(msg: types.Message, state: FSMContext):
    await state.update_data(city=msg.text)
    await Order.name.set()
    await msg.answer("Как тебя зовут?")

@dp.message_handler(state=Order.name)
async def name(msg: types.Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await Order.contact.set()
    await msg.answer("Контакт для связи (@username или телефон)")

@dp.message_handler(state=Order.contact)
async def contact(msg: types.Message, state: FSMContext):
    await state.update_data(contact=msg.text)
    await Order.comment.set()
    await msg.answer("Комментарий? (если нет — напиши «—»)")

@dp.message_handler(state=Order.comment)
async def finish(msg: types.Message, state: FSMContext):
    data = await state.get_data()

    text = (
        "🧾 *НОВЫЙ ЗАКАЗ — Luminary Wear*\n\n"
        f"👕 Модель: {data['model']}\n"
        f"📏 Размер: {data['size']}\n"
        f"📍 Город: {data['city']}\n"
        f"👤 Имя: {data['name']}\n"
        f"📱 Контакт: {data['contact']}\n"
        f"💬 Комментарий: {msg.text}"
    )

    await bot.send_message(ADMIN_ID, text, parse_mode="Markdown")
    await msg.answer("Спасибо 🤍 Я передал заказ дизайнеру Luminary Wear.")
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
