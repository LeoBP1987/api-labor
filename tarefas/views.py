from rest_framework import filters, pagination, status
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets, generics
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
from tarefas.models import Tarefas, Repeticoes
from tarefas.serializers import TarefasAdmSerializers, RepeticoesAdmSerializers, TarefasAdmSemAgendamentoSerializers, \
                                TarefasAdmPorDataSerializers, TarefasPorUsuarioSerializers, RepeticoesPorUsuarioSerializers, \
                                    TarefasPorUsuarioSemAgendamentoSerializers, TarefasPorUsuarioPorDataSerializers

class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = page_size
    max_page_size = 100

class TarefasAdmViewSets(viewsets.ModelViewSet):
    queryset = Tarefas.objects.all().order_by('usuario')
    serializer_class = TarefasAdmSerializers
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['usuario', ]
    searching_fields = ['usuario' ,'descricao', 'agendamento', ]
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return super().create(request, *args, **kwargs)
        
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

class RepeticoesAdmViewSets(viewsets.ModelViewSet):
    queryset = Repeticoes.objects.all().order_by('usuario')
    serializer_class = RepeticoesAdmSerializers
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['usuario', ]
    searching_fields = ['usuario' ,'descricao', 'repeticoes']
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return super().create(request, *args, **kwargs)
        
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

class TarefasAdmSemAgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Tarefas.objects.filter(agendamento="None").order_by('usuario')
    serializer_class = TarefasAdmSemAgendamentoSerializers
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['usuario']
    searching_fields = ['usuario', 'descricao', ]
    pagination_class = CustomPagination

class TarefasAdmPorDataViewSet(generics.ListAPIView):
    def get_queryset(self):

        data_str = self.kwargs['data']
        data_formatada = datetime.fromisoformat(data_str)

        queryset = Tarefas.objects.filter(agendamento=data_formatada).order_by('usuario')
        return queryset
    
    serializer_class = TarefasAdmPorDataSerializers

class TarefasPorUsuarioViewSet(generics.ListAPIView):
    def get_queryset(self): 

        queryset = Tarefas.objects.filter(usuario=self.kwargs['id']).order_by('descricao')
        return queryset
    
    serializer_class = TarefasPorUsuarioSerializers
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['descricao']
    searching_fields = ['descricao', 'agendamento']
    pagination_class = CustomPagination
       

class RepeticoesPorUsuarioViewSet(generics.ListAPIView):
    def get_queryset(self):
        queryset = Repeticoes.objects.filter(usuario=self.kwargs['id']).order_by('descricao')
        return queryset
    
    serializer_class = RepeticoesPorUsuarioSerializers
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['descricao']
    searching_fields = ['descricao', 'repeticoes']
    pagination_class = CustomPagination
    
class TarefasPorUsuarioSemAgendamentoViewSet(generics.ListAPIView):
    def get_queryset(self):
        queryset = Tarefas.objects.filter(usuario=self.kwargs['id']).filter(agendamento=None).order_by('descricao')
        return queryset
    
    serializer_class = TarefasPorUsuarioSemAgendamentoSerializers
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['descricao']
    searching_fields = ['descricao', ]
    pagination_class = CustomPagination

class TarefasPorUsuarioPorDataViewSet(generics.ListAPIView):
    def get_queryset(self):

        data_str = self.kwargs['data']
        data_formatada = datetime.fromisoformat(data_str)

        queryset = Tarefas.objects.filter(usuario=self.kwargs['id'], agendamento=data_formatada).order_by('descricao')
        return queryset
    
    serializer_class = TarefasPorUsuarioPorDataSerializers
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['descricao']
    searching_fields = ['descricao', 'agendamento']
    pagination_class = CustomPagination