from django.test import TestCase
from tarefas.models import Tarefas, Repeticoes
from datetime import date

class ModelTarefasTestCase(TestCase):
    def setUp(self):
        self.tarefa = Tarefas.objects.create(
            usuario = 1,
            descricao = 'Descrição Teste',
            agendamento = date.today(),
            comentarios = 'Teste de comentário que seja maior que a descrição'
        )
    
    def tearDown(self):
        self.tarefa.delete()

    def test_verifica_atributos_modelo_tarefas(self):
        'Teste que verifica atributos do modelo Tarefas'

        self.assertEqual(self.tarefa.usuario, 1)
        self.assertEqual(self.tarefa.descricao, 'Descrição Teste')
        self.assertEqual(self.tarefa.agendamento, date.today())
        self.assertEqual(self.tarefa.comentarios, 'Teste de comentário que seja maior que a descrição')

class ModelRepeticoesTestCase(TestCase):
    def setUp(self):
        self.repeticao = Repeticoes.objects.create(
            usuario = 2,
            descricao = 'Descrição de repetição teste',
            repeticoes = [0,1,4,5]
        )
    
    def tearDown(self):
        self.repeticao.delete()

    def test_verifica_atributos_modelo_repeticoes(self):
        'Teste que verifica atributos do modelo Repeticoes'

        self.assertEqual(self.repeticao.usuario, 2)
        self.assertEqual(self.repeticao.descricao, 'Descrição de repetição teste')
        self.assertEqual(self.repeticao.repeticoes[2], 4)
        self.assertEqual(self.repeticao.repeticoes, [0,1,4,5])