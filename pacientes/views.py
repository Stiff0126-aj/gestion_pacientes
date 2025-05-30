from django.shortcuts import render, get_object_or_404, redirect
from .models import Paciente
from historias_clinicas.models import HistoriaClinica
import time
from .forms import PacienteForm
from django.http import HttpResponse
from .login import autenticacion_jwt, rol_requerido


@autenticacion_jwt
def home(request):
    return render(request, 'Paciente/home.html')

@autenticacion_jwt
def paciente_historial(request, paciente_id):
    start_time = time.time()
    
    paciente = get_object_or_404(Paciente, id=paciente_id)
    historias = HistoriaClinica.objects.filter(paciente=paciente)
    
    end_time = time.time()
    consulta_time = end_time - start_time
    
    context = {
        'paciente': paciente,
        'historias': historias,
        'consulta_time': consulta_time
    }
    return render(request, 'Paciente/paciente_historial.html', context)

@autenticacion_jwt
@rol_requerido('Doctor')
def paciente_create(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('paciente_list')  
    else:
        form = PacienteForm()

    context = {'form': form}
    return render(request, 'Paciente/paciente_create.html', context)

@autenticacion_jwt
def paciente_list(request):
    pacientes = Paciente.objects.all()
    context = {'paciente_list': pacientes}
    return render(request, 'Paciente/pacientes.html', context)

@autenticacion_jwt
def paciente_delete(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        paciente.delete()
        return redirect('paciente_list')
    return render(request, 'Paciente/pacientes.html')

def healthCheck(request):
    return HttpResponse('ok')