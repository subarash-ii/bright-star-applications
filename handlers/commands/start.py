from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from enums.callback_data import CallbackData
from handlers.form import Form
from db.blacklist.queries import is_user_blocked
from db.active.queries import is_user_active
from handlers.form import get_final_message

router = Router()


@router.message(Command("start"))
async def command_start_handler(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="📝 Заполнить анкету",
        callback_data=CallbackData.START_PRESSED
    ))

    await message.answer(
        "*Здесь нужен текст, мол, нажмите кнопку и запоните данные",
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data == CallbackData.START_PRESSED)
async def start_button_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    is_blocked = await is_user_blocked(callback.from_user.id)

    if is_blocked:
        await callback.message.answer(
            "🚫 <b>Доступ ограничен</b>\n\n"
            "Вы были заблокированы администрацией и не можете подать анкету."
        )
        return

    is_active = await is_user_active(callback.from_user.id)

    if is_active:
        await callback.message.answer(
            "⏳ <b>Заявка уже отправлена</b>\n\n"
            "Ваша анкета находится на рассмотрении у администрации. Пожалуйста, ожидайте решения."
        )
        return

    final_message = get_final_message()

    if final_message is not None:
        await final_message.delete()

    await state.set_state(Form.username)

    await callback.message.answer(
        "👤 <b>Введите ваш юзернейм:</b>"
    )