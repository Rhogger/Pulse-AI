from app.models.specialist import Specialist
from tortoise.exceptions import DoesNotExist


async def get_all_specialists():
    """Retorna todos os especialistas."""
    return await Specialist.all()


async def get_specialist_by_id(specialist_id: int):
    """Retorna um especialista pelo ID."""
    try:
        return await Specialist.get(id=specialist_id)
    except DoesNotExist:
        return None


async def create_specialist(data: dict):
    """Cria um novo especialista."""
    return await Specialist.create(**data)


async def update_specialist(specialist_id: int, data: dict):
    """Atualiza um especialista existente."""
    specialist = await Specialist.get_or_none(id=specialist_id)
    if specialist:
        await specialist.update_from_dict(data)
        await specialist.save()
    return specialist


async def delete_specialist(specialist_id: int):
    """Deleta um especialista pelo ID."""
    specialist = await Specialist.get_or_none(id=specialist_id)
    if specialist:
        await specialist.delete()
        return True
    return False


async def get_specialist_by_name(name: str):
    """Retorna um especialista pelo nome."""
    try:
        return await Specialist.get_by_name(name)
    except DoesNotExist:
        return None


async def search_specialists_by_name(name: str):
    """Retorna todos os especialistas que correspondam ao nome."""
    return await Specialist.search_by_name(name)
