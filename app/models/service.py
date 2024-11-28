from tortoise import Model
from tortoise import fields


class Service(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    specialists = fields.ManyToManyField(
        "models.Specialist", related_name="services", through="service_specialist"
    )
    time_slots = fields.IntField(default=1)

    def __str__(self):
        return self.name

    @property
    def duration_minutes(self):
        """
        Calcula a duração total do serviço em minutos.
        """
        return self.time_slots * 30
