from crewai import Task


def create_customer_task(agent, welcome_task: Task):
    return Task(
        description="""
        Analise a resposta do agente anterior. 
        
        Se foi indicado que o cliente não existe, extraia o nome e número de contato das informações passadas e cadastre um novo cliente com esses dados. 
        
        Retorne os dados do cliente cadastrado.
        """,
        expected_output="JSON do cliente criado",
        agent=agent,
        context=welcome_task.output
    )
