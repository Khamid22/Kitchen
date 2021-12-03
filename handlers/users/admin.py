from aiogram.types import Message
from states.admin import Admin
from loader import dp, Database as db


@dp.message_handler(text="☎️ Aloqa tizimi", state=Admin.menu)
async def aloqa(message: Message):
    admin = await db.admin_data(message.from_user.id)
    name = admin.get("name") or "Kiritilmagan"
    admin_id = admin.get("admin_id") or "Kiritilmagan"
    phone = admin.get("phone") or "Kiritilmagan"
    await message.answer("<b> Aloqa tizimi </b>")