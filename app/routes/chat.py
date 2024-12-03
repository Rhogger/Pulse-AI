from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
import re
from zoneinfo import ZoneInfo

from app.services.chat_service import process_new_message, get_session_analysis

router = APIRouter()


class WhatsAppMessage(BaseModel):
    name: str
    contact_number: str
    message_content: str
    sent_at: datetime


class ChatResponse(BaseModel):
    success: bool
    message: str
    data: Optional[List[str]] = None


@router.post("/webhook")
async def handle_webhook(data: dict):
    try:
        # Extrai o número do contato (remove @s.whatsapp.net)
        contact_number = data.get("sender", "").split(
            "@")[0] if data.get("sender") else None

        # Extrai o timestamp e converte para datetime com fuso de Brasília
        timestamp = data.get("data", {}).get("message", {}).get(
            "messageContextInfo", {}).get("deviceListMetadata", {}).get("senderTimestamp")
        if timestamp:
            # Converte para inteiro e depois para datetime
            timestamp_int = int(timestamp)
            sent_at = datetime.fromtimestamp(
                timestamp_int, tz=ZoneInfo("America/Sao_Paulo"))
        else:
            sent_at = datetime.now(tz=ZoneInfo("America/Sao_Paulo"))

        message = WhatsAppMessage(
            name=data.get("data", {}).get("pushName", ""),
            contact_number=contact_number,
            message_content=data.get("data", {}).get(
                "message", {}).get("conversation", ""),
            sent_at=sent_at
        )

        if not all([message.contact_number, message.message_content]):
            raise HTTPException(
                status_code=400,
                detail="Dados incompletos no webhook"
            )

        # Processa a mensagem
        result = await process_new_message(
            contact_number=message.contact_number,
            content=message.message_content,
            sent_at=message.sent_at,
            name=message.name
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar webhook: {str(e)}"
        )


@router.get("/analysis/{session_id}")
async def get_analysis(session_id: str):
    """Endpoint para recuperar a análise de uma sessão."""
    try:
        analysis = await get_session_analysis(session_id)
        if not analysis:
            raise HTTPException(
                status_code=404,
                detail="Análise não encontrada"
            )
        return analysis
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar análise: {str(e)}"
        )
