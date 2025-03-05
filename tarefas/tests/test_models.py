from mongoengine import connect, disconnect, get_connection
from django.test import TestCase
from tarefas.models import Tarefas, Repeticoes, Dia, Semana
from datetime import date
import os

class ModelTarefasTestCase(TestCase):
    def setUp(self):
        self.mongo_bd_teste = os.getenv('MONGOTESTE_BD')
        disconnect()
        connect(db=self.mongo_bd_teste, host=os.getenv('MONGOTESTE_HOST'), port=27017)

        self.tarefa = Tarefas.objects.create(
            usuario = 1,
            descricao = 'Descrição Teste',
            agendamento = date.today(),
            comentarios = 'Teste de comentário que seja maior que a descrição'
        )
    
    def tearDown(self):
        connection = get_connection()
        connection.drop_database(self.mongo_bd_teste)
        disconnect()
        connect(db=os.getenv('BD') ,host=os.getenv('HOST'))

    def test_verifica_atributos_modelo_tarefas(self):
        'Teste que verifica atributos do modelo Tarefas'

        self.assertEqual(self.tarefa.usuario, 1)
        self.assertEqual(self.tarefa.descricao, 'Descrição Teste')
        self.assertEqual(self.tarefa.agendamento, date.today())
        self.assertEqual(self.tarefa.comentarios, 'Teste de comentário que seja maior que a descrição')

class ModelRepeticoesTestCase(TestCase):
    def setUp(self):
        self.mongo_bd_teste = os.getenv('MONGOTESTE_BD')
        disconnect()
        connect(db=self.mongo_bd_teste, host=os.getenv('MONGOTESTE_HOST'), port=27017)

        self.repeticao = Repeticoes.objects.create(
            usuario = 2,
            descricao = 'Descrição de repetição teste',
            repeticoes = [0,1,4,5]
        )
    
    def tearDown(self):
        connection = get_connection()
        connection.drop_database(self.mongo_bd_teste)
        disconnect()
        connect(db=os.getenv('BD') ,host=os.getenv('HOST'))

    def test_verifica_atributos_modelo_repeticoes(self):
        'Teste que verifica atributos do modelo Repeticoes'

        self.assertEqual(self.repeticao.usuario, 2)
        self.assertEqual(self.repeticao.descricao, 'Descrição de repetição teste')
        self.assertEqual(self.repeticao.repeticoes[2], 4)
        self.assertEqual(self.repeticao.repeticoes, [0,1,4,5])

class ModelSemanaTestCase(TestCase):
    def setUp(self):
        self.mongo_bd_teste = os.getenv('MONGOTESTE_BD')
        disconnect()
        connect(db=self.mongo_bd_teste, host=os.getenv('MONGOTESTE_HOST'), port=27017)

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

        self.semana = Semana.objects.create(
            usuario = 1,
            indicador = 'A',
            segunda = '2025-03-03',
            terca = '2025-03-04',
            quarta = '2025-03-05',
            quinta = '2025-03-06',
            sexta = '2025-03-07',
            sabado = '2025-03-08',
            domingo = '2025-03-09'
        )
    
    def tearDown(self):
        connection = get_connection()
        connection.drop_database(self.mongo_bd_teste)
        disconnect()
        connect(db=os.getenv('BD') ,host=os.getenv('HOST'))

    def test_verifica_atributos_modelo_semana(self):
        'Teste que verifica atributos do modelo Semana'

        self.assertEqual(self.semana.usuario, 1)
        self.assertEqual(self.semana.indicador, 'A')
        self.assertEqual(self.semana.segunda, self.dia)
        self.assertEqual(self.semana.terca, self.dia_2)
        self.assertEqual(self.semana.quarta, self.dia_3)
        self.assertEqual(self.semana.quinta, self.dia)
        self.assertEqual(self.semana.sexta, self.dia_2)
        self.assertEqual(self.semana.sabado, self.dia_3)
        self.assertEqual(self.semana.domingo, self.dia)