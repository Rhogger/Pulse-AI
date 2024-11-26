from datetime import time
from fastapi import HTTPException
from app.models.schedule import Schedule
from tortoise.exceptions import DoesNotExist

from app.models.service import Service
from app.models.specialist import Specialist

async def get_all_schedules():
    """Retorna todas as agendas."""
    return await Schedule.all()

async def get_schedule_by_id(schedule_id: int):
    """Retorna uma agenda pelo ID."""
    try:
        return await Schedule.get(id=schedule_id)
    except DoesNotExist:
        return None
    
async def get_schedules_by_specialist(specialist_id: int):
    """Retorna todos os agendamentos de um especialista específico."""
    try:
        specialist = await Specialist.get(id=specialist_id)
        schedules = await Schedule.filter(specialist=specialist)
        return schedules
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail=f"Especialista com ID {specialist_id} não encontrado"
        )

async def get_schedules_by_service(service_id: int):
    """Retorna todos os agendamentos de um serviço específico."""
    try:
        service = await Service.get(id=service_id)
        schedules = await Schedule.filter(service=service)
        return schedules
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail=f"Serviço com ID {service_id} não encontrado"
        )

async def create_schedule(data: dict):
    """Cria uma nova agenda."""
    try:
        specialist = await Specialist.get(id=data['specialist_id'])
        service = await Service.get(id=data['service_id'])

        if service.specialist_id != specialist.id:
            raise HTTPException(
                status_code=422,
                detail="Este serviço não pertence ao especialista selecionado"
            )

        schedule = await Schedule.create(
            specialist=specialist,
            service=service,
            start_time=data['start_time']
        )

        schedule.end_time = await schedule.calculate_end_time()
        await schedule.save()

        return schedule

    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Especialista ou Serviço não encontrado"
        )
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Erro ao criar agendamento: {str(e)}"
        )

async def update_schedule(schedule_id: int, data: dict):
    """Atualiza uma agenda existente."""
    schedule = await Schedule.get_or_none(id=schedule_id)
    if schedule:
        if 'start_time' in data:
            schedule.start_time = data['start_time']
            schedule.end_time = await schedule.calculate_end_time()

        if 'service_id' in data:
            service = await Service.get(id=data['service_id'])
            schedule.service = service

        if 'specialist_id' in data:
            specialist = await Specialist.get(id=data['specialist_id'])
            schedule.specialist = specialist

        await schedule.save()
    return schedule


async def delete_schedule(schedule_id: int):
    """Deleta uma agenda pelo ID."""
    schedule = await Schedule.get_or_none(id=schedule_id)
    if schedule:
        await schedule.delete()
        return True
    return False