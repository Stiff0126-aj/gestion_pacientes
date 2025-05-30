from django.urls import path, include
from .views import home, paciente_list, paciente_historial
from . import views
from django.conf import settings
from django.conf.urls.static import static
from foro import views as foro_views
from . import login
from historias_clinicas import views as historias_views
urlpatterns = [
    
    path('', home, name='home'), 
    path('login/', login.login_view, name='login'),
    path('pacientes/', paciente_list, name='paciente_list'),
    path('crear/', views.paciente_create, name='paciente_create'),
    path('paciente/historial/<int:paciente_id>/', views.paciente_historial, name='paciente_historial'),
    path('paciente/eliminar/<int:paciente_id>/', views.paciente_delete, name='paciente_delete'),
    path('health/', views.healthCheck, name= 'health'),	
path('<int:paciente_id>/foros/', foro_views.foro_paciente, name='foro_paciente'),
    path('<int:paciente_id>/crear_foro/', foro_views.crear_foro, name='crear_foro'),
     path('api/historias/', historias_views.historia_list, name='historia_list'),
    path('api/historia/crear/<int:paciente_id>/', historias_views.crear_historia, name='crear_historia'),

    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

