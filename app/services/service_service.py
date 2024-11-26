from fastapi import HTTPException
from app.models.service import Service
from tortoise.exceptions import DoesNotExist

from app.models.specialist import Specialist

async def get_all_services():
    """Retorna todos os serviços."""
    return await Service.all()

async def get_service_by_id(service_id: int):
    """Retorna um serviço pelo ID."""
    try:
        return await Service.get(id=service_id)
    except DoesNotExist:
        return None

async def get_services_by_specialist(specialist_id: int):
    """Retorna todos os serviços de um especialista específico."""
    try:
        specialist = await Specialist.get(id=specialist_id)
        
        services = await Service.filter(specialist_id=specialist_id)
        return services
        
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail=f"Especialista com ID {specialist_id} não encontrado"
        )

async def create_service(data: dict):
    """Cria um novo serviço."""
    try:
        specialist = await Specialist.get(id=data['specialist_id'])
        
        service = await Service.create(
            name=data['name'],
            specialist_id=data['specialist_id'],
            duration_hours=data['duration_hours'],
            duration_minutes=data['duration_minutes']
        )
        return service
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail=f"Especialista com ID {data['specialist_id']} não encontrado"
        )
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Erro ao criar serviço: {str(e)}"
        )

async def update_service(service_id: int, data: dict):
    """Atualiza um serviço existente."""
    service = await Service.get_or_none(id=service_id)
    if service:
        await service.update_from_dict(data)
        await service.save()
    return service

async def delete_service(service_id: int):
    """Deleta um serviço pelo ID."""
    service = await Service.get_or_none(id=service_id)
    if service:
        await service.delete()
        return True
    return False