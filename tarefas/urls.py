from django.urls import path, include
from rest_framework_mongoengine import routers
from tarefas.views import TarefasAdmViewSets, RepeticoesAdmViewSets, TarefasAdmSemAgendamentoViewSet, \
                        TarefasAdmPorDataViewSet , TarefasPorUsuarioViewSet, RepeticoesPorUsuarioViewSet, \
                        TarefasPorUsuarioSemAgendamentoViewSet, TarefasPorUsuarioPorDataViewSet

router = routers.DefaultRouter()
router.register('tarefas', TarefasAdmViewSets, basename='Tarefas')
router.register('repeticoes', RepeticoesAdmViewSets, basename='Repeticoes')
router.register('pilha', TarefasAdmSemAgendamentoViewSet, basename='Pilha')

urlpatterns = [
    path('', include(router.urls)),
    path('tarefas/<str:data>/agenda/', TarefasAdmPorDataViewSet.as_view()),
    path('tarefas/<int:id>/usuario/', TarefasPorUsuarioViewSet.as_view()),
    path('repeticoes/<int:id>/usuario/', RepeticoesPorUsuarioViewSet.as_view()),
    path('pilha/<int:id>/usuario/', TarefasPorUsuarioSemAgendamentoViewSet.as_view()),
    path('tarefas/<int:id>/<str:data>/agendausuario/', TarefasPorUsuarioPorDataViewSet.as_view())
]