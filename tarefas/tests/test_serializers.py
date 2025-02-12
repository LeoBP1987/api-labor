from django.test import TestCase
from datetime import date
from tarefas.models import Tarefas, Repeticoes
from tarefas.serializers import TarefasAdmSerializers, RepeticoesAdmSerializers, TarefasAdmSemAgendamentoSerializers, \
                                TarefasAdmPorDataSerializers, TarefasPorUsuarioSerializers, RepeticoesPorUsuarioSerializers, \
                                TarefasPorUsuarioSemAgendamentoSerializers, TarefasPorUsuarioPorDataSerializers

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

class SerializerTarefasAdmTestCase(TestCase):
    def setUp(self):
        self.tarefa = gerar_tarefa()
        self.tarefa.serializers = TarefasAdmSerializers(instance=self.tarefa)

    def tearDown(self):
        self.tarefa.delete()

    def test_verifica_campos_serializados_de_tarefas(self):
        'Teste que verifica os campos serializados do serializer TarefasAdm'

        dados = self.tarefa.serializers.data

        self.assertEqual(set(dados.keys()), set(['id','usuario', 'descricao', 'agendamento', 'comentarios']))

    def test_verifica_conteudos_serializados_de_tarefas(self):
        'Teste que verifica o conteudo dos campos serializados do serializer TarefasAdm'

        dados = self.tarefa.serializers.data

        self.assertEqual(str(dados['id']), str(self.tarefa.id))
        self.assertEqual(dados['usuario'], self.tarefa.usuario)
        self.assertEqual(dados['descricao'], self.tarefa.descricao)
        self.assertEqual(dados['agendamento'], self.tarefa.agendamento)
        self.assertEqual(dados['comentarios'], self.tarefa.comentarios)

class SerializerRepeticoesAdmTestCase(TestCase):
    def setUp(self):
        self.repeticao = gerar_repeticao()
        self.repeticao.serializers = RepeticoesAdmSerializers(instance=self.repeticao)
    
    def tearDown(self):
        self.repeticao.delete()

    def test_verifica_campos_serializados_de_repeticoes(self):
        'Teste que verifica os campos serializados do serializer RepeticoesAdm'

        dados = self.repeticao.serializers.data

        self.assertEqual(set(dados.keys()), set(['id','usuario', 'descricao', 'repeticoes']))

    def test_verifica_conteudos_serializados_de_repeticoes(self):
        'Teste que verifica o conteudo dos campos serializados do serializer RepeticoesAdm'

        dados = self.repeticao.serializers.data

        self.assertEqual(str(dados['id']), str(self.repeticao.id))
        self.assertEqual(dados['usuario'], self.repeticao.usuario)
        self.assertEqual(dados['descricao'], self.repeticao.descricao)
        self.assertEqual(dados['repeticoes'], self.repeticao.repeticoes)

class SerializerTarefasAdmSemAgendamentoTestCase(TestCase):
    def setUp(self):
        self.tarefa = gerar_tarefa()
        self.tarefa.serializer = TarefasAdmSemAgendamentoSerializers(instance=self.tarefa)

    def tearDown(self):
        self.tarefa.delete()

    def test_verifica_campos_serializados_de_tarefa_sem_agendamento(self):
        'Teste que verifica os campos serializados do serializer TarefasAdmSemAgendamento'

        dados = self.tarefa.serializer.data

        self.assertEqual(set(dados.keys()), set(['id', 'usuario', 'descricao', 'comentarios']))

    def test_verifica_conteudo_serializado_de_tarefa_sem_agendamento(self):
        'Teste que verifica o conteúdo serializado do serializer TarefasAdmSemAgendamento'

        dados = self.tarefa.serializer.data

        self.assertEqual(str(dados['id']), str(self.tarefa.id))
        self.assertEqual(dados['usuario'], self.tarefa.usuario)
        self.assertEqual(dados['descricao'], self.tarefa.descricao)
        self.assertEqual(dados['comentarios'], self.tarefa.comentarios)

class SerializerTarefasAdmPorDataTestCase(TestCase):
    def setUp(self):
        self.tarefa = gerar_tarefa()
        self.tarefa.serializer = TarefasAdmPorDataSerializers(instance=self.tarefa)

    def tearDown(self):
        self.tarefa.delete()

    def test_verifica_campos_serializados_de_tarefa_por_data(self):
        'Teste que verifica os campos serializados do serializer TarefasAdmPorData'

        dados = self.tarefa.serializer.data

        self.assertEqual(set(dados.keys()), set(['id', 'usuario', 'descricao', 'agendamento', 'comentarios']))

    def test_verifica_conteudo_serializado_de_tarefa_por_data(self):
        'Teste que verifica o conteúdo serializado do serializer TarefasAdmPorData'

        dados = self.tarefa.serializer.data

        self.assertEqual(str(dados['id']), str(self.tarefa.id))
        self.assertEqual(dados['usuario'], self.tarefa.usuario)
        self.assertEqual(dados['descricao'], self.tarefa.descricao)
        self.assertEqual(dados['agendamento'], self.tarefa.agendamento)
        self.assertEqual(dados['comentarios'], self.tarefa.comentarios)

class SerializerTarefasPorUsuarioTestCase(TestCase):
    def setUp(self):
        self.tarefa = gerar_tarefa()
        self.tarefa.serializers = TarefasPorUsuarioSerializers(instance=self.tarefa)

    def tearDown(self):
        self.tarefa.delete()

    def test_verifica_campos_serializados_de_tarefas_por_usuario(self):
        'Teste que verifica os campos serializados do serializer TarefasAdmPorUsuario'

        dados = self.tarefa.serializers.data

        self.assertEqual(set(dados.keys()), set(['id','usuario', 'descricao', 'agendamento', 'comentarios']))

    def test_verifica_conteudos_serializados_de_tarefas_por_usuario(self):
        'Teste que verifica o conteudo dos campos serializados do serializer TarefasAdmPorUsuario'

        dados = self.tarefa.serializers.data

        self.assertEqual(str(dados['id']), str(self.tarefa.id))
        self.assertEqual(dados['usuario'], self.tarefa.usuario)
        self.assertEqual(dados['descricao'], self.tarefa.descricao)
        self.assertEqual(dados['agendamento'], self.tarefa.agendamento)
        self.assertEqual(dados['comentarios'], self.tarefa.comentarios)

class SerializerRepeticoesPorUsuarioTestCase(TestCase):
    def setUp(self):
        self.repeticao = gerar_repeticao()
        self.repeticao.serializers = RepeticoesPorUsuarioSerializers(instance=self.repeticao)
    
    def tearDown(self):
        self.repeticao.delete()

    def test_verifica_campos_serializados_de_repeticoes_por_usuario(self):
        'Teste que verifica os campos serializados do serializer RepeticoesPorUsuario'

        dados = self.repeticao.serializers.data

        self.assertEqual(set(dados.keys()), set(['id','usuario', 'descricao', 'repeticoes']))

    def test_verifica_conteudos_serializados_de_repeticoes_por_usuario(self):
        'Teste que verifica o conteudo dos campos serializados do serializer RepeticoesPorUsuario'

        dados = self.repeticao.serializers.data

        self.assertEqual(str(dados['id']), str(self.repeticao.id))
        self.assertEqual(dados['usuario'], self.repeticao.usuario)
        self.assertEqual(dados['descricao'], self.repeticao.descricao)
        self.assertEqual(dados['repeticoes'], self.repeticao.repeticoes)

class SerializerTarefasPorUsuarioSemAgendamentoTestCase(TestCase):
    def setUp(self):
        self.tarefa = gerar_tarefa()
        self.tarefa.serializer = TarefasPorUsuarioSemAgendamentoSerializers(instance=self.tarefa)

    def tearDown(self):
        self.tarefa.delete()

    def test_verifica_campos_serializados_de_tarefa_sem_agendamento_por_usuario(self):
        'Teste que verifica os campos serializados do serializer TarefasPorUsuarioSemAgendamento'

        dados = self.tarefa.serializer.data

        self.assertEqual(set(dados.keys()), set(['id', 'usuario', 'descricao', 'comentarios']))

    def test_verifica_conteudo_serializado_de_tarefa_sem_agendamento_por_usuario(self):
        'Teste que verifica o conteúdo serializado do serializer TarefasPorUsuarioSemAgendamento'

        dados = self.tarefa.serializer.data

        self.assertEqual(str(dados['id']), str(self.tarefa.id))
        self.assertEqual(dados['usuario'], self.tarefa.usuario)
        self.assertEqual(dados['descricao'], self.tarefa.descricao)
        self.assertEqual(dados['comentarios'], self.tarefa.comentarios)

class SerializerTarefasPorUsuarioPorDataTestCase(TestCase):
    def setUp(self):
        self.tarefa = gerar_tarefa()
        self.tarefa.serializer = TarefasPorUsuarioPorDataSerializers(instance=self.tarefa)

    def tearDown(self):
        self.tarefa.delete()

    def test_verifica_campos_serializados_de_tarefa_por_data_por_usuario(self):
        'Teste que verifica os campos serializados do serializer TarefasPorUsuarioPorData'

        dados = self.tarefa.serializer.data

        self.assertEqual(set(dados.keys()), set(['id', 'usuario', 'descricao', 'agendamento', 'comentarios']))

    def test_verifica_conteudo_serializado_de_tarefa_por_data_por_usuario(self):
        'Teste que verifica o conteúdo serializado do serializer TarefasPorUsuarioPorData'

        dados = self.tarefa.serializer.data

        self.assertEqual(str(dados['id']), str(self.tarefa.id))
        self.assertEqual(dados['usuario'], self.tarefa.usuario)
        self.assertEqual(dados['descricao'], self.tarefa.descricao)
        self.assertEqual(dados['agendamento'], self.tarefa.agendamento)
        self.assertEqual(dados['comentarios'], self.tarefa.comentarios)