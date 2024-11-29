from crewai import Task


def list_specialists_task(agent):
    return Task(
        description="""
        EXECUTE AGORA:
        1. Use a tool 'list_specialists' para obter a lista completa de profissionais
        2. Organize e apresente as informações da seguinte forma:
           
           ESPECIALISTAS DA CLÍNICA:
           - Nome completo do profissional
           - Número de contato para agendamentos
           
           CASOS ESPECIAIS:
           - Se encontrar especialistas com nomes similares,
             agrupe-os e destaque características únicas de cada um
           - Se precisar de confirmação do cliente sobre qual especialista
             está buscando, faça perguntas específicas
           
        IMPORTANTE:
        - Formate a resposta de maneira amigável e profissional
        - Use marcadores para melhor organização visual
        - Destaque informações importantes em negrito quando necessário
        - Mantenha um tom cordial e prestativo
        
        NÃO EXPLIQUE O PROCESSO, APENAS APRESENTE OS RESULTADOS ORGANIZADOS.
        """,
        expected_output="Lista detalhada e organizada dos especialistas",
        agent=agent
    )
