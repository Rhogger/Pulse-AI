from tortoise import Model
from tortoise import fields

class Service(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    specialist = fields.ForeignKeyField(
        "models.Specialist", related_name="services"
    )
    duration_hours = fields.IntField(default=0)
    duration_minutes = fields.IntField(default=0)

    def __str__(self):
        return self.name

    @property
    def total_duration_minutes(self):
        """
        Calcula a duração total do serviço em minutos.
        """
        return self.duration_hours * 60 + self.duration_minutes
