from rest_framework import filters, pagination, status
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets
from rest_framework.decorators import action
from tarefas.models import Tarefas, Repeticoes, Dia, Semana
from tarefas.serializers import TarefasSerializers, RepeticoesSerializers, DiaSerializers, SemanaSerializers
from tarefas.filters import TarefasFilter, RepeticoesFilter, DiaFilter, SemanaFilter

class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = page_size
    max_page_size = 100

class TarefasViewSets(viewsets.ModelViewSet):
   
    queryset = Tarefas.objects.all().order_by('usuario')
    serializer_class = TarefasSerializers
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['usuario', 'descricao', 'agendamento']
    ordering_fields = ['usuario', ]
    searching_fields = ['usuario' ,'descricao', 'agendamento', ]
    filter_class = TarefasFilter
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
    filter_class = RepeticoesFilter
    pagination_class = CustomPagination

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

class DiaViewSet(viewsets.ModelViewSet):
    queryset = Dia.objects.all().order_by('usuario')
    serializer_class = DiaSerializers
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['usuario', ]
    filterset_fields = ['usuario', 'dia']
    searching_fields = ['usuario' ,'dia' ]
    filter_class = DiaFilter
    pagination_class = CustomPagination

class SemanaViewSet(viewsets.ModelViewSet):
    queryset = Semana.objects.all().order_by('usuario')
    serializer_class = SemanaSerializers
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['usuario', ]
    filterset_fields = ['usuario', 'indicador', 'dia']
    searching_fields = ['usuario' ,'dia' ]
    filter_class = SemanaFilter
    pagination_class = CustomPagination
    