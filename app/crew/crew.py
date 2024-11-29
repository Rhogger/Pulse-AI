from crewai import Crew, Process
from dotenv import load_dotenv
from app.crew.agents.calendar_agent import get_calendar_agent
from app.crew.agents.customer_reception_agent import get_reception_agent
from app.crew.agents.service_displayer_agent import get_services_display_agent
from app.crew.agents.specialist_displayer_agent import get_specialists_display_agent
from app.crew.llms.gemma2_llm import get_gemma2_llm
from app.crew.llms.llama3_2_llm import get_llama3_2_llm
from app.crew.agents.manager_agent import get_manager_agent
from app.crew.tasks.calendar_tasks import check_available_slots_task
from app.crew.tasks.get_services_task import list_services_task, list_services_by_specialist_task
from app.crew.tasks.get_specialists_task import list_specialists_task
from app.crew.tasks.welcome_customer_task import welcome_customer_task
from app.crew.agents.customer_register_agent import get_register_agent
from app.crew.tasks.create_customer_task import create_customer_task
from app.services.customer_service import get_all_customers


async def run_crew(contact_number, initial_message):
    load_dotenv()

    user_info = await get_all_customers(contact_number)
    print("Tipo de user_info:", type(user_info))
    print("Valor de user_info:", user_info)

    if isinstance(user_info, tuple):
        print("É uma tupla!")
        user_info = {}
    elif isinstance(user_info, list):
        print("É uma lista!")
        user_info = user_info[0] if user_info else {}

    print("user_info após conversão:", user_info)
    print("Tipo de user_info após conversão:", type(user_info))

    customer_name = user_info.get(
        'name') if isinstance(user_info, dict) else None
    print("customer_name:", customer_name, type(customer_name))

    customer_contact = user_info.get('number_contact') if isinstance(
        user_info, dict) else contact_number
    print("customer_contact:", customer_contact, type(customer_contact))

    customer_info = {
        "name": "Rhogger FS",
        "number": "64999840431"
    }
    print("customer_info estruturado:", customer_info, type(customer_info))

    llm = get_gemma2_llm()
    llm_manager = get_llama3_2_llm()

    # manager = get_manager_agent(llm_manager, customer_name, customer_contact)
    receptionist = get_reception_agent(llm, customer_name, customer_contact)
    print("Receptionist criado:", type(receptionist))

    print("Criando register...")
    register = get_register_agent(llm, customer_info)
    print("Register criado:", type(register))

    print("Criando specialist_advisor...")
    specialist_advisor = get_specialists_display_agent(llm)
    print("Specialist_advisor criado:", type(specialist_advisor))

    print("Criando service_advisor...")
    service_advisor = get_services_display_agent(llm)
    print("Service_advisor criado:", type(service_advisor))

    print("\n=== Criando Tasks ===")
    print("Criando welcome task...")
    welcome = welcome_customer_task(
        receptionist, initial_message, customer_name)
    print("Welcome task criada:", type(welcome))

    print("\nCriando create_customer task...")
    create_customer = create_customer_task(register, welcome)
    print("Create_customer task criada:", type(create_customer))

    print("\nCriando get_specialists task...")
    get_specialists = list_specialists_task(specialist_advisor)
    print("Get_specialists task criada:", type(get_specialists))

    print("\nCriando get_services task...")
    get_services = list_services_task(service_advisor)
    print("Get_services task criada:", type(get_services))

    print("\nCriando get_services_by_specialist task...")
    get_services_by_specialist = list_services_by_specialist_task(
        service_advisor, customer_name)
    print("Get_services_by_specialist task criada:",
          type(get_services_by_specialist))

    tasks = [
        welcome,
        create_customer,
        get_specialists,
        get_services,
        get_services_by_specialist
    ]
    print("\n=== Tasks criadas ===")
    print("Número de tasks:", len(tasks))
    for i, task in enumerate(tasks):
        print(f"Task {i+1}:", type(task))

    print("\n=== Criando Crew ===")
    crew = Crew(
        agents=[receptionist, register, specialist_advisor, service_advisor],
        tasks=tasks,
        process=Process.hierarchical,
        manager_llm=llm_manager,
        verbose=True,
    )
    print("Crew criada com sucesso!")

    print("\n=== Iniciando Kickoff ===")
    results = await crew.kickoff()
    print("Kickoff finalizado!")
    return results
