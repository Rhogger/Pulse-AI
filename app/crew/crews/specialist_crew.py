from crewai import Crew
from dotenv import load_dotenv
from app.crew.agents.specialist_displayer_agent import get_specialists_display_agent
from app.crew.llms.openai_llm import get_openai_llm
from app.crew.tasks.get_specialists_task import list_specialists_task


def run_specialist_crew() -> dict:
    """
    Executa uma crew simples apenas com o agente de especialistas.
    """
    load_dotenv()

    # Inicializa o LLM
    llm = get_openai_llm()

    # Cria o agente
    specialist_advisor = get_specialists_display_agent(llm)

    # Cria a task
    get_specialists = list_specialists_task(specialist_advisor)

    # Cria a crew com apenas um agente e uma task
    crew = Crew(
        agents=[specialist_advisor],
        tasks=[get_specialists],
        verbose=True
    )

    # Executa a crew
    results = crew.kickoff()

    # Retorna um dicionário com a resposta
    return {
        "text": str(results),
        "type": "text"
    }


result = run_specialist_crew()
print(result)
