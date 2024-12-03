from typing import List, Dict
from app.crew.crews.conversation_analyzer_crew import run_analyzer_crew
from app.crew.crews.hierarquical_crew import run_crew
import multiprocessing
from functools import partial


def _run_crew_in_process(func, *args):
    """Executa uma crew em um processo separado."""
    with multiprocessing.Pool(1) as pool:
        result = pool.apply(func, args)
    return result


def execute_analyze_conversation_crew(messages: List[Dict], customer_status: str) -> str:
    """
    Analisa uma lista de mensagens e retorna a intenção identificada.
    """
    try:
        formatted_messages = [
            {
                'content': msg['content'],
                'timestamp': msg['created_at']
            }
            for msg in messages
        ]

        # Retorna apenas a palavra que identifica a intenção
        return _run_crew_in_process(run_analyzer_crew, formatted_messages, customer_status)

    except Exception as e:
        raise Exception(f"Erro ao analisar conversa: {str(e)}")


def execute_hierarchical_crew(customer_name: str, contact_number: str, intention: str) -> dict:
    """
    Executa a crew específica baseada na intenção identificada.
    """
    try:
        return _run_crew_in_process(
            run_crew,
            customer_name,
            contact_number,
            intention
        )

    except Exception as e:
        raise Exception(f"Erro ao executar crew específica: {str(e)}")
