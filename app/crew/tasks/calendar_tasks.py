from crewai import Task


def process_calendar_request(agent, request_message: str, current_datetime: str):
    return Task(
        description=f"""
        ANALISE E EXECUTE A SEGUINTE SOLICITAÇÃO:
        "{request_message}"
        
        CONTEXTO TEMPORAL:
        Momento atual: {current_datetime}
        
        IMPORTANTE:
        1. Identifique a intenção do cliente (agendar, cancelar, consultar horários, etc)
        2. Extraia todas as informações relevantes da mensagem
        3. Valide TODAS as informações antes de executar qualquer ação:
           - Especialista foi informado?
           - Serviço foi especificado?
           - Data/hora é posterior ao momento atual?
           - Horário está dentro do período comercial?
        4. Use linguagem natural e cordial na resposta
        
        REGRAS DE VALIDAÇÃO:
        - Se faltar especialista ou serviço, solicite a informação ao cliente
        - Se a data/hora for anterior ao momento atual, informe o erro e sugira horários futuros
        - Se o horário estiver fora do período comercial (8h-12h e 14h-18h), sugira horários disponíveis
        - Sempre confirme disponibilidade antes de agendar
        
        FORMATO DA RESPOSTA:
        - Use linguagem natural e cordial
        - Formate datas de forma amigável (exemplo: "quarta-feira, 15 de março às 14h")
        - Nunca exponha informações técnicas ou IDs
        - Em caso de dúvidas ou falta de informações, faça perguntas claras e objetivas
        """,
        expected_output="Resposta em linguagem natural para a solicitação do cliente",
        agent=agent
    )
