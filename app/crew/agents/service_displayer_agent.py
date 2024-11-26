from crewai import Agent
import os
from app.crew.tools.service_tool import (
    list_services,
    get_service,
    get_services_by_specialist
)


def get_service_display_agent(llm):
    return Agent(
        role='Verificador de Serviços',
        goal='Verificar com precisão os serviços cadastrados',
        backstory="""
        Você é um auditor que EXECUTA verificações de serviços.
        
        NUNCA explique como fazer, SEMPRE EXECUTE a ação usando as tools.
        
        Para verificar, você DEVE:
        1. Se tiver ID do especialista, use get_services_by_specialist
        2. Se tiver ID do serviço, use get_service
        3. Se não tiver IDs, use list_services
        4. Reporte EXATAMENTE o que encontrou
        """,
        tools=[list_services, get_service, get_services_by_specialist],
        llm=llm,
        allow_delegation=False,
        max_iter=1,
        verbose=True
    )
