from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from enums.callback_data import CallbackData
from handlers.form import Form

router = Router()


@router.message(Command("start"))
async def command_start_handler(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Заполнить анкету",
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

    await state.set_state(Form.username)

    await callback.message.answer("Введите свой юз (@ необязательна)")