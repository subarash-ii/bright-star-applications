from enum import StrEnum

class Statuses(StrEnum):
    PENDING = "⏳ На рассмотрении"
    ACCEPTED = "✅ Принято"
    REJECTED = "❌ Отклонено"
    BLOCKED = "🚫 Заблокирован"