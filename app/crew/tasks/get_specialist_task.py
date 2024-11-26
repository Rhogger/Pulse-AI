from crewai import Task
import json


def get_specialist_task(agent, specialist_data: str):
    """
    Args:
        specialist_data: JSON string do especialista criado na task anterior
    """
    # Converte o JSON string para dict para extrair o ID
    try:
        specialist = json.loads(specialist_data)
        specialist_id = specialist.get('id')
    except:
        specialist_id = None

    return Task(
        description=f"""
        EXECUTE AGORA:
        1. Use get_specialist com o ID {specialist_id} para confirmar o cadastro
        2. Se não conseguir buscar por ID, use list_specialists e procure pelo nome
        3. Reporte exatamente o que encontrou
        
        NÃO EXPLIQUE O PROCESSO, APENAS EXECUTE.
        """,
        expected_output="Dados encontrados do especialista",
        agent=agent,
        context=specialist_data  # Passa o contexto completo para o agente
    )
