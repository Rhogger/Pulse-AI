from fastapi import APIRouter, HTTPException
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
    specialist_id: int
    duration_hours: int
    duration_minutes: int

class ServiceOut(BaseModel):
    id: int
    name: str
    specialist_id: int
    duration_hours: int
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
    return await create_service(service.dict())

@router.put("/{service_id}", response_model=ServiceOut)
async def modify_service(service_id: int, service: ServiceIn):
    updated_service = await update_service(service_id, service.dict())
    if not updated_service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return updated_service

@router.delete("/{service_id}")
async def remove_service(service_id: int):
    success = await delete_service(service_id)
    if not success:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return {"detail": "Serviço deletado com sucesso"}