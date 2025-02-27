from rest_framework import status
from rest_framework.test import APITestCase
from mongoengine import connect, disconnect, get_connection
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from tarefas.models import Tarefas, Dia, Semana
from tarefas.serializers import SemanaSerializers
import os

def trocaParaBancoTeste():
    disconnect()
    connect(db= os.getenv('MONGOTESTE_BD'), host=os.getenv('MONGOTESTE_HOST'))

def trocaParaBancoDev():
    disconnect()
    connect(db=os.getenv('BD') ,host=os.getenv('HOST'))

trocaParaBancoTeste()

class SemanaTestCase(APITestCase):
    @classmethod
    def tearDownClass(cls):
        connection = get_connection()
        connection.drop_database(os.getenv('MONGOTESTE_BD'))
        trocaParaBancoDev()

        return super().tearDownClass()

    def setUp(self):
        
        self.usuario = self.usuario = User.objects.create_superuser(
            username = 'admin',
            password = 'admin'
        )
        self.url = reverse('Semana-list')
        self.client.force_authenticate(self.usuario)

        self.tarefa = Tarefas.objects.create(
            usuario = 1,
            descricao = 'Descrição Teste',
            agendamento = date.today(),
            comentarios = 'Teste de comentário que seja maior que a descrição'
        )

        self.tarefa_2 = Tarefas.objects.create(
            usuario = 2,
            descricao = 'Descrição Teste 2',
            agendamento = date.today(),
            comentarios = 'Teste de comentário que seja maior que a descrição 2'
        )

        self.dia = Dia.objects.create(
            usuario = 1,
            dia = date.today(),
            tarefas = [self.tarefa, self.tarefa_2]
        )

        self.dia_2 = Dia.objects.create(
            usuario = 1,
            dia = date.today(),
            tarefas = [self.tarefa_2]
        )

        self.dia_3 = Dia.objects.create(
            usuario = 1,
            dia = date.today(),
            tarefas = []
        )

        self.semana = Semana.objects.create(
            usuario = 1,
            indicador = 'A',
            segunda = self.dia,
            terca = self.dia_2,
            quarta = self.dia_3,
            quinta = self.dia,
            sexta = self.dia_2,
            sabado = self.dia_3,
            domingo = self.dia
        )
    
    def test_verifica_requisicao_get_lista_semana(self):
        'Teste que verifica requisição GET para a lista semana'

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verifica_requisicao_get_para_uma_semana(self):
        'Teste que verifica requisição GET para uma Semana'

        response = self.client.get(f'{self.url}{self.semana.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dados_semana = self.semana
        dados_serializados = SemanaSerializers(dados_semana).data

        self.assertEqual(response.data['id'], dados_serializados['id'])
        self.assertEqual(response.data['usuario'], dados_serializados['usuario'])
        self.assertEqual(response.data['indicador'], dados_serializados['indicador'])
        self.assertEqual(response.data['segunda'], dados_serializados['segunda'])
        self.assertEqual(response.data['terca'], dados_serializados['terca'])
        self.assertEqual(response.data['quarta'], dados_serializados['quarta'])
        self.assertEqual(response.data['quinta'], dados_serializados['quinta'])
        self.assertEqual(response.data['sexta'], dados_serializados['sexta'])
        self.assertEqual(response.data['sabado'], dados_serializados['sabado'])
        self.assertEqual(response.data['domingo'], dados_serializados['domingo'])

    def test_verifica_requisicao_post_uma_semana(self):
        'Teste que verifica requisição POST para um semana'

        dados = {
            "usuario": 1,
            "indicador": "A",
            "segunda": self.dia.id,
            "terca": self.dia.id,
            "quarta": self.dia.id,
            "quinta": self.dia.id,
            "sexta": self.dia.id,
            "sabado": self.dia.id,
            "domingo": self.dia.id,
        }        

        response = self.client.post(self.url, data=dados)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_verifica_requisicao_delete_uma_semana(self):
        '''Teste que verifica requisição DELETE para uma Semana'''

        response = self.client.delete(f'{self.url}{self.semana.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_verifica_requisicao_put_uma_semana(self):
        '''Teste que verifica requisição PUT para uma Semana'''

        dados = {
            "usuario": 1,
            "indicador": "B",
            "segunda": self.dia_2.id,
            "terca": self.dia_3.id,
            "quarta": self.dia_3.id,
            "quinta": self.dia_2.id,
            "sexta": self.dia_2.id,
            "sabado": self.dia_3.id,
            "domingo": self.dia_2.id,
        }

        response = self.client.put(f'{self.url}{self.semana.id}/', data=dados)

        self.assertEqual(response.status_code, status.HTTP_200_OK)