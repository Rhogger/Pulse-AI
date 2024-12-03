from tortoise.models import Model
from tortoise import fields
from tortoise.expressions import Q


class Specialist(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    contact_number = fields.CharField(max_length=16)

    def __str__(self):
        return self.name

    @classmethod
    async def get_by_name(cls, name: str):
        """
        Busca um especialista pelo nome, usando correspondência parcial case-insensitive.
        
        Args:
            name (str): Nome ou parte do nome do especialista
            
        Returns:
            Specialist: Primeiro especialista encontrado que corresponda ao nome
        """
        return await cls.filter(
            Q(name__icontains=name)
        ).first()

    @classmethod
    async def search_by_name(cls, name: str):
        """
        Busca todos os especialistas que correspondam ao nome.
        
        Args:
            name (str): Nome ou parte do nome do especialista
            
        Returns:
            List[Specialist]: Lista de especialistas que correspondam ao nome
        """
        return await cls.filter(
            Q(name__icontains=name)
        ).all()
