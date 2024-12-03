from fastapi import APIRouter, HTTPException
from app.models.specialist import Specialist
from app.services.specialist_service import (
    get_all_specialists,
    get_specialist_by_id,
    create_specialist,
    update_specialist,
    delete_specialist,
    get_specialist_by_name,
    search_specialists_by_name,
)
from pydantic import BaseModel
from typing import List

router = APIRouter()


class SpecialistIn(BaseModel):
    name: str
    contact_number: str


class SpecialistOut(SpecialistIn):
    id: int

    class Config:
        orm_mode = True


@router.get("/", response_model=List[SpecialistOut])
async def list_specialists():
    return await get_all_specialists()


@router.get("/{specialist_id}", response_model=SpecialistOut)
async def retrieve_specialist(specialist_id: int):
    specialist = await get_specialist_by_id(specialist_id)
    if not specialist:
        raise HTTPException(status_code=404, detail="Specialist not found")
    return specialist


@router.post("/", response_model=SpecialistOut)
async def add_specialist(specialist: SpecialistIn):
    return await create_specialist(specialist.dict())


@router.put("/{specialist_id}", response_model=SpecialistOut)
async def modify_specialist(specialist_id: int, specialist: SpecialistIn):
    updated_specialist = await update_specialist(specialist_id, specialist.dict())
    if not updated_specialist:
        raise HTTPException(status_code=404, detail="Specialist not found")
    return updated_specialist


@router.delete("/{specialist_id}")
async def remove_specialist(specialist_id: int):
    success = await delete_specialist(specialist_id)
    if not success:
        raise HTTPException(status_code=404, detail="Specialist not found")
    return {"detail": "Specialist deleted successfully"}


@router.get("/by-name/{name}", response_model=SpecialistOut)
async def get_specialist_by_name(name: str):
    """Busca um especialista específico pelo nome"""
    specialist = await get_specialist_by_name(name)
    if not specialist:
        raise HTTPException(
            status_code=404,
            detail="Especialista não encontrado"
        )
    return specialist


@router.get("/search/{name}", response_model=List[SpecialistOut])
async def search_specialists_by_name(name: str):
    """Busca especialistas pelo nome"""
    specialists = await search_specialists_by_name(name)
    if not specialists:
        raise HTTPException(
            status_code=404,
            detail="Nenhum especialista encontrado com este nome"
        )
    return specialists
