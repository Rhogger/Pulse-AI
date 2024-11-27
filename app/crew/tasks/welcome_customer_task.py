from crewai import Task


def welcome_customer_task(agent, initial_message: str, customer_name: str, customer_contact: str):
    return Task(
        description=f"""
        O cliente enviou a seguinte mensagem: "{initial_message}"
        Informações do cliente: {customer_name} {customer_contact}
        
        Sua missão é:
        1. Analise as informações do cliente recebidas
        2. Se o cliente foi encontrado no sistema:
           - Cumprimente usando o nome do cliente
           - Reconheça que é um cliente recorrente
           - Demonstre que valorizamos sua fidelidade
        3. Se é um novo cliente:
           - Dê boas-vindas especiais
           - Demonstre entusiasmo em tê-lo conosco
        
        Importante:
        - Mantenha sempre um tom cordial e prestativo
        - Demonstre que estamos felizes em atendê-lo
        - Personalize a mensagem com base no status do cliente
        """,
        expected_output="Resposta personalizada baseada no status do cliente (novo ou recorrente)",
        agent=agent
    )
