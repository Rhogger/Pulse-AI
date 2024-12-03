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
                        specialist_name: str = None, service_type: str = None) -> str:
    """Útil para buscar horários disponíveis.
    Args:
        start_date (str): Data inicial no formato ISO
        end_date (str): Data final no formato ISO
        specialist_name (str, opcional): Nome do especialista
        service_type (str, opcional): Tipo de serviço
    """
    try:
        # Primeiro, busca os IDs correspondentes aos nomes
        specialist_id = None
        service_id = None
        
        if specialist_name:
            specialist_response = requests.get(
                f"{BASE_URL}/specialists/search",
                params={"name": specialist_name}
            )
            if specialist_response.status_code == 200:
                specialist_data = specialist_response.json()
                if specialist_data:
                    specialist_id = specialist_data[0]["id"]

        if service_type:
            service_response = requests.get(
                f"{BASE_URL}/services/search",
                params={"name": service_type}
            )
            if service_response.status_code == 200:
                service_data = service_response.json()
                if service_data:
                    service_id = service_data[0]["id"]

        # Agora busca os horários disponíveis
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "specialist_id": specialist_id,
            "service_id": service_id
        }

        response = requests.get(
            f"{BASE_URL}/appointments/available-slots",
            params=params
        )

        if response.status_code == 200:
            slots = response.json()
            # Formata a resposta de maneira amigável
            formatted_slots = []
            for slot in slots:
                dt = datetime.fromisoformat(slot["datetime"])
                formatted_slots.append(
                    dt.strftime("%A, %d de %B às %H:%M")
                )
            return "\n".join(formatted_slots)
        return "Não foi possível encontrar horários disponíveis para o período solicitado."
    except Exception as e:
        return f"Ocorreu um erro ao buscar horários disponíveis: {str(e)}"


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


@tool
def cancel_appointment(event_id: str) -> str:
    """Útil para cancelar um agendamento existente.
    Args:
        event_id (str): ID do agendamento a ser cancelado
    """
    try:
        response = requests.delete(
            f"{BASE_URL}/appointments/{event_id}"
        )

        if response.status_code == 200:
            return "Agendamento cancelado com sucesso!"
        return f"Erro ao cancelar agendamento: {response.text}"
    except Exception as e:
        return f"Erro ao cancelar agendamento: {str(e)}"
