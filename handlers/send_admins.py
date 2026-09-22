from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.application import ApplicationDecision
from config import ADMINS
from enums.actions import Actions
from enums.statuses import Statuses
from storage import APPLICATIONS_MESSAGES


async def send_admins(bot, data: dict, user_id: int):
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="✅ Принять",
            callback_data=ApplicationDecision(action=Actions.ACCEPT, user_id=user_id).pack()
        ),
        InlineKeyboardButton(
            text="❌ Отклонить",
            callback_data=ApplicationDecision(action=Actions.REJECT, user_id=user_id).pack()
        )
    )

    builder.adjust(2)

    text = (
        f"Новая анкета на вступление\n\n"
        f"Юз: @{data.get("username")}\n"
        f"Роль: {data.get("role")}\n"
        f"День рождения: {data.get("birthday")}\n\n"
        f"Статус: {Statuses.PENDING}"
    )

    APPLICATIONS_MESSAGES[user_id] = {}

    for admin_id in ADMINS:
        try:
            msg = await bot.send_message(
                chat_id=admin_id,
                text=text,
                reply_markup=builder.as_markup()
            )

            APPLICATIONS_MESSAGES[user_id][admin_id] = msg.message_id
        except:
            pass