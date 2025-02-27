from rest_framework import serializers as drf_serializers
from rest_framework_mongoengine import serializers
from django.contrib.auth.models import User
from tarefas.models import Tarefas, Repeticoes, Dia, Semana
from tarefas.validators import repeticoes_invalida

class TarefasSerializers(serializers.DocumentSerializer):
    class Meta:
        model = Tarefas
        fields = ('id', 'usuario', 'descricao', 'agendamento', 'comentarios' )

class RepeticoesSerializers(serializers.DocumentSerializer):
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

class DiaSerializers(serializers.DocumentSerializer):
    class Meta:
        model = Dia
        fields = ('id', 'usuario', 'dia', 'tarefas')

class SemanaSerializers(serializers.DocumentSerializer):
    class Meta:
        model = Semana
        fields = ('id', 'usuario', 'indicador', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo')