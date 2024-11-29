import os
from crewai.tools import tool
import requests
from typing import List

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

        result = []
        for s in services:
            specialists_str = ", ".join([spec["name"]
                                        for spec in s["specialists"]])
            result.append(
                f"ID: {s['id']}, Nome: {s['name']}, "
                f"Especialistas: [{specialists_str}], "
                f"Duração: {s['duration_minutes']} minutos ({s['time_slots']} slots)"
            )
        return "\n".join(result)
    except Exception as e:
        return f"Erro ao listar serviços: {str(e)}"


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
        result = []
        for s in services:
            specialists_str = ", ".join([spec["name"]
                                        for spec in s["specialists"]])
            result.append(
                f"ID: {s['id']}, Nome: {s['name']}, "
                f"Especialistas: [{specialists_str}], "
                f"Duração: {s['duration_minutes']} minutos ({s['time_slots']} slots)"
            )
        return "\n".join(result)
    except Exception as e:
        return f"Erro ao listar serviços do especialista: {str(e)}"
