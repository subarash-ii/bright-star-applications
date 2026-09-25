import html
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.application import ApplicationDecision
from config import ADMINS
from enums.actions import Actions
from enums.statuses import Statuses
from storage import APPLICATIONS_MESSAGES, save_applications


async def send_admins(bot, data: dict):
    user_id = data.get("tg_id")
    username = data.get("tg_username")

    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="✅ Принять",
            callback_data=ApplicationDecision(action=Actions.ACCEPT, user_id=user_id, username=username).pack()
        ),
        InlineKeyboardButton(
            text="❌ Отклонить",
            callback_data=ApplicationDecision(action=Actions.REJECT, user_id=user_id, username=username).pack()
        ),
        InlineKeyboardButton(
            text="🚫 Заблокировать",
            callback_data=ApplicationDecision(action=Actions.BLOCK, user_id=user_id, username=username).pack()
        )
    )

    builder.adjust(2)

    username_val = html.escape(str(data.get("username", "")))
    role_val = html.escape(str(data.get("role", "")))
    birthday_val = html.escape(str(data.get("birthday", "")))

    text = (
        f"📥 <b>Новая анкета на вступление</b>\n\n"
        f"👤 <b>Юзернейм:</b> @{username_val}\n"
        f"🎭 <b>Роль:</b> {role_val}\n"
        f"🎂 <b>Дата рождения:</b> {birthday_val}\n"
        f"📌 <b>Статус:</b> {Statuses.PENDING}"
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
        except Exception:
            pass

    save_applications()