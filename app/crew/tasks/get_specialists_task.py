from crewai import Task


def list_specialists_task(agent):
    return Task(
        description="""
        EXECUTE AGORA:
        1. Obtenha a lista completa de profissionais
        2. Organize e apresente as informações da seguinte forma:
           
           ESPECIALISTAS DA CLÍNICA:
           - Nome do profissional
           
        IMPORTANTE:
        - Formate a resposta de maneira amigável e profissional
        - Use marcadores para melhor organização visual
        - Destaque informações importantes em negrito quando necessário
        - Mantenha um tom cordial e prestativo
        
        NÃO EXPLIQUE O PROCESSO, APENAS APRESENTE OS RESULTADOS ORGANIZADOS.
        """,
        expected_output="Lista detalhada e organizada dos especialistas",
        agent=agent)
