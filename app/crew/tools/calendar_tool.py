import os
from crewai.tools import tool
import requests
from datetime import datetime

BASE_URL = os.getenv("BASE_URL")


@tool
def create_appointment(specialist_id: int, service_id: int, customer_id: int,
                       start_time: str, notes: str = None) -> str:
    """Útil para criar um novo agendamento.
    Args:
        specialist_id (int): ID do especialista
        service_id (int): ID do serviço
        customer_id (int): ID do cliente
        start_time (str): Data e hora de início no formato ISO (YYYY-MM-DDTHH:MM:SS)
        notes (str, opcional): Observações sobre o agendamento
    """
    try:
        response = requests.post(
            f"{BASE_URL}/appointments/",
            json={
                "specialist_id": specialist_id,
                "service_id": service_id,
                "customer_id": customer_id,
                "start_time": start_time,
                "notes": notes
            }
        )

        if response.status_code == 200:
            return f"Agendamento criado com sucesso!\n{response.json()}"
        return f"Erro ao criar agendamento: {response.text}"
    except Exception as e:
        return f"Erro ao criar agendamento: {str(e)}"


@tool
def get_available_slots(start_date: str, end_date: str,
                        specialist_id: int = None, service_id: int = None) -> str:
    """Útil para buscar horários disponíveis.
    Args:
        start_date (str): Data inicial no formato ISO
        end_date (str): Data final no formato ISO
        specialist_id (int, opcional): ID do especialista
        service_id (int, opcional): ID do serviço
    """
    try:
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        if specialist_id:
            params["specialist_id"] = specialist_id
        if service_id:
            params["service_id"] = service_id

        response = requests.get(
            f"{BASE_URL}/appointments/available-slots",
            params=params
        )

        if response.status_code == 200:
            slots = response.json()
            return f"Horários disponíveis encontrados:\n{slots}"
        return f"Erro ao buscar horários: {response.text}"
    except Exception as e:
        return f"Erro ao buscar horários: {str(e)}"


@tool
def get_appointments_by_contact(contact: str, start_date: str, end_date: str) -> str:
    """Útil para buscar agendamentos de um cliente pelo número de contato.
    Args:
        contact (str): Número de contato do cliente
        start_date (str): Data inicial no formato ISO
        end_date (str): Data final no formato ISO
    """
    try:
        response = requests.get(
            f"{BASE_URL}/appointments/by-contact/{contact}",
            params={
                "start_date": start_date,
                "end_date": end_date
            }
        )

        if response.status_code == 200:
            appointments = response.json()
            return f"Agendamentos encontrados:\n{appointments}"
        return f"Erro ao buscar agendamentos: {response.text}"
    except Exception as e:
        return f"Erro ao buscar agendamentos: {str(e)}"
