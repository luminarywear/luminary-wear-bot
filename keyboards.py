from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def models_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    models = [
        "порхаю крыльями выше облаков",
        "бесконечность любви",
        "вера",
        "люминари inside"
    ]
    for m in models:
        kb.add(InlineKeyboardButton(m, callback_data=m))
    return kb
