from tarefas.models import Tarefas, Repeticoes, Dia, Semana
import django_mongoengine_filter as filters

class TarefasFilter(filters.FilterSet):
    usuario = filters.NumberFilter(field_name='usuario', lookup_expr='exact')
    descricao = filters.StringFilter(field_name='descricao', lookup_expr='icontains')
    agendamento = filters.DateFilter(field_name='agendamento', lookup_expr='exact')
    agendamento_range = filters.DateRangeFilter(field_name='agendamento')

    class Meta:
        model = Tarefas
        fields = ['usuario', 'descricao', 'agendamento', 'agendamento_range']

class RepeticoesFilter(filters.FilterSet):
    usuario = filters.NumberFilter(field_name='usuario', lookup_expr='exact')
    descricao = filters.StringFilter(field_name='descricao', lookup_expr='icontains')

    class Meta:
        model = Repeticoes
        fields = ['usuario', 'descricao']

class DiaFilter(filters.FilterSet):
    usuario = filters.NumberFilter(field_name='usuario', lookup_expr='exact')
    dia = filters.DateFilter(field_name='dia', lookup_expr='exact')

    class Meta:
        model = Dia
        fields = ['usuario', 'dia']

class SemanaFilter(filters.FilterSet):
    usuario = filters.NumberFilter(field_name='usuario', lookup_expr='exact')
    indicador = filters.ChoiceFilter(field_name='indicador', choices=[('A', 'A'), ('B', 'B')]) 

    class Meta:
        model = Semana
        fields = ['usuario', 'indicador']