from rest_framework_mongoengine import serializers
from tarefas.models import Tarefas, Repeticoes
from tarefas.validators import repeticoes_invalida

class TarefasAdmSerializers(serializers.DocumentSerializer):
    class Meta:
        model = Tarefas
        fields = ('id', 'usuario', 'descricao', 'agendamento', 'comentarios' )

class RepeticoesAdmSerializers(serializers.DocumentSerializer):
    class Meta:
        model = Repeticoes
        fields = ('id', 'usuario', 'descricao', 'repeticoes')

    def validate(self, dados):
        try:
            if repeticoes_invalida(dados['repeticoes']):
                raise serializers.ValidationError({'repeticoes':'A sequência de repetição é inválida.'})
        except:
            return dados
        
        return dados

class TarefasAdmSemAgendamentoSerializers(serializers.DocumentSerializer):
    class Meta:
        model = Tarefas
        fields = ('id', 'usuario', 'descricao', 'comentarios' )

class TarefasAdmPorDataSerializers(serializers.DocumentSerializer):
    class Meta:
        model = Tarefas
        fields = ('id', 'usuario', 'descricao', 'agendamento', 'comentarios' )

class TarefasPorUsuarioSerializers(serializers.DocumentSerializer):
    class Meta:
        model = Tarefas
        fields = ('id', 'usuario', 'descricao', 'agendamento', 'comentarios' )

class RepeticoesPorUsuarioSerializers(serializers.DocumentSerializer):
    class Meta:
        model = Repeticoes
        fields = ('id', 'usuario', 'descricao', 'repeticoes')

class TarefasPorUsuarioSemAgendamentoSerializers(serializers.DocumentSerializer):
    class Meta:
        model = Tarefas
        fields = ('id', 'usuario', 'descricao', 'comentarios' )

class TarefasPorUsuarioPorDataSerializers(serializers.DocumentSerializer):
    class Meta:
        model = Tarefas
        fields = ('id', 'usuario', 'descricao', 'agendamento', 'comentarios' )