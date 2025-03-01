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

    agendamento_range = query_params.get('agendamento_range')
    if agendamento_range:
        start_date, end_date = agendamento_range.split('__')
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        queryset = queryset.filter(agendamento__gte=start_date, agendamento__lte=end_date)

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

def DiaFilters(queryset, query_params):
    """
    Aplica filtros ao queryset de Dia com base nos parâmetros da requisição.
    """
    usuario = query_params.get('usuario')
    if usuario:
        queryset = queryset.filter(usuario=int(usuario))

    dia = query_params.get('dia')
    if dia:
        dia_date = datetime.strptime(dia, '%Y-%m-%d').date()
        queryset = queryset.filter(dia=dia_date)

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