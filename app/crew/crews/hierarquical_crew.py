from crewai import Crew
from dotenv import load_dotenv
from app.crew.agents.customer_reception_agent import get_reception_agent
from app.crew.agents.manager_agent import get_manager_agent
from app.crew.agents.service_displayer_agent import get_services_display_agent
from app.crew.agents.specialist_displayer_agent import get_specialists_display_agent
from app.crew.agents.calendar_agent import get_calendar_agent
from app.crew.llms.openai_llm import get_openai_llm
from app.crew.tasks.welcome_customer_task import welcome_customer_task
from app.crew.tasks.get_services_task import list_services_task
from app.crew.tasks.get_specialists_task import list_specialists_task
from app.crew.tasks.calendar_tasks import process_calendar_request

def run_crew(customer_name: str, contact_number: str, intention: str) -> dict:
    """
    Executa a crew apropriada baseada na intenção identificada.
    
    Args:
        customer_name: Nome do cliente
        contact_number: Número de contato
        intention: Intenção identificada (recepcao, especialista, servico ou agendamento)
    """
    load_dotenv()
    llm = get_openai_llm()

    # Configura agentes conforme necessidade
    if intention == "recepcao":
        agent = get_reception_agent(llm, customer_name, contact_number)
        task = welcome_customer_task(agent, "Olá", customer_name)
        agents = [agent]
        tasks = [task]
    
    elif intention == "especialista":
        agent = get_specialists_display_agent(llm)
        task = list_specialists_task(agent)
        agents = [agent]
        tasks = [task]
    
    elif intention == "servico":
        agent = get_services_display_agent(llm)
        task = list_services_task(agent)
        agents = [agent]
        tasks = [task]
    
    elif intention == "agendamento":
        agent = get_calendar_agent(llm, customer_name, contact_number)
        task = process_calendar_request(agent, "Verificar disponibilidade")
        agents = [agent]
        tasks = [task]
    
    else:
        # Caso padrão - recepção
        agent = get_reception_agent(llm, customer_name, contact_number)
        task = welcome_customer_task(agent, "Olá", customer_name)
        agents = [agent]
        tasks = [task]

    # Cria e executa a crew
    crew = Crew(
        agents=agents,
        tasks=tasks,
        verbose=True
    )

    results = crew.kickoff()

    return {
        "text": str(results),
        "type": "text",
        "contact_number": contact_number
    }
