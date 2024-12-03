from redis import asyncio as aioredis
import json
from datetime import datetime, timedelta
from typing import List, Optional, Dict
import os
from dotenv import load_dotenv
from app.enum.session_status import SessionStatus
from app.crew.crews.hierarquical_crew import run_crew
from app.services.crews_service import execute_analyze_conversation_crew
from app.utils.date_utils import normalize_datetime, get_current_datetime, TIMEZONE_BR
import httpx

# Carrega variáveis de ambiente
load_dotenv()
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost")
SESSION_TTL = int(os.getenv("SESSION_TTL", 14400))  # 4 horas em segundos
WHATSAPP_API_KEY = os.getenv("WHATSAPP_API_KEY")

# Inicializa Redis
redis = aioredis.from_url(REDIS_URL, decode_responses=True)


class RedisKeys:
    @staticmethod
    def session_key(contact: str) -> str:
        return f"chat:session:{contact}"

    @staticmethod
    def messages_key(session_id: str) -> str:
        return f"chat:messages:{session_id}"

    @staticmethod
    def crew_response_key(contact: str) -> str:
        return f"chat:crew_response:{contact}"


async def get_or_create_session(contact_number: str, name: str) -> Dict:
    """Busca ou cria uma sessão no Redis."""
    try:
        session_key = RedisKeys.session_key(contact_number)
        session_data = await redis.get(session_key)

        if session_data:
            try:
                session = json.loads(session_data)
                session['name'] = name
                last_interaction = normalize_datetime(
                    datetime.fromisoformat(session['last_interaction'])
                )
                if last_interaction > get_current_datetime() - timedelta(seconds=SESSION_TTL):
                    await redis.set(
                        session_key,
                        json.dumps(session),
                        ex=SESSION_TTL
                    )
                    return session
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Erro ao decodificar sessão existente: {str(e)}")

        session_counter = await redis.incr('chat:session:counter')
        session_id = f"{contact_number}_{session_counter}"

        current_time = get_current_datetime()
        session = {
            'id': session_id,
            'contact_number': contact_number,
            'name': name,
            'status': SessionStatus.IDLE.value,
            'last_interaction': current_time.isoformat(),
            'created_at': current_time.isoformat()
        }

        await redis.set(
            session_key,
            json.dumps(session),
            ex=SESSION_TTL
        )

        return session

    except Exception as e:
        print(f"Erro ao criar/buscar sessão: {str(e)}")
        raise


async def get_session_by_contact(contact_number: str) -> Optional[Dict]:
    """Busca uma sessão existente pelo número de contato."""
    session_key = RedisKeys.session_key(contact_number)
    session_data = await redis.get(session_key)

    if session_data:
        try:
            return json.loads(session_data)
        except json.JSONDecodeError:
            return None
    return None


async def save_message(contact_number: str, content: str) -> Dict:
    """Salva uma mensagem no Redis vinculada à sessão do contato."""
    try:
        # Busca a sessão do contato
        session = await get_session_by_contact(contact_number)
        if not session:
            raise ValueError(
                f"Sessão não encontrada para o contato {contact_number}")

        current_time = get_current_datetime()
        message_data = {
            'id': str(await redis.incr('chat:message:counter')),
            'contact_number': contact_number,
            'session_id': session['id'],  # Usa o ID da sessão existente
            'content': content,
            'created_at': current_time.isoformat()
        }

        # Debug
        print(
            f"Salvando mensagem para contato {contact_number} na sessão {session['id']}")

        messages_key = RedisKeys.messages_key(session['id'])
        await redis.lpush(messages_key, json.dumps(message_data))
        await redis.ltrim(messages_key, 0, 19)
        await redis.expire(messages_key, SESSION_TTL)

        return message_data

    except Exception as e:
        print(f"Erro ao salvar mensagem: {str(e)}")
        raise


async def get_session_messages(session_id: str) -> List[Dict]:
    """Recupera as mensagens de uma sessão."""
    try:
        messages_key = RedisKeys.messages_key(session_id)
        messages = await redis.lrange(messages_key, 0, -1)
        return [json.loads(msg) for msg in messages]
    except Exception as e:
        print(f"Erro ao recuperar mensagens: {str(e)}")
        return []


async def should_analyze_session(session_id: str) -> bool:
    """Verifica se a sessão deve ser analisada."""
    try:
        messages_key = RedisKeys.messages_key(session_id)
        messages = await redis.lrange(messages_key, 0, -1)

        if not messages:
            return False

        # Converte as mensagens para verificar timestamps
        message_list = [json.loads(msg) for msg in messages]

        # Obtém o timestamp da mensagem mais recente
        latest_message = message_list[0]
        latest_time = normalize_datetime(
            datetime.fromisoformat(latest_message['created_at'])
        )

        # Verifica se passou tempo suficiente desde a última mensagem
        current_time = get_current_datetime()
        time_diff = (current_time - latest_time).total_seconds()

        print(f"Tempo desde última mensagem: {time_diff} segundos")
        print(f"Quantidade de mensagens: {len(message_list)}")

        # Retorna True se tiver 20+ mensagens OU passou 10 segundos desde a última
        should_analyze = len(message_list) >= 20 or time_diff >= 10

        print(f"Deve analisar sessão {session_id}? {should_analyze}")

        return should_analyze

    except Exception as e:
        print(f"Erro ao verificar se deve analisar sessão: {str(e)}")
        return False


async def process_new_message(
    contact_number: str,
    content: str,
    sent_at: datetime,
    name: str
) -> Dict:
    try:
        # Verifica se é o número autorizado
        if contact_number != "556493383309":
            print(f"Número não autorizado: {contact_number}")
            return None

        sent_at = normalize_datetime(sent_at)

        session = await get_session_by_contact(contact_number)
        if not session:
            session = await get_or_create_session(contact_number, name)
        else:
            session['name'] = name
            await redis.set(
                RedisKeys.session_key(contact_number),
                json.dumps(session),
                ex=SESSION_TTL
            )

        # Debug
        print(
            f"Processando mensagem para contato {contact_number}, sessão {session['id']}")

        # Atualiza status e última interação
        session['status'] = SessionStatus.ACTIVE.value
        session['last_interaction'] = sent_at.isoformat()

        # Salva a sessão atualizada
        await redis.set(
            RedisKeys.session_key(contact_number),
            json.dumps(session),
            ex=SESSION_TTL
        )

        # Salva a mensagem usando o número do contato
        await save_message(contact_number, content)

        return {
            'status': SessionStatus.ACTIVE.value,
            'session_id': session['id']
        }

    except Exception as e:
        print(f"Erro ao processar mensagem: {str(e)}")
        raise


async def check_and_process_session(session_id: str) -> Optional[Dict]:
    """Verifica e processa a sessão se necessário."""
    try:
        if not await should_analyze_session(session_id):
            return None

        # Busca todas as sessões
        all_sessions = await redis.keys("chat:session:*")
        session = None

        # Debug
        print(
            f"Buscando sessão {session_id} entre {len(all_sessions)} sessões")

        # Procura a sessão com o ID correto
        for key in all_sessions:
            data = await redis.get(key)
            if data:
                try:
                    sess_data = json.loads(data)
                    if isinstance(sess_data, dict) and sess_data.get('id') == session_id:
                        session = sess_data
                        break
                except json.JSONDecodeError:
                    continue

        if not session:
            print(f"Sessão {session_id} não encontrada")
            return None

        # Debug
        print(f"Encontrou sessão: {session}")

        # Atualiza status para PROCESSING
        session['status'] = SessionStatus.PROCESSING.value
        await redis.set(
            RedisKeys.session_key(session['contact_number']),
            json.dumps(session),
            ex=SESSION_TTL
        )

        # Obtém e formata mensagens
        messages = await get_session_messages(session_id)
        if not messages:
            print(f"Nenhuma mensagem encontrada para sessão {session_id}")
            return None

        # Executa a análise de forma síncrona
        analysis = execute_analyze_conversation_crew(messages)

        # Executa a crew hierárquica
        print("\n=== EXECUTANDO CREW ===")
        crew_result = run_crew(
            customer_name=session['name'],
            contact_number=session['contact_number'],
            initial_message=analysis
        )
        print(f"Resultado da crew: {crew_result}")

        # Salva a resposta da crew
        await save_crew_response(session['contact_number'], crew_result)
        print("\nResposta da crew salva no Redis")

        # Envia a resposta da crew
        print("\nTentando enviar resposta para o WhatsApp...")
        await send_crew_response(session['contact_number'], crew_result['text'])

        # Após resposta da crew, limpa a sessão atual
        await redis.delete(RedisKeys.session_key(session['contact_number']))
        await redis.delete(RedisKeys.messages_key(session_id))

        # Cria nova sessão
        await get_or_create_session(session['contact_number'], session['name'])

        return {
            'previous_session_id': session_id,
            'analysis': analysis,
            'crew_result': crew_result
        }

    except Exception as e:
        print(f"\nERRO ao processar sessão:")
        print(f"Tipo do erro: {type(e)}")
        print(f"Mensagem de erro: {str(e)}")
        raise


async def get_session_analysis(session_id: str) -> Optional[Dict]:
    """Recupera a análise de uma sessão."""
    analysis_key = f"chat:analysis:{session_id}"
    analysis_data = await redis.get(analysis_key)
    return json.loads(analysis_data) if analysis_data else None


async def save_crew_response(contact_number: str, response: Dict) -> None:
    """Salva a resposta da crew no Redis."""
    try:
        response_key = RedisKeys.crew_response_key(contact_number)
        await redis.set(
            response_key,
            json.dumps(response),
            ex=SESSION_TTL  # Usa o mesmo TTL das sessões
        )
    except Exception as e:
        print(f"Erro ao salvar resposta da crew: {str(e)}")
        raise


async def get_crew_response(contact_number: str) -> Optional[Dict]:
    """Recupera a resposta da crew do Redis."""
    try:
        response_key = RedisKeys.crew_response_key(contact_number)
        response_data = await redis.get(response_key)
        if response_data:
            return json.loads(response_data)
        return None
    except Exception as e:
        print(f"Erro ao recuperar resposta da crew: {str(e)}")
        return None


async def send_crew_response(contact_number: str, text: str) -> None:
    """Envia a resposta da crew para o endpoint externo."""
    url = "https://evo-pulse.duckdns.org/message/sendText/Pulse-AI"
    
    # Adiciona o header com a API key
    headers = {
        "apikey": WHATSAPP_API_KEY
    }
    
    payload = {
        "number": contact_number,
        "text": text
    }
    
    print("\n=== INICIANDO ENVIO DE RESPOSTA DA CREW ===")
    print(f"URL: {url}")
    print(f"Headers: {headers}")
    print(f"Payload: {payload}")
    
    try:
        async with httpx.AsyncClient() as client:
            print("\nEnviando requisição...")
            response = await client.post(
                url, 
                json=payload, 
                headers=headers
            )
            print(f"\nResposta recebida - Status: {response.status_code}")
            print(f"Resposta completa: {response.text}")
            
            response.raise_for_status()
            print(f"\nResposta enviada com sucesso para {contact_number}")
            
    except httpx.HTTPStatusError as e:
        print(f"\nERRO HTTP ao enviar resposta:")
        print(f"Status Code: {e.response.status_code}")
        print(f"Response Headers: {e.response.headers}")
        print(f"Response Body: {e.response.text}")
    except Exception as e:
        print(f"\nERRO GERAL ao enviar resposta:")
        print(f"Tipo do erro: {type(e)}")
        print(f"Mensagem de erro: {str(e)}")
    finally:
        print("\n=== FIM DO ENVIO DE RESPOSTA DA CREW ===\n")
