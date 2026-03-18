from django.urls import path
from . import views

urlpatterns = [
    path('', views.conecta, name='home'),
    path('calendario/', views.calendario, name='calendario'),
    path('chamada/', views.chamada, name='chamada'),
    path('area_professor/', views.area_professor, name='area_professor'),
    path('area_aluno/', views.area_aluno, name='area_aluno'),
]