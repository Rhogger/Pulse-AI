from fastapi import APIRouter, HTTPException
from app.services.customer_service import (
    get_all_customers,
    get_customer_by_id,
    create_customer,
    update_customer,
    delete_customer,
)
from pydantic import BaseModel
from typing import List

router = APIRouter()


class CustomerIn(BaseModel):
    name: str
    contact_number: str


class CustomerOut(CustomerIn):
    id: int

    class Config:
        orm_mode = True


@router.get("/", response_model=List[CustomerOut])
async def list_customers(contact_number: str | None = None):
    return await get_all_customers(contact_number)


@router.get("/{customer_id}", response_model=CustomerOut)
async def retrieve_customer(customer_id: int):
    customer = await get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return customer


@router.post("/", response_model=CustomerOut)
async def add_customer(customer: CustomerIn):
    return await create_customer(customer.dict())


@router.put("/{customer_id}", response_model=CustomerOut)
async def modify_customer(customer_id: int, customer: CustomerIn):
    updated_customer = await update_customer(customer_id, customer.dict())
    if not updated_customer:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return updated_customer


@router.delete("/{customer_id}")
async def remove_customer(customer_id: int):
    success = await delete_customer(customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"detail": "Cliente deletado com sucesso"}
