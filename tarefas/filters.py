from datetime import datetime

def TarefasFilters(queryset, query_params):
    """
    Aplica filtros ao queryset de Tarefas com base nos parâmetros da requisição.
    """
    usuario = query_params.get('usuario')
    if usuario:
        queryset = queryset.filter(usuario=int(usuario))

    descricao = query_params.get('descricao')
    if descricao:
        queryset = queryset.filter(descricao__icontains=descricao)

    agendamento = query_params.get('agendamento')
    if agendamento:
        agendamento_date = datetime.strptime(agendamento, '%Y-%m-%d').date()
        queryset = queryset.filter(agendamento=agendamento_date)

    agendamento = query_params.get('agendamento_lt')
    if agendamento:
        agendamento_lt = datetime.strptime(agendamento, '%Y-%m-%d').date()
        queryset = queryset.filter(agendamento__lt=agendamento_lt)

    return queryset

def RepaticoesFilters(queryset, query_params):
    """
    Aplica filtros ao queryset de Repeticoes com base nos parâmetros da requisição.
    """
    usuario = query_params.get('usuario')
    if usuario:
        queryset = queryset.filter(usuario=int(usuario))

    descricao = query_params.get('descricao')
    if descricao:
        queryset = queryset.filter(descricao__icontains=descricao)

    return queryset

def SemanaFilters(queryset, query_params):
    """
    Aplica filtros ao queryset de Semana com base nos parâmetros da requisição.
    """
    usuario = query_params.get('usuario')
    if usuario:
        queryset = queryset.filter(usuario=int(usuario))

    indicador = query_params.get('indicador')
    if indicador:
        queryset = queryset.filter(indicador=indicador)

    return queryset