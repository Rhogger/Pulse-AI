import os
from crewai.tools import tool
import requests

BASE_URL = os.getenv("BASE_URL")


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
