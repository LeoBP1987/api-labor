from rest_framework import filters, pagination, status, viewsets as drf_viewsets
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from tarefas.models import Tarefas, Repeticoes, Semana
from tarefas.serializers import TarefasSerializers, RepeticoesSerializers, SemanaSerializers, \
                                UsuarioSeriliazers
from tarefas.filters import TarefasFilters, RepaticoesFilters, DiaFilters, SemanaFilters
from datetime import datetime, timedelta
from collections import defaultdict
import os
import requests

class CustomPagination(pagination.PageNumberPagination):
    page_size = 200
    page_size_query_param = page_size

class TarefasViewSets(viewsets.ModelViewSet):

    queryset = Tarefas.objects.all().order_by('usuario')
    serializer_class = TarefasSerializers
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['agendamento', 'usuario' ]
    searching_fields = ['usuario' ,'descricao', 'agendamento', ]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Tarefas.objects.all().order_by('agendamento')
        queryset = TarefasFilters(queryset, self.request.query_params)
        return queryset

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return super().create(request, *args, **kwargs)
        
    @action(detail=False, methods=['get'], url_path='get-periodo')
    def get_periodo(self, request):
        agendamento_range = request.query_params.get('agendamento_range')
        usuario = request.query_params.get('usuario')
        lista_payload = []
        payload_agrupado = defaultdict(list)

        if agendamento_range:
            start_date, end_date = agendamento_range.split('__')
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            tarefasPeriodo = Tarefas.objects.filter(usuario=usuario, agendamento__gte=start_date, agendamento__lte=end_date)

            for tarefa in tarefasPeriodo:
                agendamento_str = tarefa.agendamento.strftime('%Y-%m-%d')
                payload_agrupado[agendamento_str].append({
                    "id": str(tarefa.id),
                    "usuario": str(tarefa.usuario),
                    "descricao": tarefa.descricao,
                    "agendamento": agendamento_str,
                    "comentarios": tarefa.comentarios if tarefa.comentarios else None
                })

            for data, tarefas in payload_agrupado.items():
                lista_payload.append({data: tarefas})

            
        return Response(lista_payload)


    @action(detail=False, methods=['patch'], url_path='bulk-update')
    def bulk_update(self, request):
        if not isinstance(request.data, list):
            return Response({"error": "Os dados devem ser enviados em uma lista"}, status=status.HTTP_400_BAD_REQUEST)
        ids = [data.get('id') for data in request.data if 'id' in data]
        if not ids:
            return Response({"error": "Nenhum ID fornecido"}, status=status.HTTP_400_BAD_REQUEST)
        objetos = Tarefas.objects.filter(id__in=ids)
        object_map = {str(obj.id): obj for obj in objetos}
        errors = []
        for data in request.data:
            obj_id = str(data.get('id'))
            if obj_id not in object_map:
                errors.append({"error": f"Objeto com ID {obj_id} não encontrado"})
                continue
            obj = object_map[obj_id]
            for key, value in data.items():
                if key != 'id':
                    if hasattr(obj, key):
                        setattr(obj, key, value)
                    else:
                        errors.append({"error": f"Campo '{key}' não existe no objeto com ID {obj_id}"})
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        for obj in object_map.values():
            obj.save()
        return Response({"message": "Atualização em lote concluída com sucesso"}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['delete'], url_path='bulk-delete')
    def bulk_delete(self, request):
        if isinstance(request.data, list):
            try:
                Tarefas.objects.filter(id__in=request.data).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Erro na lista de IDs"}, status=status.HTTP_400_BAD_REQUEST)

class RepeticoesViewSets(viewsets.ModelViewSet):
    queryset = Repeticoes.objects.all().order_by('usuario')
    serializer_class = RepeticoesSerializers
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['usuario', ]
    filterset_fields = ['usuario', 'descricao', 'repeticoes']
    searching_fields = ['usuario' ,'descricao', 'repeticoes']
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Repeticoes.objects.all().order_by('usuario')
        queryset = RepaticoesFilters(queryset, self.request.query_params)
        return queryset
    
    @action(detail=False, methods=['patch'], url_path='bulk-update')
    def bulk_update(self, request):
        if not isinstance(request.data, list):
            return Response({"error": "Os dados devem ser enviados em uma lista"}, status=status.HTTP_400_BAD_REQUEST)
        ids = [data.get('id') for data in request.data if 'id' in data]
        if not ids:
            return Response({"error": "Nenhum ID fornecido"}, status=status.HTTP_400_BAD_REQUEST)
        objetos = Repeticoes.objects.filter(id__in=ids)
        object_map = {str(obj.id): obj for obj in objetos}
        errors = []
        for data in request.data:
            obj_id = str(data.get('id'))
            if obj_id not in object_map:
                errors.append({"error": f"Objeto com ID {obj_id} não encontrado"})
                continue
            obj = object_map[obj_id]
            for key, value in data.items():
                if key != 'id':
                    if hasattr(obj, key):
                        setattr(obj, key, value)
                    else:
                        errors.append({"error": f"Campo '{key}' não existe no objeto com ID {obj_id}"})
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        for obj in object_map.values():
            obj.save()
        return Response({"message": "Atualização em lote concluída com sucesso"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], url_path='bulk-delete')
    def bulk_delete(self, request):
        if isinstance(request.data, list):
            try:
                Repeticoes.objects.filter(id__in=request.data).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Erro na lista de IDs"}, status=status.HTTP_400_BAD_REQUEST)

class SemanaViewSet(viewsets.ModelViewSet):
    queryset = Semana.objects.all().order_by('usuario')
    serializer_class = SemanaSerializers
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['usuario', ]
    filterset_fields = ['usuario', 'indicador', 'dia']
    searching_fields = ['usuario' ,'dia' ]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Semana.objects.all().order_by('usuario')
        queryset = SemanaFilters(queryset, self.request.query_params)
        return queryset

    @action(detail=False, methods=['post'], url_path='monta-semana')
    def monta_semana(self, request):
        data = request.data
        usuario = data.get('usuario')
        indicador = data.get('indicador')

        if not usuario or not indicador:
            return Response(
                {"error": "Os campos 'usuario' e 'indicador' são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        hoje = datetime.today().date()
        dia_semana = hoje.isoweekday()
        dia_map = {
            1:"segunda",
            2:"terca",
            3:"quarta",
            4:"quinta",
            5:"sexta",
            6:"sabado",
            7:"domingo" 
        }

        if indicador == 'A':
            semana_atual = Semana.objects.create(
                                                    usuario=usuario,
                                                    indicador='A'
                                                )
            ultima_segunda = dia_semana - 1
            dia_controle = hoje - timedelta(days=ultima_segunda)
            dia_semana_controle = 1
            while dia_semana_controle <= 7:
                dia = dia_controle
                campo_dia = dia_map[dia_semana_controle]
                setattr(semana_atual, campo_dia, dia)
                semana_atual.save()

                dia_controle = dia_controle + timedelta(days=1)
                dia_semana_controle += 1
            
            semana_atual_serializers = SemanaSerializers(semana_atual)
            return Response(semana_atual_serializers.data, status=status.HTTP_201_CREATED)
        
        if indicador == 'B':
            semana_seguinte = Semana.objects.create(
                                                        usuario=usuario,
                                                        indicador='B'
                                                    )
            dias_para_proxima_segunda = (7 - dia_semana) + 1
            dia_controle = hoje + timedelta(days=dias_para_proxima_segunda)

            for dia_semana in range(1, 8):
                dia = dia_controle

                campo_dia = dia_map[dia_semana]
                setattr(semana_seguinte, campo_dia, dia)
                semana_seguinte.save()

                dia_controle = dia_controle + timedelta(days=1)
            
            semana_seguinte_serializers = SemanaSerializers(semana_seguinte)
            return Response(semana_seguinte_serializers.data, status=status.HTTP_201_CREATED)


class LoginViewSet(drf_viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'], url_path='get-login')
    def oauth_login(self, request):
        data = request.data

        username = data.get('username')
        password = data.get('password')

        payload = {
            'client_id': str(os.getenv('ClientId')),
            'client_secret': str(os.getenv('ClientSecret')),
            'grant_type': 'password',
            'username': username,
            'password': password
        }

        try:
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            response = requests.post('https://api-labor-5ee8ad3cd3aa.herokuapp.com/oauth2/token/', data=payload, headers=headers)
            response.raise_for_status()
            token_data = response.json()

            try:
                user_id = User.objects.get(username=username).id
            except ObjectDoesNotExist:
                return Response({"error": "Usuário não encontrado"}, status=status.HTTP_404_NOT_FOUND)

            return Response({
                'access_token': token_data['access_token'],
                'refresh_token': token_data.get('refresh_token', ''),
                'user_id': user_id
            }, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Falha ao obter token de acesso: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
class UsuariosViewSet(drf_viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UsuarioSeriliazers
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    ordering_fields = ['username', ]
    filterset_fields = ['id', 'username', 'email']
    searching_fields = ['id', 'username', 'email']
    pagination_class = CustomPagination
    permission_classes = [AllowAny]