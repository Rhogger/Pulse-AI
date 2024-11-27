from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime
from app.services.google_auth_service import GoogleAuthService
from fastapi import HTTPException


class GoogleCalendarService:
    def __init__(self):
        auth_service = GoogleAuthService()
        self.credentials = auth_service.get_credentials()
        self.service = build('calendar', 'v3', credentials=self.credentials)
        self.calendar_id = 'primary'

    async def create_appointment(
        self,
        specialist_name: str,
        service_name: str,
        customer_name: str,
        customer_contact: str,
        start_time: datetime,
        end_time: datetime,
        notes: str | None = None
    ):
        """
        Cria um evento no Google Calendar para um agendamento.
        """
        # Cria uma descrição detalhada
        description = f"""
        Cliente: {customer_name}
        Contato: {customer_contact}
        Serviço: {service_name}
        Profissional: {specialist_name}
        """

        if notes:
            description += f"\nObservações: {notes}"

        event = {
            'summary': f'{specialist_name} - {service_name}',
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'America/Sao_Paulo',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'America/Sao_Paulo',
            },
        }

        try:
            event = self.service.events().insert(
                calendarId=self.calendar_id,
                body=event
            ).execute()

            return {
                'id': event['id'],
                'summary': event['summary'],
                'description': event['description'],
                'start': event['start']['dateTime'],
                'end': event['end']['dateTime']
            }
        except HttpError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro na API do Google Calendar: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao criar evento: {str(e)}"
            )
