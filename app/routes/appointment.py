from zoneinfo import ZoneInfo
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from datetime import datetime, timedelta, timezone
from app.services.google_calendar_service import GoogleCalendarService
from app.models.specialist import Specialist
from app.models.service import Service
from app.models.customer import Customer
from google.auth.exceptions import DefaultCredentialsError
from typing import Optional

router = APIRouter()


class AppointmentIn(BaseModel):
    specialist_id: int
    service_id: int
    customer_id: int
    start_time: datetime
    notes: str | None = None

    @validator('specialist_id')
    def validate_specialist_id(cls, v):
        if v <= 0:
            raise ValueError("ID do especialista deve ser maior que zero")
        return v

    @validator('service_id')
    def validate_service_id(cls, v):
        if v <= 0:
            raise ValueError("ID do serviço deve ser maior que zero")
        return v

    @validator('start_time')
    def validate_start_time(cls, v):
        if v < datetime.now():
            raise ValueError("A data de início não pode ser no passado")
        return v

    @validator('customer_id')
    def validate_customer_id(cls, v):
        if v <= 0:
            raise ValueError("ID do cliente deve ser maior que zero")
        return v


@router.post("/")
async def create_appointment(appointment: AppointmentIn):
    try:
        # Converte o horário para o timezone de Brasília
        start_time = appointment.start_time.astimezone(
            ZoneInfo('America/Sao_Paulo'))

        # Verifica se o horário está dentro do horário comercial
        hour = start_time.hour
        if not (8 <= hour < 12 or 14 <= hour < 18):
            raise HTTPException(
                status_code=400,
                detail="O agendamento deve estar dentro do horário comercial (8h-12h ou 14h-18h)"
            )

        # Verifica se o especialista existe
        specialist = await Specialist.get(id=appointment.specialist_id)
        if not specialist:
            raise HTTPException(
                status_code=404,
                detail=f"Especialista com ID {appointment.specialist_id} não encontrado"
            )

        # Verifica se o serviço existe
        service = await Service.get(id=appointment.service_id)
        if not service:
            raise HTTPException(
                status_code=404,
                detail=f"Serviço com ID {appointment.service_id} não encontrado"
            )

        # Verifica se o cliente existe
        customer = await Customer.get(id=appointment.customer_id)
        if not customer:
            raise HTTPException(
                status_code=404,
                detail=f"Cliente com ID {appointment.customer_id} não encontrado"
            )

        duration_minutes = service.total_duration_minutes
        end_time = appointment.start_time + timedelta(minutes=duration_minutes)

        try:
            calendar_service = GoogleCalendarService()
            event = await calendar_service.create_appointment(
                specialist_name=specialist.name,
                service_name=service.name,
                customer_name=customer.name,
                customer_contact=customer.contact_number,
                start_time=appointment.start_time,
                end_time=end_time,
                notes=appointment.notes
            )
            return event

        except DefaultCredentialsError:
            raise HTTPException(
                status_code=500,
                detail="Erro na configuração das credenciais do Google Calendar"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao criar evento no Google Calendar: {str(e)}"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/available-slots")
async def get_available_slots(
    start_date: str,
    end_date: str,
    specialist_id: Optional[int] = None,
    service_id: Optional[int] = None
):
    try:
        # Convertendo as strings para datetime e garantindo que estão em UTC
        start_datetime = datetime.fromisoformat(
            start_date).replace(tzinfo=timezone.utc)
        end_datetime = datetime.fromisoformat(
            end_date).replace(tzinfo=timezone.utc)

        calendar_service = GoogleCalendarService()

        # Se um serviço for especificado, obtém sua duração
        duration_minutes = None
        if service_id:
            service = await Service.get(id=service_id)
            if not service:
                raise HTTPException(
                    status_code=404,
                    detail=f"Serviço com ID {service_id} não encontrado"
                )
            duration_minutes = service.total_duration_minutes

        # Se um especialista for especificado, verifica se existe
        if specialist_id:
            specialist = await Specialist.get(id=specialist_id)
            if not specialist:
                raise HTTPException(
                    status_code=404,
                    detail=f"Especialista com ID {specialist_id} não encontrado"
                )

        slots = await calendar_service.get_available_slots(
            start_date=start_datetime,
            end_date=end_datetime,
            specialist_id=specialist_id,
            service_id=service_id,
            duration_minutes=duration_minutes
        )

        return slots

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-contact/{contact}")
async def get_appointments_by_contact(
    contact: str,
    start_date: str,
    end_date: str
):
    try:
        print(f"\nRecebendo requisição de busca por contato:")
        print(f"Contato: {contact}")
        print(f"Data início: {start_date}")
        print(f"Data fim: {end_date}")

        # Converte as strings de data para datetime
        try:
            start_datetime = datetime.fromisoformat(start_date)
            end_datetime = datetime.fromisoformat(end_date)
            print("Datas convertidas com sucesso")
        except ValueError as e:
            print(f"Erro ao converter datas: {str(e)}")
            raise

        calendar_service = GoogleCalendarService()
        print("Iniciando busca no Google Calendar")

        appointments = await calendar_service.get_appointments_by_contact(
            contact=contact,
            start_date=start_datetime,
            end_date=end_datetime
        )

        print(f"Busca concluída. Encontrados {len(appointments)} agendamentos")
        return appointments

    except ValueError as e:
        print(f"Erro de validação: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Formato de data inválido: {str(e)}"
        )
    except Exception as e:
        print(f"Erro não esperado: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar agendamentos: {str(e)}"
        )


@router.delete("/{event_id}")
async def delete_appointment(event_id: str):
    """
    Deleta um agendamento existente.

    Args:
        event_id (str): ID do evento no Google Calendar

    Returns:
        dict: Mensagem de sucesso

    Raises:
        HTTPException: Se houver erro ao deletar o agendamento
    """
    try:
        calendar_service = GoogleCalendarService()
        await calendar_service.delete_appointment(event_id)
        return {"detail": "Agendamento cancelado com sucesso"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao cancelar agendamento: {str(e)}"
        )
