from crewai import Task


def welcome_customer_task(agent, initial_message: str, customer_name: str):
    return Task(
        description=f"""
        O cliente enviou a seguinte mensagem: "{initial_message}"
        Informações do cliente: {customer_name}
        
        Sua missão é:
         1. Analise as informações do cliente recebidas
         2. Se o nome do cliente foi encontrado no sistema:
           - Cumprimente usando o nome do cliente
           - Reconheça que é um cliente recorrente
           - Demonstre que valorizamos sua fidelidade
         3. Se é um novo cliente, (nome não encontrado no sistema):
           - Dê boas-vindas especiais
           - Demonstre entusiasmo em tê-lo conosco
         4. Indague o usuário sobre o que ele está procurando
        
        Importante:
        - Mantenha sempre um tom cordial e prestativo
        - Demonstre que estamos felizes em atendê-lo
        - Personalize a mensagem com base no status do cliente
        - Indague o usuário sobre o que ele está procurando
        - Responda em português brasileiro
        - Mantenha a resposta curta e objetiva
        """,
        expected_output="Resposta personalizada baseada no status do cliente (novo ou recorrente)",
        agent=agent

    )
