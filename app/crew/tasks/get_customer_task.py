from crewai import Task


def get_customer_task(agent, contact_number: str):
    return Task(
        description=f"""
        Verifique o cliente com o número: {contact_number}
        
        Sua tarefa é:
        1. Buscar clientes com este número no sistema
        2. Retornar uma resposta estruturada no seguinte formato JSON:
           {{"status": "encontrado", "dados": "dados completos do cliente"}}
           ou
           {{"status": "nao_encontrado", "dados": "Nenhum cliente encontrado"}}
        
        Importante: 
        - Mantenha a resposta exatamente no formato JSON especificado
        - Inclua todos os dados do cliente se encontrado
        """,
        expected_output="""
        Resposta em formato JSON com status e dados do cliente
        """,
        agent=agent
    )
