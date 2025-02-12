from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from tarefas.models import Tarefas, Repeticoes
from tarefas.serializers import TarefasAdmSerializers

class TarefasAdmTestCade(APITestCase):
    def setUp(self):
        self.usuario = self.usuario = User.objects.create_superuser(
            username = 'admin',
            password = 'admin'
        )
        self.url = reverse('Tarefas-list')
        self.client.force_authenticate(self.usuario)

        self.tarefa = Tarefas.objects.create(
            usuario = 1,
            descricao = 'Descrição Teste',
            agendamento = date.today(),
            comentarios = 'Teste de comentários'
        )
        self.tarefa_2 = Tarefas.objects.create(
            usuario = 2,
            descricao = 'Descrição Teste de Tarefa 2',
            agendamento = date.today(),
            comentarios = 'Teste de comentários 2'
        )

    def tearDown(self):
        self.tarefa.delete()
        self.tarefa_2.delete()

    def test_verifica_requisicao_get_list_tarefas(self):
        'Teste que verifica requisição GET para a lista tarefas'

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verifica_requisicao_get_para_uma_tarefa(self):
        'Teste que verifica requisição GET para uma Tarefa'

        response = self.client.get(f'{self.url}{self.tarefa.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dados_tarefa = self.tarefa
        dados_serializados = TarefasAdmSerializers(dados_tarefa).data

        self.assertEqual(response.data['id'], dados_serializados['id'])
        self.assertEqual(response.data['usuario'], dados_serializados['usuario'])
        self.assertEqual(response.data['descricao'], dados_serializados['descricao'])
        self.assertEqual(response.data['agendamento'], dados_serializados['agendamento'])
        self.assertEqual(response.data['comentarios'], dados_serializados['comentarios'])

    def test_verifica_requisicao_post_uma_tarefa(self):
        'Teste que verifica requisição POST para uma tarefa'

        dados = {
            "usuario": 1,
            "descricao": "Teste de descrição de tarefa",
            "agendamento": date.today()
        }        

        response = self.client.post(self.url, data=dados)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_verifica_requisicao_post_multiplas_tarefas(self):
        'Teste que verifica requisição POST para múltiplas tarefas'

        dados = [ 
                  {
                     "usuario": 1,
                     "descricao": "Teste de descrição de tarefa",
                     "agendamento": date.today(),
                     "comentarios": "Teste de comentarios 1"
                  },
                  {
                     "usuario": 2,
                      "descricao": "Teste de descrição 2",
                      "agendamento": date.today(),
                      "comentarios": "Teste de comentarios 2"
                  },
                  {
                     "usuario": 1,
                      "descricao": "Teste de descrição 3",
                      "agendamento": date.today() 
                  }
                ]         

        response = self.client.post(
                                    self.url, 
                                    data=dados,
                                    format='json'
                                )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_verifica_requisicao_delete_uma_tarefa(self):
        '''Teste que verifica requisição DELETE para uma Tarefa'''

        response = self.client.delete(f'{self.url}{self.tarefa.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_verifica_requisicao_delete_multiplas_tarefas(self):
        '''Teste que verifica requisição DELETE para multiplas Tarefas'''

        dados = [
            str(self.tarefa.id),
            str(self.tarefa_2.id)
        ]

        response = self.client.delete(
                                      reverse('Tarefas-bulk-delete'),
                                      dados,
                                      format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_verifica_requisicao_put_uma_tarefa(self):
        '''Teste que verifica requisição PUT para uma Tarefa'''

        dados = {
            "usuario": 1,
            "descricao": 'Teste de atualização',
            "agendamento": date.today(),
            "comentarios": "Teste de comentarios 1"
        }

        response = self.client.put(f'{self.url}{self.tarefa.id}/', data=dados)

        self.assertEqual(response.status_code, status.HTTP_200_OK)