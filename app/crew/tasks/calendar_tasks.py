from crewai import Task


def create_appointment_task(agent, specialist_id: int, service_id: int,
                            customer_id: int, start_time: str, notes: str = None):
    return Task(
        description=f"""
        EXECUTE AGORA:
        1. Verifique a disponibilidade do horário solicitado
        2. Se disponível, crie o agendamento com:
           - Especialista ID: {specialist_id}
           - Serviço ID: {service_id}
           - Cliente ID: {customer_id}
           - Horário: {start_time}
           - Observações: {notes if notes else 'Nenhuma'}
           
        IMPORTANTE:
        - Confirme que o horário está no horário comercial
        - Verifique se todos os IDs são válidos
        - Formate a resposta de maneira clara
        """,
        expected_output="Confirmação do agendamento criado",
        agent=agent
    )


def check_available_slots_task(agent, start_date: str, end_date: str,
                               specialist_id: int = None, service_id: int = None):
    return Task(
        description=f"""
        EXECUTE AGORA:
        1. Busque os horários disponíveis entre {start_date} e {end_date}
        2. Filtre por:
           - Especialista ID: {specialist_id if specialist_id else 'Todos'}
           - Serviço ID: {service_id if service_id else 'Todos'}
           
        IMPORTANTE:
        - Organize os horários por data
        - Destaque os períodos com mais opções
        - Indique claramente quando não houver disponibilidade
        """,
        expected_output="Lista organizada de horários disponíveis",
        agent=agent
    )


def check_customer_appointments_task(agent, contact: str,
                                     start_date: str, end_date: str):
    return Task(
        description=f"""
        EXECUTE AGORA:
        1. Busque os agendamentos do cliente {contact}
        2. Filtre entre {start_date} e {end_date}
        
        IMPORTANTE:
        - Organize cronologicamente
        - Destaque data, horário e serviço
        - Inclua nome do especialista
        - Indique se há observações especiais
        """,
        expected_output="Lista detalhada dos agendamentos do cliente",
        agent=agent
    )
