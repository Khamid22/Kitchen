from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📬 Buyurtmalar"),
            KeyboardButton(text="⏰ Jarayonda")
        ],
        [
            KeyboardButton(text="🍴 Taomlar"),
            KeyboardButton(text="☎️ Aloqa tizimi")
        ]
    ], resize_keyboard=True
)