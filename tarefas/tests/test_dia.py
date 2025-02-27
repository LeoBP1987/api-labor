from rest_framework import status
from rest_framework.test import APITestCase
from mongoengine import connect, disconnect, get_connection
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from tarefas.models import Tarefas, Dia
from tarefas.serializers import DiaSerializers
import os

def trocaParaBancoTeste():
    disconnect()
    connect(db= os.getenv('MONGOTESTE_BD'), host=os.getenv('MONGOTESTE_HOST'))

def trocaParaBancoDev():
    disconnect()
    connect(db=os.getenv('BD') ,host=os.getenv('HOST'))

trocaParaBancoTeste()

class DiaTestCase(APITestCase):
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
        self.url = reverse('Dia-list')
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

    def test_verifica_requisicao_get_list_dia(self):
        'Teste que verifica requisição GET para a lista dia'

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verifica_requisicao_get_para_uma_dia(self):
        'Teste que verifica requisição GET para uma Dia'

        response = self.client.get(f'{self.url}{self.dia.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dados_dia = self.dia
        dados_serializados = DiaSerializers(dados_dia).data

        self.assertEqual(response.data['id'], dados_serializados['id'])
        self.assertEqual(response.data['usuario'], dados_serializados['usuario'])
        self.assertEqual(response.data['dia'], dados_serializados['dia'])
        self.assertEqual(response.data['tarefas'], dados_serializados['tarefas'])

    def test_verifica_requisicao_post_um_dia(self):
        'Teste que verifica requisição POST para um dia'

        dados = {
            "usuario": 1,
            "dia": date.today(),
            "tarefas": [self.tarefa.id, self.tarefa_2.id]
        }        

        response = self.client.post(self.url, data=dados)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_verifica_requisicao_delete_um_dia(self):
        '''Teste que verifica requisição DELETE para um Dia'''

        response = self.client.delete(f'{self.url}{self.dia.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_verifica_requisicao_put_um_dia(self):
        '''Teste que verifica requisição PUT para um Dia'''

        dados = {
            "usuario": 1,
            "dia": date.today(),
            "tarefas": []
        }

        response = self.client.put(f'{self.url}{self.dia.id}/', data=dados)

        self.assertEqual(response.status_code, status.HTTP_200_OK)