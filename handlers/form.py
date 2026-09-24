import html
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from util import remove_at, is_valid_date
from enums.callback_data import CallbackData
from handlers.send_admins import send_admins
from db.active.queries import add_active

router = Router()


class Form(StatesGroup):
    username = State()
    role = State()
    birthday = State()
    tg_username = State()
    tg_id = State()


_final_message: Message | None = None


def get_final_message():
    return _final_message


@router.message(Form.username)
async def process_username(message: Message, state: FSMContext):
    await state.update_data(tg_id=message.from_user.id)
    await state.update_data(tg_username=message.from_user.username)

    await state.update_data(username=remove_at(message.text))
    await state.set_state(Form.role)

    await message.answer(
        "🎭 <b>Укажите вашу роль:</b>"
    )


@router.message(Form.role)
async def process_role(message: Message, state: FSMContext):
    await state.update_data(role=message.text.title())
    await state.set_state(Form.birthday)

    await message.answer(
        "🎂 <b>Введите дату рождения</b> <i>(в формате ДД.ММ.ГГГГ):</i>"
    )


@router.message(Form.birthday)
async def process_birthday(message: Message, state: FSMContext):
    if not is_valid_date(message.text):
        await message.answer(
            "⚠️ <b>Некорректный формат даты</b>\n\n"
            "Пожалуйста, введите дату строго в формате <b>ДД.ММ.ГГГГ</b> (например, <code>25.12.2000</code>)."
        )
        return

    await state.update_data(birthday=message.text)

    await show_final_applications(message, state)


async def show_final_applications(message: Message, state: FSMContext):
    data = await state.get_data()

    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="✅ Отправить", callback_data=CallbackData.SEND_ADMINS_PRESSED),
        InlineKeyboardButton(text="✏️ Изменить", callback_data=CallbackData.REWRITE_PRESSED),
        InlineKeyboardButton(text="🚫 Отменить", callback_data=CallbackData.CANCEL_PRESSED)
    )

    builder.adjust(2)

    username_val = html.escape(str(data.get("username", "")))
    role_val = html.escape(str(data.get("role", "")))
    birthday_val = html.escape(str(data.get("birthday", "")))

    text = (
        f"📋 <b>Проверьте правильность заполнения анкеты:</b>\n\n"
        f"👤 <b>Юзернейм:</b> @{username_val}\n"
        f"🎭 <b>Роль:</b> {role_val}\n"
        f"🎂 <b>Дата рождения:</b> {birthday_val}\n\n"
        f"Всё верно? Нажмите кнопку <b>«Отправить»</b> для передачи анкеты администраторам."
    )

    global _final_message
    _final_message = await message.answer(text, reply_markup=builder.as_markup())


@router.callback_query(F.data == CallbackData.SEND_ADMINS_PRESSED)
async def send_admins_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    data = await state.get_data()

    await state.clear()
    global _final_message
    _final_message = None

    await add_active(data.get("tg_id"), data.get("tg_username"))

    await callback.message.answer(
        "🎉 <b>Анкета успешно отправлена!</b>\n\n"
        "Ваша заявка передана администраторам на рассмотрение. Ожидайте решения!"
    )

    await send_admins(callback.bot, data)


@router.callback_query(F.data == CallbackData.REWRITE_PRESSED)
async def rewrite_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

    await state.clear()
    global _final_message
    _final_message = None

    await state.set_state(Form.username)

    await callback.message.answer(
        "🔄 <b>Заполнение анкеты заново</b>\n\n"
        "👤 <b>Введите ваш юзернейм:</b>"
    )


@router.callback_query(F.data == CallbackData.CANCEL_PRESSED)
async def cancel_send_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

    await state.clear()
    global _final_message
    _final_message = None

    await callback.message.answer(
        "❌ <b>Заполнение анкеты отменено.</b>\n\n"
        "Если захотите заполнить заявку позже, используйте команду /start."
    )