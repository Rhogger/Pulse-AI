from crewai import Crew, Process
from dotenv import load_dotenv
from app.crew.agents.customer_reception_agent import get_reception_agent
from app.crew.agents.manager_agent import get_manager_agent
from app.crew.agents.service_displayer_agent import get_services_display_agent
from app.crew.agents.specialist_displayer_agent import get_specialists_display_agent
from app.crew.llms.gemini_llm import get_gemini_llm
from app.crew.tasks.get_services_task import list_services_task, list_services_by_specialist_task
from app.crew.tasks.get_specialists_task import list_specialists_task
from app.crew.tasks.welcome_customer_task import welcome_customer_task
from app.crew.agents.customer_register_agent import get_register_agent
from app.crew.tasks.create_customer_task import create_customer_task
from app.services.customer_service import get_all_customers


def run_crew(contact_number: str, initial_message: str) -> str:
    load_dotenv()

    user_info = get_all_customers(contact_number)

    if isinstance(user_info, tuple):
        user_info = {}
    elif isinstance(user_info, list):
        user_info = user_info[0] if user_info else {}

    customer_name = user_info.get(
        'name') if isinstance(user_info, dict) else None
    customer_contact = user_info.get('number_contact') if isinstance(
        user_info, dict) else contact_number

    print(customer_name)
    print(customer_contact)

    llm = get_gemini_llm()
    llm_manager = get_gemini_llm()

    manager_agent = get_manager_agent(
        llm_manager)
    receptionist = get_reception_agent(llm, customer_name, customer_contact)
    register = get_register_agent(llm, customer_info)
    specialist_advisor = get_specialists_display_agent(llm)
    service_advisor = get_services_display_agent(llm)

    welcome = welcome_customer_task(
        receptionist, initial_message, customer_name)
    create_customer = create_customer_task(register, welcome)
    get_specialists = list_specialists_task(specialist_advisor)
    get_services = list_services_task(service_advisor)
    get_services_by_specialist = list_services_by_specialist_task(
        service_advisor)

    tasks = [
        welcome,
        # create_customer,
        # get_specialists,
        # get_services,
        # get_services_by_specialist
    ]

    crew = Crew(
        agents=[
            receptionist,
            # register,
            # specialist_advisor,
            # service_advisor
        ],
        tasks=tasks,
        # manager_agent=manager_agent,
        verbose=True,
    )

    results = crew.kickoff()
    return str(results)