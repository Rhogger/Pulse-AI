from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta, timezone
from app.services.google_auth_service import GoogleAuthService
from fastapi import HTTPException
from app.models.specialist import Specialist
from app.models.service import Service
from zoneinfo import ZoneInfo


class GoogleCalendarService:
    def __init__(self):
        auth_service = GoogleAuthService()
        self.credentials = auth_service.get_credentials()
        self.service = build('calendar', 'v3', credentials=self.credentials)
        self.calendar_id = 'primary'
        self.TIMEZONE = ZoneInfo('America/Sao_Paulo')
        self.BUSINESS_HOURS = [
            {'start': 8, 'end': 12},  # Período da manhã
            {'start': 14, 'end': 18}  # Período da tarde
        ]

    def _is_within_business_hours(self, time: datetime) -> bool:
        """Verifica se o horário está dentro do horário comercial."""
        hour = time.hour
        for period in self.BUSINESS_HOURS:
            if period['start'] <= hour < period['end']:
                return True
        return False

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
        # Converte os horários para o timezone de Brasília
        start_time = start_time.astimezone(self.TIMEZONE)
        end_time = end_time.astimezone(self.TIMEZONE)

        # Valida se o horário está dentro do horário comercial
        if not self._is_within_business_hours(start_time) or not self._is_within_business_hours(end_time):
            raise HTTPException(
                status_code=400,
                detail="O agendamento deve estar dentro do horário comercial (8h-12h ou 14h-18h)"
            )

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

    async def get_available_slots(
        self,
        start_date: datetime,
        end_date: datetime,
        specialist_id: int | None = None,
        service_id: int | None = None,
        duration_minutes: int | None = None
    ):
        """
        Busca horários disponíveis no período especificado.
        """
        try:
            # Debug logs
            print(f"Buscando slots disponíveis:")
            print(f"Start date: {start_date}")
            print(f"End date: {end_date}")
            print(f"Specialist ID: {specialist_id}")
            print(f"Service ID: {service_id}")
            print(f"Duration: {duration_minutes}")

            # Busca o nome do especialista e do serviço
            specialist_name = None
            service_name = None

            if specialist_id:
                specialist = await Specialist.get(id=specialist_id)
                if specialist:
                    specialist_name = specialist.name
                    print(f"Nome do especialista: {specialist_name}")

            if service_id:
                service = await Service.get(id=service_id)
                if service:
                    service_name = service.name
                    print(f"Nome do serviço: {service_name}")

            # Garante que as datas estão em UTC
            start_date = start_date.astimezone(timezone.utc)
            end_date = end_date.astimezone(timezone.utc)

            # Formata as datas no formato RFC3339
            time_min = start_date.isoformat()
            time_max = end_date.isoformat()

            print(f"Time Min (formatted): {time_min}")
            print(f"Time Max (formatted): {time_max}")

            # Busca eventos existentes no período
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = events_result.get('items', [])

            # Define horário comercial (8h às 18h)
            business_hours = {
                'start': 8,  # 8:00
                'end': 18    # 18:00
            }

            # Gera slots disponíveis
            available_slots = []
            current_date = start_date

            while current_date <= end_date:
                # Pula fins de semana
                if current_date.weekday() >= 5:  # 5 = Sábado, 6 = Domingo
                    current_date += timedelta(days=1)
                    continue

                # Configura início e fim do dia útil
                day_start = current_date.replace(
                    hour=business_hours['start'],
                    minute=0,
                    second=0,
                    microsecond=0
                )
                day_end = current_date.replace(
                    hour=business_hours['end'],
                    minute=0,
                    second=0,
                    microsecond=0
                )

                # Filtra eventos do dia
                day_events = [
                    event for event in events
                    if self._is_event_in_day(event, current_date)
                ]

                # Gera slots disponíveis para o dia
                day_slots = self._generate_available_slots(
                    day_start,
                    day_end,
                    day_events,
                    duration_minutes or 30,
                    specialist_name,
                    service_name
                )

                available_slots.extend(day_slots)
                current_date += timedelta(days=1)

            return available_slots

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao buscar horários disponíveis: {str(e)}"
            )

    def _is_event_in_day(self, event, date):
        """Verifica se um evento está em uma determinada data."""
        event_start = datetime.fromisoformat(
            event['start']['dateTime'].replace('Z', '+00:00')
        )
        # Garantindo que a data de comparação tenha timezone
        compare_date = date.replace(tzinfo=timezone.utc)
        return event_start.date() == compare_date.date()

    def _generate_available_slots(
        self,
        day_start: datetime,
        day_end: datetime,
        events: list,
        duration_minutes: int,
        specialist_name: str | None = None,
        service_name: str | None = None
    ):
        """Gera slots disponíveis para um dia, considerando eventos existentes."""
        # Garantindo que as datas estão no timezone de Brasília
        day_start = day_start.astimezone(self.TIMEZONE)
        day_end = day_end.astimezone(self.TIMEZONE)

        # Debug dos eventos
        print("\nEventos encontrados:")
        for event in events:
            print(f"Título: {event.get('summary', 'Sem título')}")
            print(
                f"Início: {event.get('start', {}).get('dateTime', 'Sem data')}")
            print(f"Fim: {event.get('end', {}).get('dateTime', 'Sem data')}")
            print("---")

        # Filtra eventos
        filtered_events = []
        for event in events:
            if 'summary' not in event:
                continue

            print(f"Verificando evento: {event['summary']}")
            event_parts = event['summary'].split(' - ')
            if len(event_parts) != 2:
                continue

            event_specialist, event_service = event_parts
            print(f"Especialista do evento: {event_specialist}")
            print(f"Serviço do evento: {event_service}")
            print(f"Comparando com: {specialist_name} - {service_name}")

            if specialist_name and service_name:
                if specialist_name in event_specialist and service_name in event_service:
                    print("Evento corresponde ao filtro!")
                    filtered_events.append(event)

        print(f"Total de eventos filtrados: {len(filtered_events)}")

        # Ordena eventos
        sorted_events = sorted(
            filtered_events,
            key=lambda x: datetime.fromisoformat(
                x['start']['dateTime'].replace('Z', '+00:00')
            )
        )

        slots = []

        # Gera slots para cada período do horário comercial
        for period in self.BUSINESS_HOURS:
            # Define início e fim do período
            period_start = day_start.replace(
                hour=period['start'],
                minute=0,
                second=0,
                microsecond=0
            )
            period_end = day_start.replace(
                hour=period['end'],
                minute=0,
                second=0,
                microsecond=0
            )

            current_time = period_start

            while current_time + timedelta(minutes=duration_minutes) <= period_end:
                slot_end = current_time + timedelta(minutes=duration_minutes)
                has_conflict = False

                for event in sorted_events:
                    event_start = datetime.fromisoformat(
                        event['start']['dateTime'].replace('Z', '+00:00')
                    ).astimezone(self.TIMEZONE)
                    event_end = datetime.fromisoformat(
                        event['end']['dateTime'].replace('Z', '+00:00')
                    ).astimezone(self.TIMEZONE)

                    if (
                        (current_time < event_end and slot_end > event_start) or
                        (current_time <= event_start and slot_end >= event_end)
                    ):
                        has_conflict = True
                        current_time = event_end  # Pula para o fim do evento
                        break

                if not has_conflict:
                    # Verifica se o slot está dentro do horário comercial
                    if (
                        current_time.hour >= period['start'] and
                        slot_end.hour <= period['end']
                    ):
                        slots.append({
                            'start': current_time.isoformat(),
                            'end': slot_end.isoformat()
                        })
                    current_time += timedelta(minutes=duration_minutes)
                else:
                    # Se houve conflito e pulamos para o fim do evento,
                    # continuamos a partir dali sem incrementar
                    continue

        return slots
