from crewai import Task


def list_services_task(agent):
    return Task(
        description="""
        EXECUTE AGORA:
        1. Use a tool 'list_services' para obter o catálogo completo de serviços
        2. Organize e apresente as informações da seguinte forma:
           
           SERVIÇOS DISPONÍVEIS:
           - Nome do serviço
           - Duração em minutos (calculada pelos slots de 30 minutos)
           - Lista completa dos especialistas que realizam o serviço
           
           AGRUPAMENTOS ESPECIAIS:
           - Se encontrar serviços similares (ex: "Corte Feminino" e "Corte Feminino Premium"),
             agrupe-os e explique as diferenças
           - Se encontrar serviços com múltiplos especialistas,
             destaque essa versatilidade
           
        IMPORTANTE:
        - Formate a resposta de maneira amigável e profissional
        - Use marcadores para melhor organização visual
        - Destaque informações importantes em negrito quando necessário
        - Mantenha um tom cordial e prestativo
        
        NÃO EXPLIQUE O PROCESSO, APENAS APRESENTE OS RESULTADOS ORGANIZADOS.
        """,
        expected_output="Catálogo detalhado e organizado de serviços",
        agent=agent
    )


def list_services_by_specialist_task(agent):
    return Task(
        description=f"""
        EXECUTE AGORA:
        1. Use a tool 'list_services' para obter todos os serviços disponíveis
        2. Organize e apresente os serviços do especialista:
           
           SERVIÇOS REALIZADOS PELO ESPECIALISTA:
           - Nome de cada serviço que realiza
           - Duração em minutos de cada serviço
           - Outros especialistas que também realizam o mesmo serviço
           
           CASOS ESPECIAIS:
           - Se houver especialistas com nomes similares",
             pergunte ao cliente para confirmar qual profissional está buscando
           - Se o especialista realizar versões especiais de serviços,
             destaque essas especializações
           
        IMPORTANTE:
        - Formate a resposta de maneira amigável e profissional
        - Use marcadores para melhor organização visual
        - Destaque informações importantes em negrito quando necessário
        - Mantenha um tom cordial e prestativo
        
        NÃO EXPLIQUE O PROCESSO, APENAS APRESENTE OS RESULTADOS ORGANIZADOS.
        """,
        expected_output=f"Lista organizada de serviços realizados pelo especialista mencionado",
        agent=agent
    )
