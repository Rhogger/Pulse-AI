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
    Analisa uma lista de mensagens usando a crew especializada de forma síncrona.

    Args:
        messages: Lista de mensagens para análise

    Returns:
        str: Resumo estruturado da conversa
    """
    try:
        # Formata as mensagens para o formato esperado
        formatted_messages = [
            {
                'content': msg['content'],
                'timestamp': msg['created_at']
            }
            for msg in messages
        ]

        # Executa a crew de análise em um processo separado
        return _run_crew_in_process(run_analyzer_crew, formatted_messages, customer_status)

    except Exception as e:
        raise Exception(f"Erro ao analisar conversa: {str(e)}")


def execute_hierarchical_crew(contact_number: str, initial_message: str) -> str:
    """
    Executa a crew hierárquica de forma síncrona.

    Args:
        contact_number: Número de contato do cliente
        initial_message: Mensagem inicial ou resumo da análise

    Returns:
        str: Resultado da execução da crew hierárquica
    """
    try:
        # Executa a crew hierárquica em um processo separado
        return _run_crew_in_process(run_crew, contact_number, initial_message)

    except Exception as e:
        raise Exception(f"Erro ao executar crew hierárquica: {str(e)}")
