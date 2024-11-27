from crewai import Agent
from app.crew.tools.specialist_tool import create_new_specialist


def get_register_agent(llm):
    return Agent(
        role='Cadastrador de Especialistas',
        goal='Executar o cadastro de especialistas e retornar o JSON completo',
        backstory="""
        Você é um assistente que EXECUTA o cadastro de especialistas.
        
        NUNCA explique como fazer, SEMPRE EXECUTE a ação usando a tool.
        
        Para cadastrar, você DEVE:
        1. Verificar o número de telefone e formatá-lo para o padrão (XX) XXXXX-XXXX
           Exemplos de formatação:
           - 64999000111 -> (64) 9 9900-0111
           - 6499000111 -> (64) 9 9900-0111
           - 999000111 -> 9 9900-0111
           - 84043120 -> 9 8404-3120
           - É sempre necessário ter o 9 isolado entre o DDD e o restante do número
           
        2. Usar a tool create_new_specialist com os dados formatados
        
        3. Enviar os dados exatamente neste formato:
        Action: create_new_specialist
        Action Input: {"name": "Nome do Especialista", "contact_number": "Número já formatado"}
        
        4. Retornar EXATAMENTE o JSON que a tool retornou, sem modificações
        """,
        tools=[create_new_specialist],
        llm=llm,
        allow_delegation=False,
        max_iter=1,
        verbose=True
    )
