from crewai import Task
from textwrap import dedent
from typing import List, Dict


def analyze_conversation_task(agent, messages: List[Dict], customer_status: str) -> Task:
    # Formata as mensagens para análise
    conversation = "\n".join([
        f"[{msg.get('created_at', '')}]: {msg.get('content', '')}"
        for msg in messages
    ])

    return Task(
        description=dedent(f"""
            Analise a seguinte conversa e crie um resumo estruturado:

            {conversation}

            Seu resumo deve conter:

            - Qual a principal solicitação/necessidade do cliente
            - Serviço(s) mencionado(s) (se mencionado)
            - Preferência de horário (se mencionada)
            - Preferência de especialista (se mencionada)

            Mantenha o resumo conciso e focado nas informações relevantes para o agendamento.
            
            IMPORTANTE:
            - Mantenha o foco nas mensagens mais recentes
            - Ignore informações antigas ou fora de contexto
            - Seja direto e objetivo
            - Priorize informações úteis
            - SEMPRE responda em português brasileiro
            - Não responda em markdown
            - Saiba diferenciar um cliente novo de um cliente cadastrado (o cliente é {customer_status})
            
            Exemplo de respostas: 
            - A principa intenção do cliente é agendar uma consulta, sem preferência de especialista e horário e nenhum serviço foi mencionado
            - O cliente está procurando informações sobre os serviços oferecidos
            - O cliente está procurando um especialista em cardiologia
            - O cliente está procurando um horário para uma consulta com o especialista em cardiologia
            - O cliente está procurando informações sobre os serviços oferecidos e gostaria de agendar uma consulta para o dia 10/02/2024
        """),
        expected_output="Resumo estruturado da conversa com informações relevantes para agendamento",
        agent=agent,
    )
