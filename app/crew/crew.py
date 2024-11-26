from crewai import Crew
from dotenv import load_dotenv
from app.crew.llms.gemma2_llm import get_gemma2_llm
from app.crew.agents.specialist_register_agent import get_register_agent
from app.crew.agents.specialist_displayer_agent import get_display_agent
from app.crew.tasks.create_specialist_task import get_create_specialist_task
from app.crew.tasks.get_specialist_task import get_specialist_task


def get_user_input():
    print("\n=== Cadastro de Especialista ===")
    name = input("Nome do especialista: ")
    contact_number = input("Número de contato [(XX) XXXXX-XXXX]: ")
    return name, contact_number


def run_specialist_crew():
    load_dotenv()

    # Configurar LLM
    llm = get_gemma2_llm()

    # Criar agentes
    cadastrador = get_register_agent(llm)
    verificador = get_display_agent(llm)

    # Obter dados do usuário
    name, contact_number = get_user_input()

    # Criar e executar primeira task
    create_task = get_create_specialist_task(
        agent=cadastrador,
        name=name,
        contact_number=contact_number
    )

    # Executa primeira task e obtém resultado
    crew_create = Crew(
        agents=[cadastrador],
        tasks=[create_task],
        verbose=True
    )
    create_result = crew_create.kickoff()

    # Criar task de verificação com o resultado anterior
    verify_task = get_specialist_task(
        agent=verificador,
        specialist_data=create_result  # Passa o JSON do especialista criado
    )

    # Executa segunda task
    crew_verify = Crew(
        agents=[verificador],
        tasks=[verify_task],
        verbose=True
    )
    verify_result = crew_verify.kickoff()

    return f"""
    Cadastro: {create_result}
    Verificação: {verify_result}
    """


if __name__ == "__main__":
    try:
        run_specialist_crew()
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")
    except Exception as e:
        print(f"\nErro: {str(e)}")
