from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from keyboards.default.menu import sozlamalar, main_menu, back
from states.registration import new_user
from states.user import Public
from keyboards.inline.qaror import decision
from aiogram.dispatcher import FSMContext
from loader import dp, Database as db


@dp.message_handler(text="⚙️ Sozlamalar", state=new_user.bosh_menyu)
async def sozlama(message: Message):
    await message.answer(message.text, reply_markup=sozlamalar)
    await Public.sozlamalar.set()


@dp.message_handler(text="🔙 Back", state="*")
async def orqaga(message: Message):
    await message.answer("Quyidagi buyruqlardan birini tanlang", reply_markup=main_menu)
    await new_user.bosh_menyu.set()


@dp.message_handler(text="💼 Profil", state=Public.sozlamalar)
async def akkaunt(message: Message, state: FSMContext):
    data = await db.user_data(telegram_id=message.from_user.id)
    profile_id = data.get("telegram_id")
    name = data.get("full_name")
    username = data.get("username") or "No username"
    phone_number = data.get("phone_number")

    msg = f"<b>↪️ Mening profilm↩️   ID: {profile_id}</b>\n" \
          f"  ➖➖➖➖➖➖➖➖➖➖➖➖ \n"
    msg += f"Name : {name}\n"
    msg += f"Phone : {phone_number}\n"
    msg += f"Username : {username}\n"
    await message.answer(msg, reply_markup=back)
    await state.finish()


@dp.message_handler(text="🗑 Akkauntni o'chirish",state=Public.sozlamalar)
async def delete(message: Message):
    await message.answer("<b>Haqiqatan ham akkauntingizni o'chirib tashlamoqchimisiz?! </b>", reply_markup=decision())
    await Public.qaror.set()


@dp.callback_query_handler(text="yes", state=Public.qaror)
async def submit_yes(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    await call.message.delete()
    await db.delete_user(user_id)
    await call.message.answer("Akkauntingiz oʻchirildi..", reply_markup=ReplyKeyboardRemove(True))
    await call.answer(cache_time=60)
    await state.finish()


@dp.callback_query_handler(text="no", state=Public.qaror)
async def submit_no(call: CallbackQuery):
    await call.message.delete()
    await call.answer(cache_time=60)
    await call.message.answer("⚙️ Sozlamalar", reply_markup=sozlamalar)
    await Public.sozlamalar.set()


