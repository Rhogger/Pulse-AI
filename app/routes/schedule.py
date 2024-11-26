from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from typing import List
from datetime import datetime, time

from app.routes.service import ServiceOut
from app.services.schedule_service import create_schedule, delete_schedule, get_all_schedules, get_schedule_by_id, get_schedules_by_service, get_schedules_by_specialist, update_schedule
from app.services.service_service import get_services_by_specialist

router = APIRouter()

class ScheduleIn(BaseModel):
    specialist_id: int
    service_id: int
    start_time: datetime
            
    @validator('specialist_id')
    def validate_specialist(cls, v):
        if v <= 0:
            raise ValueError('ID do especialista deve ser maior que 0')
        return v
        
    @validator('service_id')
    def validate_service(cls, v):
        if v <= 0:
            raise ValueError('ID do serviço deve ser maior que 0')
        return v

class ScheduleOut(ScheduleIn):
    id: int
    end_time: datetime

    class Config:
        orm_mode = True

@router.get("/", response_model=List[ScheduleOut])
async def list_schedules():
    return await get_all_schedules()

@router.get("/{schedule_id}", response_model=ScheduleOut)
async def retrieve_schedule(schedule_id: int):
    schedule = await get_schedule_by_id(schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Agenda não encontrada")
    return schedule

@router.get("/specialist/{specialist_id}", response_model=List[ServiceOut])
async def list_services_by_specialist(specialist_id: int):
    """Retorna todos os serviços de um especialista específico."""
    try:
        services = await get_services_by_specialist(specialist_id)
        return services
    except HTTPException as e:
        raise e

@router.get("/by-specialist/{specialist_id}", response_model=List[ScheduleOut])
async def list_schedules_by_specialist(specialist_id: int):
    """Retorna todos os agendamentos de um especialista específico."""
    try:
        schedules = await get_schedules_by_specialist(specialist_id)
        return schedules
    except HTTPException as e:
        raise e

@router.get("/by-service/{service_id}", response_model=List[ScheduleOut])
async def list_schedules_by_service(service_id: int):
    """Retorna todos os agendamentos de um serviço específico."""
    try:
        schedules = await get_schedules_by_service(service_id)
        return schedules
    except HTTPException as e:
        raise e

@router.post("/", response_model=ScheduleOut)
async def add_schedule(schedule: ScheduleIn):
    return await create_schedule(schedule.dict())

@router.put("/{schedule_id}", response_model=ScheduleOut)
async def modify_schedule(schedule_id: int, schedule: ScheduleIn):
    updated_schedule = await update_schedule(schedule_id, schedule.dict())
    if not updated_schedule:
        raise HTTPException(status_code=404, detail="Agenda não encontrada")
    return updated_schedule

@router.delete("/{schedule_id}")
async def remove_schedule(schedule_id: int):
    success = await delete_schedule(schedule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agenda não encontrada")
    return {"detail": "Agenda deletada com sucesso"}