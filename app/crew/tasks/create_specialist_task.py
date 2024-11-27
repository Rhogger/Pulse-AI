from crewai import Task


def create_specialist_task(agent, name: str, contact_number: str):
    return Task(
        description=f"""
        EXECUTE AGORA:
        1. Use create_new_specialist com estes dados exatos:
        {{"name": "{name}", "contact_number": "{contact_number}"}}
        
        2. Reporte a resposta da tool EXATAMENTE como ela retornou, incluindo o ID
        
        NÃO EXPLIQUE O PROCESSO, APENAS EXECUTE E RETORNE O JSON COMPLETO.
        """,
        expected_output="JSON do especialista criado, incluindo ID",
        agent=agent
    )
