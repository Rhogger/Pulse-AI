from crewai import Crew, Process
from typing import List, Dict
from app.crew.agents.conversation_analyzer_agent import get_conversation_analyzer_agent
from app.crew.llms.gemini_llm import get_gemini_llm
from app.crew.tasks.analyze_conversation_task import analyze_conversation_task


def run_analyzer_crew(messages: List[Dict], customer_status: str) -> str:
    """
    Executa a crew de análise de conversas de forma síncrona.

    Args:
        messages: Lista de mensagens para análise

    Returns:
        str: Resumo estruturado da conversa
    """
    llm = get_gemini_llm()
    analyzer_agent = get_conversation_analyzer_agent(llm)
    analyze_task = analyze_conversation_task(
        analyzer_agent, messages, customer_status)

    crew = Crew(
        agents=[analyzer_agent],
        tasks=[analyze_task],
        process=Process.sequential,
        verbose=True
    )

    # Executa de forma síncrona e retorna o resultado como string
    result = crew.kickoff()
    return str(result)
