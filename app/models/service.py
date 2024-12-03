from tortoise import Model, fields
from tortoise.expressions import Q


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

    @classmethod
    async def get_by_name(cls, name: str):
        """
        Busca um serviço pelo nome, usando correspondência parcial case-insensitive.
        
        Args:
            name (str): Nome ou parte do nome do serviço
            
        Returns:
            Service: Primeiro serviço encontrado que corresponda ao nome
        """
        return await cls.filter(
            Q(name__icontains=name)
        ).first()

    @classmethod
    async def search_by_name(cls, name: str):
        """
        Busca todos os serviços que correspondam ao nome.
        
        Args:
            name (str): Nome ou parte do nome do serviço
            
        Returns:
            List[Service]: Lista de serviços que correspondam ao nome
        """
        return await cls.filter(
            Q(name__icontains=name)
        ).all()
