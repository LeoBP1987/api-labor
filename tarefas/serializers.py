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

class UsuarioSeriliazers(drf_serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password' ,'email', 'first_name')
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
        )
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance