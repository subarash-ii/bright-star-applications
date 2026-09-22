from aiogram import Router
from aiogram.types import CallbackQuery

from filters.application import ApplicationDecision
from enums.actions import Actions
from enums.statuses import Statuses
from storage import APPLICATIONS_MESSAGES, save_applications

router = Router()


@router.callback_query(ApplicationDecision.filter())
async def process_decision(callback: CallbackQuery, callback_data: ApplicationDecision):
    await callback.answer()

    target_user_id = callback_data.user_id

    if callback_data.action == Actions.ACCEPT:
        new_status = Statuses.ACCEPTED.value
        user_message = "Ваша анкета была одобрена!"
    else:
        new_status = Statuses.REJECTED.value
        user_message = "К сожалению, ваша анкета была отклонена."

    new_text = callback.message.text.replace(Statuses.PENDING.value, new_status)
    admin_messages = APPLICATIONS_MESSAGES.get(target_user_id, {})

    for admin_id, msg_id in admin_messages.items():
        try:
            await callback.bot.edit_message_text(
                chat_id=admin_id,
                message_id=msg_id,
                text=new_text,
                reply_markup=None
            )
        except Exception:
            pass

    APPLICATIONS_MESSAGES.pop(target_user_id, None)
    save_applications()

    try:
        await callback.bot.send_message(
            chat_id=target_user_id,
            text=user_message
        )
    except Exception:
        pass