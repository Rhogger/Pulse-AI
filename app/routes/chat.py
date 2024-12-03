from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
import re
from zoneinfo import ZoneInfo

from app.services.chat_service import process_new_message, get_session_analysis, get_crew_response

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


class CrewResponse(BaseModel):
    contact_number: str


@router.post("/webhook")
async def handle_webhook(data: dict):
    try:
        print("\n=== INICIANDO PROCESSAMENTO DO WEBHOOK ===")
        print(f"Dados recebidos: {data}")

        # Extrai o número do contato do remoteJid (remove @s.whatsapp.net)
        contact_number = data.get("data", {}).get("key", {}).get("remoteJid", "").split(
            "@")[0] if data.get("data", {}).get("key", {}).get("remoteJid") else None
        print(f"Número do contato extraído: {contact_number}")

        # Usa o messageTimestamp diretamente do data
        timestamp = data.get("data", {}).get("messageTimestamp")
        if timestamp:
            sent_at = datetime.fromtimestamp(
                timestamp, tz=ZoneInfo("America/Sao_Paulo"))
        else:
            sent_at = datetime.now(tz=ZoneInfo("America/Sao_Paulo"))
        print(f"Timestamp da mensagem: {sent_at}")

        message = WhatsAppMessage(
            name=data.get("data", {}).get("pushName", ""),
            contact_number=contact_number,
            message_content=data.get("data", {}).get(
                "message", {}).get("conversation", ""),
            sent_at=sent_at
        )
        print(f"Mensagem criada: {message}")

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
        print(f"Resultado do processamento: {result}")

        return result

    except HTTPException as e:
        print(f"\nHTTPException: {e.detail}")
        raise
    except Exception as e:
        print(f"\nERRO GERAL ao processar webhook:")
        print(f"Tipo do erro: {type(e)}")
        print(f"Mensagem de erro: {str(e)}")
        print(f"Traceback: {e.__traceback__}")
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


@router.post("/crew-response")
async def get_contact_crew_response(data: CrewResponse):
    """Endpoint para recuperar a resposta da crew para um contato específico."""
    try:
        response = await get_crew_response(data.contact_number)
        if not response:
            raise HTTPException(
                status_code=404,
                detail="Resposta não encontrada para este contato"
            )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar resposta da crew: {str(e)}"
        )
