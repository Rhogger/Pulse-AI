import asyncio
import json
import os
import signal
from contextlib import suppress

from redis import asyncio as aioredis
from dotenv import load_dotenv
from app.enum.session_status import SessionStatus
from app.services.chat_service import check_and_process_session
from app.utils.date_utils import normalize_datetime, get_current_datetime

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost")

redis = aioredis.from_url(REDIS_URL, decode_responses=True)


async def check_sessions():
    """Job para verificar sessões periodicamente."""
    try:
        while True:
            session_keys = await redis.keys("chat:session:*")

            for session_key in session_keys:
                session_data = await redis.get(session_key)

                if session_data:
                    try:
                        session = json.loads(session_data)

                        if isinstance(session, dict) and session.get('status') == SessionStatus.ACTIVE.value:
                            session_id = session.get('id')
                            if session_id:
                                result = await check_and_process_session(session_id)
                                if result:
                                    print(
                                        f"Sessão {session_id} processada: {result}")
                                    # Pausa após processar uma sessão
                                    await asyncio.sleep(1)
                    except json.JSONDecodeError as e:
                        print(f"Erro ao decodificar dados da sessão: {str(e)}")
                        continue

            # Pausa entre verificações
            await asyncio.sleep(4)

    except asyncio.CancelledError:
        print("Job de verificação de sessões cancelado")
    except Exception as e:
        print(f"Erro ao verificar sessões: {str(e)}")


async def start_session_checker():
    """Inicia o job de verificação com tratamento de sinais."""
    loop = asyncio.get_event_loop()

    # Configura handlers para sinais
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(
            sig, lambda s=sig: asyncio.create_task(shutdown(sig)))

    try:
        await check_sessions()
    finally:
        loop.remove_signal_handler(signal.SIGINT)
        loop.remove_signal_handler(signal.SIGTERM)


async def shutdown(sig):
    """Função de shutdown limpo."""
    print(f'Recebido sinal de shutdown {sig.name}...')
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

    for task in tasks:
        task.cancel()

    print(f'Cancelando {len(tasks)} tarefas pendentes')
    with suppress(asyncio.CancelledError):
        await asyncio.gather(*tasks)

    loop = asyncio.get_event_loop()
    loop.stop()
