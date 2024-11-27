from app.models.customer import Customer
from tortoise.exceptions import DoesNotExist


async def get_all_customers(contact_number: str | None = None):
    """Retorna todos os clientes, opcionalmente filtrados por número de contato."""
    if contact_number:
        return await Customer.filter(contact_number=contact_number)
    return await Customer.all()


async def get_customer_by_id(customer_id: int):
    """Retorna um cliente pelo ID."""
    try:
        return await Customer.get(id=customer_id)
    except DoesNotExist:
        return None


async def create_customer(data: dict):
    """Cria um novo cliente."""
    return await Customer.create(**data)


async def update_customer(customer_id: int, data: dict):
    """Atualiza um cliente existente."""
    customer = await Customer.get_or_none(id=customer_id)
    if customer:
        await customer.update_from_dict(data)
        await customer.save()
    return customer


async def delete_customer(customer_id: int):
    """Deleta um cliente pelo ID."""
    customer = await Customer.get_or_none(id=customer_id)
    if customer:
        await customer.delete()
        return True
    return False
