import os
from crewai.tools import tool
import requests

BASE_URL = os.getenv("BASE_URL")


@tool
def create_new_specialist(name: str, contact_number: str) -> str:
    """Útil para criar um novo especialista no sistema. 
    Args:
        name (str): Nome completo do especialista (ex: 'Dr. Ana Silva')
        contact_number (str): Número de telefone no formato (XX) XXXXX-XXXX
    Returns:
        str: Mensagem de confirmação com os dados do especialista criado
    """
    try:
        response = requests.post(
            f"{BASE_URL}/specialists/",
            json={
                "name": name,
                "contact_number": contact_number
            }
        )

        if response.status_code == 200:
            specialist = response.json()
            return f"Especialista criado com sucesso!\nID: {specialist['id']}\nNome: {specialist['name']}\nContato: {specialist['contact_number']}"
        else:
            return f"Erro ao criar especialista: {response.text}"
    except Exception as e:
        return f"Erro ao criar especialista: {str(e)}"


@tool
def list_specialists() -> str:
    """Útil para listar todos os especialistas cadastrados no sistema."""
    try:
        response = requests.get(f"{BASE_URL}/specialists/")

        if response.status_code != 200:
            return f"Erro ao listar especialistas: {response.text}"

        specialists = response.json()
        if not specialists:
            return "Nenhum especialista encontrado."

        return "\n".join([
            f"ID: {s['id']}, Nome: {s['name']}, Contato: {s['contact_number']}"
            for s in specialists
        ])
    except Exception as e:
        return f"Erro ao listar especialistas: {str(e)}"


@tool
def get_specialist(specialist_id: int) -> str:
    """Útil para buscar um especialista específico pelo ID."""
    try:
        response = requests.get(f"{BASE_URL}/specialists/{specialist_id}")

        if response.status_code == 404:
            return "Especialista não encontrado"
        elif response.status_code != 200:
            return f"Erro ao buscar especialista: {response.text}"

        specialist = response.json()
        return f"ID: {specialist['id']}, Nome: {specialist['name']}, Contato: {specialist['contact_number']}"
    except Exception as e:
        return f"Erro ao buscar especialista: {str(e)}"
