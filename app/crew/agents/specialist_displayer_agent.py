from crewai import Agent
from app.crew.tools.specialist_tool import list_specialists, get_specialist


def get_display_agent(llm):
    return Agent(
        role='Verificador de Cadastros',
        goal='Verificar com precisão os dados cadastrados',
        backstory="""
        Você é um auditor que EXECUTA verificações de cadastro.
        
        NUNCA explique como fazer, SEMPRE EXECUTE a ação usando as tools.
        
        Para verificar, você DEVE:
        1. Executar list_specialists
        2. Analisar a resposta
        3. Se necessário, usar get_specialist com o ID específico
        """,
        tools=[list_specialists, get_specialist],
        llm=llm,
        allow_delegation=False,
        max_iter=1,
        verbose=True
    )
