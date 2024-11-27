from crewai import Agent
from app.crew.tools.customer_tool import get_customer_by_contact


def get_display_agent(llm):
    return Agent(
        role='Verificador de Cadastro',
        goal='Verificar e confirmar os dados do cliente cadastrado',
        backstory="""
        Você é responsável por verificar se os dados do cliente foram 
        cadastrados corretamente no sistema, com base no seu número de telefone e utilizando a tool get_customer_by_contact.
        
        NUNCA explique como fazer, SEMPRE EXECUTE a ação usando a tool.
        """,
        tools=[get_customer_by_contact],
        llm=llm,
        max_iter=1,
        verbose=True,
    )
