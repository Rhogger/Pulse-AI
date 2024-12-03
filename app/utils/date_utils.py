from datetime import datetime
from zoneinfo import ZoneInfo

TIMEZONE_BR = ZoneInfo('America/Sao_Paulo')


def normalize_datetime(dt: datetime) -> datetime:
    """
    Normaliza um datetime para o timezone de Brasília.
    Se não tiver timezone, assume que é Brasília.
    Se tiver timezone diferente, converte para Brasília.
    """
    if dt.tzinfo is None:
        # Se não tem timezone, assume Brasília
        return dt.replace(tzinfo=TIMEZONE_BR)
    # Se tem timezone, converte para Brasília
    return dt.astimezone(TIMEZONE_BR)


def get_current_datetime() -> datetime:
    """Retorna o datetime atual no timezone de Brasília."""
    return datetime.now(TIMEZONE_BR)
