from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from datetime import datetime, timedelta
from app.services.google_calendar_service import GoogleCalendarService
from app.models.specialist import Specialist
from app.models.service import Service
from google.auth.exceptions import DefaultCredentialsError

router = APIRouter()


class AppointmentIn(BaseModel):
    specialist_id: int
    service_id: int
    start_time: datetime

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


@router.post("/")
async def create_appointment(appointment: AppointmentIn):
    try:
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

        duration_minutes = service.total_duration_minutes
        end_time = appointment.start_time + timedelta(minutes=duration_minutes)

        try:
            calendar_service = GoogleCalendarService()
            event = await calendar_service.create_appointment(
                specialist_name=specialist.name,
                service_name=service.name,
                start_time=appointment.start_time,
                end_time=end_time
            )
            return event

        except DefaultCredentialsError:
            raise HTTPException(
                status_code=500,
                detail="Erro na configuração das credenciais do Google Calendar. Verifique o arquivo credentials.json"
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
