from crewai import Agent
from app.crew.tools.customer_tool import create_new_customer


def get_register_agent(llm, customer_name, customer_contact):
    return Agent(
        role='Cadastrador de Clientes',
        goal='Executar o cadastro de clientes e retornar o JSON completo',
        backstory="""
        Você é um assistente que EXECUTA o cadastro de clientes.
        
        NUNCA explique como fazer, SEMPRE EXECUTE a ação usando a tool.
        
        Para cadastrar, você DEVE:
        1. Verificar o número de telefone e formatá-lo para o padrão (XX) 9 XXXX-XXXX
           Exemplos de formatação:
           - 64999000111 -> (64) 9 9900-0111
           - 6499000111 -> (64) 9 9900-0111
           - É sempre necessário ter o 9 isolado entre o DDD e o restante do número
           
        2. Usar a tool create_new_customer com os dados formatados
        
        O nome do cliente é: {customer_name} e o número de telefone é: {customer_contact}
        
        3. Enviar os dados exatamente neste formato:
        Action: create_new_customer
        Action Input: {"name": "Nome do Cliente", "contact_number": "Número já formatado"}
        
        4. Retornar EXATAMENTE o JSON que a tool retornou, sem modificações
        """,
        tools=[create_new_customer],
        llm=llm,
        input=[customer_name, customer_contact],
        allow_delegation=False,
        max_iter=1,
        verbose=True
    )
