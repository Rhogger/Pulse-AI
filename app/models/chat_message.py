from tortoise import Model, fields


class ChatMessage(Model):
    id = fields.IntField(pk=True)
    session = fields.ForeignKeyField(
        'models.ChatSession', related_name='messages')
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "chat_messages"
