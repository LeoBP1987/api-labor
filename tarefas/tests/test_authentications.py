from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.contrib.auth import authenticate
from django.urls import reverse
from rest_framework import status

class AuthenticationUserTestCase(APITestCase):
    def setUp(self):
        
        self.usuario = User.objects.create_superuser(
            username = 'admin',
            password = 'admin'
        )

        self.url = reverse('Tarefas-list')

    def test_verifica_autenticacao_usuario_credenciais_corretas(self):
        'Teste que verifica autenticação de usuário com as credencias corretas'

        usuario = authenticate(username='admin', password='admin')

        self.assertTrue((usuario is not None) and (usuario.is_authenticated))

    def test_verifica_autenticacao_usuario_username_errado(self):
        'Teste que verifica autenticação de usuário com username errado'

        usuario = authenticate(username='xx', password='admin')

        self.assertFalse((usuario is not None) and (usuario.is_authenticated))

    def test_verifica_autenticacao_usuario_password_errado(self):
        'Teste que verifica autenticação de usuário com password errado'

        usuario = authenticate(username='admin', password='xx')

        self.assertFalse((usuario is not None) and (usuario.is_authenticated))

    def test_requisicao_get_autorizada(self):
        'Teste que verifica requisição GET autorizada'

        self.client.force_authenticate(self.usuario)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_requisicao_get_nao_autorizada(self):
        'Teste que verifica requisição GET não autorizada'

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)