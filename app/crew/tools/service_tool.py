import os
from crewai.tools import tool
import requests

BASE_URL = os.getenv("BASE_URL")


@tool
def list_services() -> str:
    """Útil para listar todos os serviços cadastrados no sistema."""
    try:
        response = requests.get(f"{BASE_URL}/services/")

        if response.status_code != 200:
            return f"Erro ao listar serviços: {response.text}"

        services = response.json()
        if not services:
            return "Nenhum serviço encontrado."

        return "\n".join([
            f"ID: {s['id']}, Nome: {s['name']}, Especialista ID: {s['specialist_id']}, "
            f"Duração: {s['duration_hours']}h{s['duration_minutes']}min"
            for s in services
        ])
    except Exception as e:
        return f"Erro ao listar serviços: {str(e)}"


@tool
def get_service(service_id: int) -> str:
    """Útil para buscar um serviço específico pelo ID."""
    try:
        response = requests.get(f"{BASE_URL}/services/{service_id}")

        if response.status_code == 404:
            return "Serviço não encontrado"
        elif response.status_code != 200:
            return f"Erro ao buscar serviço: {response.text}"

        service = response.json()
        return (f"ID: {service['id']}, Nome: {service['name']}, "
                f"Especialista ID: {service['specialist_id']}, "
                f"Duração: {service['duration_hours']}h{service['duration_minutes']}min")
    except Exception as e:
        return f"Erro ao buscar serviço: {str(e)}"


@tool
def get_services_by_specialist(specialist_id: int) -> str:
    """Útil para listar todos os serviços de um especialista específico."""
    try:
        response = requests.get(
            f"{BASE_URL}/services/by-specialist/{specialist_id}")

        if response.status_code == 404:
            return "Nenhum serviço encontrado para este especialista"
        elif response.status_code != 200:
            return f"Erro ao buscar serviços: {response.text}"

        services = response.json()
        return "\n".join([
            f"ID: {s['id']}, Nome: {s['name']}, "
            f"Duração: {s['duration_hours']}h{s['duration_minutes']}min"
            for s in services
        ])
    except Exception as e:
        return f"Erro ao listar serviços do especialista: {str(e)}"
