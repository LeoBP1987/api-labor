from django.test import TestCase
from mongoengine import connect, disconnect, get_connection
from datetime import date
from tarefas.models import Tarefas, Repeticoes, Dia, Semana
from tarefas.serializers import TarefasSerializers, RepeticoesSerializers, DiaSerializers, SemanaSerializers
import os

def gerar_tarefa():
    tarefa = Tarefas.objects.create(
            usuario = 1,
            descricao = 'Descrição Teste',
            agendamento = date.today().isoformat(),
            comentarios = 'Teste de comentário que seja maior que a descrição'
        )
    return tarefa

def gerar_repeticao():
    repeticao = Repeticoes.objects.create(
            usuario = 2,
            descricao = 'Descrição de repetição teste',
            repeticoes = [0,1,4,5]
        )
    return repeticao

def gerar_dia():

    tarefa = gerar_tarefa()

    dia = Dia.objects.create(
        usuario = 1,
        dia = date.today().isoformat(),
        tarefas = [tarefa]
    )
    return dia

def gerar_semana():

    dia = gerar_dia()

    semana = Semana.objects.create(
        usuario = 1,
        indicador = 'A',
        segunda = dia,
        terca = dia,
        quarta = dia,
        quinta = dia,
        sexta = dia,
        sabado = dia,
        domingo = dia
    )
    return semana

def trocaParaBancoTeste():
    disconnect()
    connect(db= os.getenv('MONGOTESTE_BD'), host=os.getenv('MONGOTESTE_HOST'))

def trocaParaBancoDev():
    disconnect()
    connect(db=os.getenv('BD') ,host=os.getenv('HOST'))

trocaParaBancoTeste()

class SerializerTarefasTestCase(TestCase):
    @classmethod
    def tearDownClass(cls):
        connection = get_connection()
        connection.drop_database(os.getenv('MONGOTESTE_BD'))

        return super().tearDownClass()

    def setUp(self):
        self.tarefa = gerar_tarefa()
        self.tarefa.serializers = TarefasSerializers(instance=self.tarefa)
    
    def test_verifica_campos_serializados_de_tarefas(self):
        'Teste que verifica os campos serializados do serializer Tarefas'

        dados = self.tarefa.serializers.data

        self.assertEqual(set(dados.keys()), set(['id','usuario', 'descricao', 'agendamento', 'comentarios']))

    def test_verifica_conteudos_serializados_de_tarefas(self):
        'Teste que verifica o conteudo dos campos serializados do serializer Tarefas'

        dados = self.tarefa.serializers.data

        self.assertEqual(str(dados['id']), str(self.tarefa.id))
        self.assertEqual(dados['usuario'], self.tarefa.usuario)
        self.assertEqual(dados['descricao'], self.tarefa.descricao)
        self.assertEqual(dados['agendamento'], self.tarefa.agendamento)
        self.assertEqual(dados['comentarios'], self.tarefa.comentarios)

class SerializerRepeticoesTestCase(TestCase):
    @classmethod
    def tearDownClass(cls):
        connection = get_connection()
        connection.drop_database(os.getenv('MONGOTESTE_BD'))
        
        return super().tearDownClass()
    
    def setUp(self):
        self.repeticao = gerar_repeticao()
        self.repeticao.serializers = RepeticoesSerializers(instance=self.repeticao)

    def test_verifica_campos_serializados_de_repeticoes(self):
        'Teste que verifica os campos serializados do serializer Repeticoes'

        dados = self.repeticao.serializers.data

        self.assertEqual(set(dados.keys()), set(['id','usuario', 'descricao', 'repeticoes']))

    def test_verifica_conteudos_serializados_de_repeticoes(self):
        'Teste que verifica o conteudo dos campos serializados do serializer Repeticoes'

        dados = self.repeticao.serializers.data

        self.assertEqual(str(dados['id']), str(self.repeticao.id))
        self.assertEqual(dados['usuario'], self.repeticao.usuario)
        self.assertEqual(dados['descricao'], self.repeticao.descricao)
        self.assertEqual(dados['repeticoes'], self.repeticao.repeticoes)

class SerializerDiaTestCase(TestCase):
    @classmethod
    def tearDownClass(cls):
        connection = get_connection()
        connection.drop_database(os.getenv('MONGOTESTE_BD'))
        
        return super().tearDownClass()
    
    def setUp(self):
        self.dia = gerar_dia()
        self.dia.serializer = DiaSerializers(self.dia)

    def test_verifica_campos_serializados_de_dia(self):
        'Teste que verifica os campos serializados do serializer DiaAdm'

        dados = self.dia.serializer.data

        self.assertEqual(set(dados.keys()), set(['id', 'usuario', 'dia', 'tarefas']))

    def test_verifica_conteudo_serializado_de_dia(self):
        'Teste que verifica o conteudo serializado do serializer Dia'

        dados = self.dia.serializer.data

        self.assertEqual(str(dados['id']), str(self.dia.id))
        self.assertEqual(dados['usuario'], self.dia.usuario)
        self.assertEqual(dados['dia'], self.dia.dia)
        self.assertEqual(str(dados['tarefas'][0]), str(self.dia.tarefas[0].id))

class SerializerSemanaTestCase(TestCase):
    @classmethod
    def tearDownClass(cls):
        connection = get_connection()
        connection.drop_database(os.getenv('MONGOTESTE_BD'))
        
        return super().tearDownClass()
    
    def setUp(self):
        self.semana = gerar_semana()
        self.semana.serializer = SemanaSerializers(self.semana)

    def test_verifica_campos_serializados_de_semana(self):
        'Teste que verifica os campos serializados do serializer Semana'

        dados = self.semana.serializer.data

        self.assertEqual(set(dados.keys()), set(['id', 'usuario', 'indicador', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo']))

    def test_verifica_conteudo_serializado_de_semana(self):
        'Teste que verifica o conteudo serializado do serializer Semana'

        dados = self.semana.serializer.data

        self.assertEqual(str(dados['id']), str(self.semana.id))
        self.assertEqual(dados['usuario'], self.semana.usuario)
        self.assertEqual(dados['indicador'], self.semana.indicador)
        self.assertEqual(dados['segunda'], str(self.semana.segunda.id))
        self.assertEqual(dados['terca'], str(self.semana.terca.id))
        self.assertEqual(dados['quarta'], str(self.semana.quarta.id))
        self.assertEqual(dados['quinta'], str(self.semana.quinta.id))
        self.assertEqual(dados['sexta'], str(self.semana.sexta.id))
        self.assertEqual(dados['sabado'], str(self.semana.sabado.id))
        self.assertEqual(dados['domingo'], str(self.semana.domingo.id))