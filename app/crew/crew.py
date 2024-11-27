from crewai import Crew, Process
from dotenv import load_dotenv
from app.crew.agents.customer_reception_agent import get_reception_agent
from app.crew.llms.gemma2_llm import get_gemma2_llm
from app.crew.llms.llama3_2_llm import get_llama3_2_llm
from app.crew.agents.manager_agent import get_manager_agent
from app.crew.tasks.welcome_customer_task import welcome_customer_task
from app.crew.agents.customer_checker_agent import get_display_agent
from app.crew.agents.customer_register_agent import get_register_agent
from app.crew.tasks.get_customer_task import get_customer_task
from app.crew.tasks.create_customer_task import create_customer_task
from app.services.customer_service import get_all_customers


async def run_crew(contact_number, initial_message):
    load_dotenv()

    user_info = await get_all_customers(contact_number)

    if isinstance(user_info, list) and user_info:
        user_info = user_info[0]

    customer_name = user_info.get(
        'name') if isinstance(user_info, dict) else None
    customer_contact = user_info.get('number_contact') if isinstance(
        user_info, dict) else contact_number

    llm = get_gemma2_llm()
    llm_manager = get_llama3_2_llm()

    manager = get_manager_agent(llm_manager, customer_name, customer_contact)
    recepcionista = get_reception_agent(llm, customer_name)
    cadastrador = get_register_agent(llm, customer_name, customer_contact)

    welcome = welcome_customer_task(
        manager, initial_message, customer_name, customer_contact)
    create_customer = create_customer_task(cadastrador)

    tasks = [
        welcome,
        create_customer
    ]

    crew = Crew(
        agents=[recepcionista, cadastrador],
        tasks=tasks,
        process=Process.hierarchical,
        manager_agent=manager,
        verbose=True,
    )

    results = await crew.kickoff()
    return results
