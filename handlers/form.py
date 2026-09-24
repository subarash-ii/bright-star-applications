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

    await message.answer("Введите роль")


@router.message(Form.role)
async def process_role(message: Message, state: FSMContext):
    await state.update_data(role=message.text.title())
    await state.set_state(Form.birthday)

    await message.answer("Введите дату своего дня рожения в формате дд.мм.гггг")


@router.message(Form.birthday)
async def process_birthday(message: Message, state: FSMContext):
    if not is_valid_date(message.text):
        await message.answer("Введённая вами дата не соотвествует формату. Попробуйте ещё раз")
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

    text = (
        f"Проверьте правильно ли вы заполнили анкету\n\n"
        f"Юз: @{data.get("username")}\n"
        f"Роль: {data.get("role")}\n"
        f"День рождения: {data.get("birthday")}"
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

    await callback.message.answer("Ваша анкета была отправлена админам на рассмотрение")

    await send_admins(callback.bot, data)


@router.callback_query(F.data == CallbackData.REWRITE_PRESSED)
async def send_admins_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

    await state.clear()
    global _final_message
    _final_message = None

    await state.set_state(Form.username)

    await callback.message.answer("Введите свой юз (@ необязательна)")


@router.callback_query(F.data == CallbackData.CANCEL_PRESSED)
async def cancel_send_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

    await state.clear()
    global _final_message
    _final_message = None

    await callback.message.answer("Вы отменили отправку анкеты.")