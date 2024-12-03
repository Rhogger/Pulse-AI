from crewai import Crew
from dotenv import load_dotenv
from app.crew.agents.service_displayer_agent import get_services_display_agent
from app.crew.llms.openai_llm import get_openai_llm
from app.crew.tasks.get_services_task import list_services_task


def run_service_crew() -> dict:
    """
    Executa uma crew com o agente de serviços executando ambas as tasks.

    Args:
        specialist_id (int, optional): ID do especialista para filtrar serviços.
            Se None, lista todos os serviços.
    """
    load_dotenv()

    # Inicializa o LLM
    llm = get_openai_llm()

    # Cria o agente de serviços
    service_advisor = get_services_display_agent(llm)

    # Cria as tasks
    tasks = [
        list_services_task(service_advisor),  # Lista todos os serviços
    ]

    # Cria a crew com um agente e as duas tasks
    crew = Crew(
        agents=[service_advisor],
        tasks=tasks,
        verbose=True
    )

    # Executa a crew
    results = crew.kickoff()

    # Retorna um dicionário com a resposta
    return {
        "text": str(results),
        "type": "text"
    }


result = run_service_crew()
print(result)
