from fastapi import APIRouter, HTTPException
from app.routes.specialist import SpecialistOut
from app.services.service_service import (
    get_all_services,
    get_service_by_id,
    create_service,
    get_services_by_specialist,
    update_service,
    delete_service,
)
from pydantic import BaseModel
from typing import List

router = APIRouter()


class ServiceIn(BaseModel):
    name: str
    specialist_ids: List[int]
    time_slots: int


class ServiceOut(BaseModel):
    id: int
    name: str
    specialists: List[SpecialistOut]
    time_slots: int
    duration_minutes: int

    class Config:
        orm_mode = True


@router.get("/", response_model=List[ServiceOut])
async def list_services():
    return await get_all_services()


@router.get("/{service_id}", response_model=ServiceOut)
async def retrieve_service(service_id: int):
    service = await get_service_by_id(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return service


@router.get("/by-specialist/{specialist_id}", response_model=List[ServiceOut])
async def list_services_by_specialist(specialist_id: int):
    """Retorna todos os serviços de um especialista específico"""
    services = await get_services_by_specialist(specialist_id)
    if not services:
        raise HTTPException(
            status_code=404,
            detail="Nenhum serviço encontrado para este especialista"
        )
    return services


@router.post("/", response_model=ServiceOut)
async def add_service(service: ServiceIn):
    service_data = service.dict()
    specialist_ids = service_data.pop('specialist_ids')
    return await create_service(service_data, specialist_ids)


@router.put("/{service_id}", response_model=ServiceOut)
async def modify_service(service_id: int, service: ServiceIn):
    service_data = service.dict()
    specialist_ids = service_data.pop('specialist_ids')
    updated_service = await update_service(service_id, service_data, specialist_ids)
    if not updated_service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return updated_service


@router.delete("/{service_id}")
async def remove_service(service_id: int):
    success = await delete_service(service_id)
    if not success:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return {"detail": "Serviço deletado com sucesso"}
