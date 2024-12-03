from fastapi import HTTPException
from app.models.service import Service
from tortoise.exceptions import DoesNotExist
from typing import List, Dict, Any
from app.models.specialist import Specialist


async def get_all_services():
    """Retorna todos os serviços."""
    services = await Service.all().prefetch_related("specialists")
    return [
        {
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "duration": service.duration * 30,  # Convertendo para minutos
            "price": service.price,
            "specialists": [
                {
                    "id": specialist.id,
                    "name": specialist.name
                }
                for specialist in service.specialists
            ]
        }
        for service in services
    ]


async def get_service_by_id(service_id: int):
    """Retorna um serviço pelo ID."""
    try:
        service = await Service.get(id=service_id).prefetch_related("specialists")
        return {
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "duration": service.duration * 30,  # Convertendo para minutos
            "price": service.price,
            "specialists": [
                {
                    "id": specialist.id,
                    "name": specialist.name
                }
                for specialist in service.specialists
            ]
        }
    except DoesNotExist:
        return None


async def get_services_by_specialist(specialist_id: int):
    """Retorna todos os serviços de um especialista específico."""
    try:
        specialist = await Specialist.get(id=specialist_id)
        services = await Service.filter(specialists=specialist).prefetch_related("specialists")
        return [
            {
                "id": service.id,
                "name": service.name,
                "description": service.description,
                "duration": service.duration * 30,  # Convertendo para minutos
                "price": service.price,
                "specialists": [
                    {
                        "id": specialist.id,
                        "name": specialist.name
                    }
                    for specialist in service.specialists
                ]
            }
            for service in services
        ]
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail=f"Especialista com ID {specialist_id} não encontrado"
        )


async def create_service(service_data: Dict[str, Any]) -> Service:
    """Cria um novo serviço."""
    specialists = service_data.pop('specialist_ids', [])

    service = await Service.create(
        name=service_data['name'],
        description=service_data['description'],
        duration=service_data['duration'],
        price=service_data['price']
    )

    if specialists:
        for specialist_id in specialists:
            try:
                specialist = await Specialist.get(id=specialist_id)
                await service.specialists.add(specialist)
            except DoesNotExist:
                await service.delete()
                raise HTTPException(
                    status_code=404,
                    detail=f"Especialista com ID {specialist_id} não encontrado"
                )

    await service.fetch_related("specialists")

    return {
        "id": service.id,
        "name": service.name,
        "description": service.description,
        "duration": service.duration * 30,  # Convertendo para minutos
        "price": service.price,
        "specialists": [
            {
                "id": specialist.id,
                "name": specialist.name
            }
            for specialist in service.specialists
        ]
    }


async def update_service(service_id: int, service_data: Dict[str, Any]) -> Dict[str, Any]:
    """Atualiza um serviço existente."""
    try:
        service = await Service.get(id=service_id)

        if 'name' in service_data:
            service.name = service_data['name']
        if 'description' in service_data:
            service.description = service_data['description']
        if 'duration' in service_data:
            service.duration = service_data['duration']
        if 'price' in service_data:
            service.price = service_data['price']

        await service.save()

        if 'specialist_ids' in service_data:
            await service.specialists.clear()
            for specialist_id in service_data['specialist_ids']:
                try:
                    specialist = await Specialist.get(id=specialist_id)
                    await service.specialists.add(specialist)
                except DoesNotExist:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Especialista com ID {specialist_id} não encontrado"
                    )

        await service.fetch_related("specialists")

        return {
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "duration": service.duration * 30,  # Convertendo para minutos
            "price": service.price,
            "specialists": [
                {
                    "id": specialist.id,
                    "name": specialist.name
                }
                for specialist in service.specialists
            ]
        }

    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail=f"Serviço com ID {service_id} não encontrado"
        )


async def delete_service(service_id: int):
    """Deleta um serviço pelo ID."""
    try:
        service = await Service.get(id=service_id)
        await service.delete()
        return True
    except DoesNotExist:
        return False
