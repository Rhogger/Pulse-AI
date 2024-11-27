import os
from crewai.tools import tool
import requests

BASE_URL = os.getenv("BASE_URL")


@tool
def create_new_customer(name: str, contact_number: str) -> str:
    """Útil para criar um novo cliente no sistema. 
    Args:
        name (str): Nome completo do cliente
        contact_number (str): Número de telefone no formato (XX) XXXXX-XXXX
    Returns:
        str: Mensagem de confirmação com os dados do cliente criado
    """
    try:
        response = requests.post(
            f"{BASE_URL}/customers/",
            json={
                "name": name,
                "contact_number": contact_number
            }
        )

        if response.status_code == 200:
            customer = response.json()
            return f"Cliente criado com sucesso!\nID: {customer['id']}\nNome: {customer['name']}\nContato: {customer['contact_number']}"
        else:
            return f"Erro ao criar cliente: {response.text}"
    except Exception as e:
        return f"Erro ao criar cliente: {str(e)}"


@tool
def get_customer_by_contact(contact_number: str) -> str:
    """Útil para buscar clientes pelo número de telefone.
    Args:
        contact_number (str): Número de telefone no formato (XX) XXXXX-XXXX
    """
    try:
        response = requests.get(
            f"{BASE_URL}/customers/",
            params={"contact_number": contact_number}
        )

        if response.status_code != 200:
            return f"Erro ao buscar clientes: {response.text}"

        customers = response.json()
        if not customers:
            return "Nenhum cliente encontrado com este número"

        result = "Clientes encontrados:\n"
        for customer in customers:
            result += f"ID: {customer['id']}, Nome: {customer['name']}, Contato: {customer['contact_number']}\n"
        return result
    except Exception as e:
        return f"Erro ao buscar clientes: {str(e)}"
