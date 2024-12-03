from crewai import Crew
from datetime import datetime
from dotenv import load_dotenv
from app.crew.agents.calendar_agent import get_calendar_agent
from app.crew.tasks.calendar_tasks import process_calendar_request
from app.crew.llms.openai_llm import get_openai_llm


def run_calendar_crew(customer_phone: str, request_message: str) -> dict:
    """
    Executa uma crew para gerenciamento de agenda baseado em uma mensagem em linguagem natural.

    Args:
        customer_phone (str): Telefone do cliente
        request_message (str): Mensagem com a solicitação do cliente

    Returns:
        dict: Resultado da operação
    """
    load_dotenv()
    llm = get_openai_llm()
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    calendar_agent = get_calendar_agent(llm, customer_phone, current_datetime)

    task = process_calendar_request(
        agent=calendar_agent,
        request_message=request_message,
        current_datetime=current_datetime
    )

    crew = Crew(
        agents=[calendar_agent],
        tasks=[task],
        verbose=True
    )

    results = crew.kickoff()

    return {
        "text": str(results),
        "type": "text"
    }


# Exemplo de uso
result = run_calendar_crew(
    customer_phone="556493383309",
    request_message="Quero marcar um horário com a Daniela, as 15 horas dessa quarta feira para terapia"
)
