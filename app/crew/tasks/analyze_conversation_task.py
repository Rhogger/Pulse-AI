from crewai import Task
from textwrap import dedent
from typing import List, Dict


def analyze_conversation_task(agent, messages: List[Dict], customer_status: str) -> Task:
    conversation = "\n".join([
        f"[{msg.get('created_at', '')}]: {msg.get('content', '')}"
        for msg in messages
    ])

    return Task(
        description=dedent(f"""
            Analise a seguinte conversa e identifique APENAS a intenção principal do cliente, 
            respondendo com UMA ÚNICA PALAVRA conforme as regras abaixo:

            CONVERSA:
            {conversation}

            REGRAS DE CLASSIFICAÇÃO:
            - "recepcao": quando o cliente está apenas sendo cordial (bom dia, boa tarde, boa noite, olá)
            - "especialista": quando busca informações sobre especialistas
            - "servico": quando busca informações sobre serviços oferecidos
            - "agendamento": quando quer marcar, remarcar ou cancelar horários

            IMPORTANTE:
            - Responda APENAS com uma das palavras acima
            - Não adicione pontuação ou explicações
            - Priorize as mensagens mais recentes
            - Em caso de dúvida entre categorias, priorize na ordem: agendamento > servico > especialista > recepcao
            
            EXEMPLOS:
            - "Bom dia" -> recepcao
            - "Quais especialistas atendem?" -> especialista
            - "Que tipos de terapia vocês fazem?" -> servico
            - "Quero marcar um horário" -> agendamento
        """),
        expected_output="Uma única palavra indicando a intenção: recepcao, especialista, servico ou agendamento",
        agent=agent
    )
