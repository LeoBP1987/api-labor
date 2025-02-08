from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from tarefas.models import Repeticoes
from tarefas.serializers import RepeticoesAdmSerializers

class RepeticoesAdmTestCade(APITestCase):
    def setUp(self):
        self.usuario = self.usuario = User.objects.create_superuser(
            username = 'admin',
            password = 'admin'
        )
        self.url = reverse('Repeticoes-list')
        self.client.force_authenticate(self.usuario)

        self.repeticao = Repeticoes.objects.create(
            usuario = 2,
            descricao = 'Descrição de repetição teste',
            repeticoes = [0,1,4,5]
        )
        
        self.repeticao_2 = Repeticoes.objects.create(
            usuario = 1,
            descricao = 'Descrição de de teste de repetição',
            repeticoes = [7]
        )

    def tearDown(self):
        self.repeticao.delete()
        self.repeticao_2.delete()

    def test_verifica_requisicao_get_list_repeticoes(self):
        'Teste que verifica requisição GET para a lista Repeticoes'

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verifica_requisicao_get_para_uma_repeticao(self):
        'Teste que verifica requisição GET para uma repeticao'

        response = self.client.get(f'{self.url}{self.repeticao.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dados_repeticao = self.repeticao
        dados_serializados = RepeticoesAdmSerializers(dados_repeticao).data

        self.assertEqual(response.data['id'], dados_serializados['id'])
        self.assertEqual(response.data['usuario'], dados_serializados['usuario'])
        self.assertEqual(response.data['descricao'], dados_serializados['descricao'])
        self.assertEqual(response.data['repeticoes'], dados_serializados['repeticoes'])

    def test_verifica_requisicao_post_uma_repeticao(self):
        'Teste que verifica requisição POST para uma repeticao'

        dados = {
            "usuario": 1,
            "descricao": "Teste de descrição de repeticao",
            "repeticoes": [2,5,6]
        }        

        response = self.client.post(self.url, data=dados)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_verifica_requisicao_post_multiplas_repeticaos(self):
        'Teste que verifica requisição POST para múltiplas repeticoes'

        dados = [ 
                  {
                     "usuario": 1,
                     "descricao": "Teste de descrição de repeticao",
                     "repeticoes": [2,5,6] 
                  },
                  {
                     "usuario": 2,
                      "descricao": "Teste de descrição 2",
                      "repeticoes": [7] 
                  },
                  {
                     "usuario": 1,
                      "descricao": "Teste de descrição 3",
                      "repeticoes": [1,3] 
                  }
                ]         

        response = self.client.post(
                                    self.url, 
                                    data=dados,
                                    format='json'
                                )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_verifica_requisicao_delete_uma_repeticao(self):
        '''Teste que verifica requisição DELETE para uma repeticao'''

        response = self.client.delete(f'{self.url}{self.repeticao.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_verifica_requisicao_delete_multiplas_repeticaos(self):
        '''Teste que verifica requisição DELETE para multiplas repeticaos'''

        dados = [
            str(self.repeticao.id),
            str(self.repeticao_2.id)
        ]

        response = self.client.delete(
                                      reverse('Tarefas-bulk-delete'),
                                      dados,
                                      format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_verifica_requisicao_put_uma_repeticao(self):
        '''Teste que verifica requisição PUT para uma repeticao'''

        dados = {
            "usuario": 1,
            "descricao": 'Teste de atualização',
            "repeticoes": [7]
        }

        response = self.client.put(f'{self.url}{self.repeticao.id}/', data=dados)

        self.assertEqual(response.status_code, status.HTTP_200_OK)