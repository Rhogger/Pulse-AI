from crewai import Agent
from app.crew.tools.specialist_tool import list_specialists


def get_specialists_display_agent(llm):
    return Agent(
        role='Consultor de Especialistas',
        goal='Apresentar os especialistas da clínica de forma clara e organizada',
        backstory="""
        Você é um consultor especializado em apresentar os especialistas da clínica, pessoa que trabalham nela.
        
        Você DEVE:
        1. Usar list_specialists para obter todos os especialistas
        2. Organizar as informações de forma clara e amigável
        3. Destacar:
           - Nome do especialista
        
        Seja sempre cordial e profissional ao apresentar as informações.
        """,
        tools=[list_specialists],
        llm=llm,
        allow_delegation=False,
        max_iter=1,
        verbose=True
    )
