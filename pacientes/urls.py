from django.urls import path, include
from .views import home, paciente_list, paciente_historial
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', home, name='home'), 
    path('pacientes/', paciente_list, name='paciente_list'),
    path('crear/', views.paciente_create, name='paciente_create'),
    path('paciente/historial/<int:paciente_id>/', views.paciente_historial, name='paciente_historial'),
    path('paciente/eliminar/<int:paciente_id>/', views.paciente_delete, name='paciente_delete'),
    path('health/', views.healthCheck, name= 'health'),		
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('historias/', include('historias_clinicas.urls')),
]