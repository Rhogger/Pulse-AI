from datetime import timedelta
from tortoise import Model, fields

class Schedule(Model):
    id = fields.IntField(pk=True)
    specialist = fields.ForeignKeyField(
        "models.Specialist", related_name="schedules"
    )
    service = fields.ForeignKeyField(
        "models.Service", related_name="schedules"
    )
    start_time = fields.DatetimeField()
    end_time = fields.DatetimeField(null=True)

    def __str__(self):
        return f"{self.specialist.name} - {self.service.name} ({self.start_time})"

    async def calculate_end_time(self):
        """Calcula o horário de término baseado na duração do serviço"""
        service = await self.service
        duration_minutes = service.total_duration_minutes

        start_datetime = self.start_time
        end_datetime = start_datetime + timedelta(minutes=duration_minutes)

        return end_datetime
