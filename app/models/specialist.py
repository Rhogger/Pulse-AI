from tortoise.models import Model
from tortoise import fields

class Specialist(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    contact_number = fields.CharField(max_length=16)

    def __str__(self):
        return self.name
