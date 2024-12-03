from tortoise import Model, fields


class Service(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    duration = fields.IntField()
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    specialists = fields.ManyToManyField(
        'models.Specialist', related_name='services', through='service_specialist'
    )

    @property
    def total_duration_minutes(self) -> int:
        """Retorna a duração total em minutos."""
        return self.duration * 30

    class Meta:
        table = "services"

    def __str__(self):
        return self.name
