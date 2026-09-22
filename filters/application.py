from aiogram.filters.callback_data import CallbackData

from enums.actions import Actions

class ApplicationDecision(CallbackData, prefix="app"):
    action: Actions
    user_id: int