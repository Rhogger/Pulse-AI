from crewai import Task
import json


def get_services_by_specialist_task(agent, specialist_data: str):
    """
    Args:
        specialist_data: JSON string do especialista
    """
    try:
        specialist = json.loads(specialist_data)
        specialist_id = specialist.get('id')
    except:
        specialist_id = None

    return Task(
        description=f"""
        EXECUTE AGORA:
        1. Use get_services_by_specialist com o ID {specialist_id} para listar os serviços
        2. Se não conseguir buscar por ID, use list_services
        3. Reporte exatamente o que encontrou
        
        NÃO EXPLIQUE O PROCESSO, APENAS EXECUTE.
        """,
        expected_output="Lista de serviços encontrados",
        agent=agent,
        context=specialist_data
    )


def get_service_by_id_task(agent, service_id: int):
    return Task(
        description=f"""
        EXECUTE AGORA:
        1. Use get_service com o ID {service_id}
        2. Se não encontrar, use list_services
        3. Reporte exatamente o que encontrou
        
        NÃO EXPLIQUE O PROCESSO, APENAS EXECUTE.
        """,
        expected_output="Dados do serviço encontrado",
        agent=agent
    )


def list_all_services_task(agent):
    return Task(
        description="""
        EXECUTE AGORA:
        1. Use list_services para ver todos os serviços
        2. Reporte exatamente o que encontrou
        
        NÃO EXPLIQUE O PROCESSO, APENAS EXECUTE.
        """,
        expected_output="Lista completa de serviços",
        agent=agent
    )
