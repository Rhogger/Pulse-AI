from tortoise import Model, fields

from app.enum.session_status import SessionStatus


class ChatSession(Model):
    id = fields.IntField(pk=True)
    contact_number = fields.CharField(max_length=20)
    status = fields.CharEnumField(SessionStatus, default=SessionStatus.IDLE)
    last_interaction = fields.DatetimeField(auto_now=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "chat_sessions"
