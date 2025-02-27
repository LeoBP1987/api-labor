from django.urls import path, include
from rest_framework_mongoengine import routers
from tarefas.views import TarefasViewSets, RepeticoesViewSets, DiaViewSet, SemanaViewSet
from oauth2_provider import urls as oauth2_urls

router = routers.DefaultRouter()
router.register('tarefas', TarefasViewSets, basename='Tarefas')
router.register('repeticoes', RepeticoesViewSets, basename='Repeticoes')
router.register('dia', DiaViewSet, basename='Dia')
router.register('semana', SemanaViewSet, basename='Semana')

urlpatterns = [
    path('', include(router.urls)),
    path('oauth2/', include(oauth2_urls))
]