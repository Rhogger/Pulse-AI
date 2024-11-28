from fastapi import HTTPException
from app.models.service import Service
from tortoise.exceptions import DoesNotExist
from typing import List

from app.models.specialist import Specialist


async def get_all_services():
    """Retorna todos os serviços."""
    return await Service.all().prefetch_related("specialists")


async def get_service_by_id(service_id: int):
    """Retorna um serviço pelo ID."""
    try:
        return await Service.get(id=service_id).prefetch_related("specialists")
    except DoesNotExist:
        return None


async def get_services_by_specialist(specialist_id: int):
    """Retorna todos os serviços de um especialista específico."""
    try:
        specialist = await Specialist.get(id=specialist_id)
        return await Service.filter(specialists=specialist).prefetch_related("specialists")
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail=f"Especialista com ID {specialist_id} não encontrado"
        )


async def create_service(service_data: dict, specialist_ids: List[int]):
    if service_data.get('time_slots', 0) <= 0:
        raise ValueError("O número de slots de tempo deve ser maior que zero")

    service = await Service.create(**service_data)
    specialists = await Specialist.filter(id__in=specialist_ids)
    await service.specialists.add(*specialists)
    return await Service.get(id=service.id).prefetch_related("specialists")


async def update_service(service_id: int, service_data: dict, specialist_ids: List[int]):
    service = await Service.get_or_none(id=service_id)
    if not service:
        return None

    await service.update_from_dict(service_data)
    await service.save()

    # Atualiza os especialistas
    await service.specialists.clear()
    specialists = await Specialist.filter(id__in=specialist_ids)
    await service.specialists.add(*specialists)

    return await Service.get(id=service.id).prefetch_related("specialists")


async def delete_service(service_id: int):
    """Deleta um serviço pelo ID."""
    service = await Service.get_or_none(id=service_id)
    if service:
        await service.delete()
        return True
    return False
