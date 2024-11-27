from crewai import Task


def create_customer_task(agent):
    return Task(
        description="""
        Analise a resposta do agente anterior. 
        
        Se foi indicado que o cliente não existe, extraia o nome e telefone da conversa inicial e cadastre um novo cliente com esses dados. 
        
        Retorne os dados do cliente cadastrado.
        """,
        expected_output="JSON do cliente criado, incluindo ID",
        agent=agent,
    )
