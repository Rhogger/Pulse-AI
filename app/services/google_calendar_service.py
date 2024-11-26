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

    async def create_appointment(self, specialist_name: str, service_name: str,
                                 start_time: datetime, end_time: datetime):
        """
        Cria um evento no Google Calendar para um agendamento.
        """
        event = {
            'summary': f'{specialist_name} - {service_name}',
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
