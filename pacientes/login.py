import jwt
import datetime
from django.http import JsonResponse
from django.conf import settings
from functools import wraps
from django.shortcuts import render, redirect 
from .models import Paciente
from django.contrib import messages

def autenticacion(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario_autenticado'):
            return redirect('login')
        return func(request, *args, **kwargs)
    return wrapper


def autenticacion_jwt(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        token = None

        # Prioridad 1: Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        else:
            # Prioridad 2: cookie JWT
            token = request.COOKIES.get('jwt')

        if not token:
            print("❌ Token no encontrado")
            return redirect('login')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            request.user_id = payload.get('usuario')  # o 'user_id', según cómo lo pusiste
        except jwt.ExpiredSignatureError:
            print("❌ Token expirado")
            return redirect('login')
        except jwt.InvalidTokenError:
            print("❌ Token inválido")
            return redirect('login')

        return func(request, *args, **kwargs)
    return wrapper




USUARIOS_SIMULADOS = { 'Doctor': {'clave':'123456', 'rol': 'Doctor'},'Doctor Alfredo': {'clave':'123456', 'rol': 'Doctor'}, 'Doctor Juan': {'clave':'123456', 'rol': 'Doctor'}, 'Doctor Messi': {'clave':'123456', 'rol': 'Doctor'}, 'Doctor Cristiano': {'clave':'123456', 'rol': 'Doctor'}, 'Doctor Lamine Yamal': {'clave':'123456', 'rol': 'Doctor'},'a': {'clave':'987654', 'rol': 'Paciente'}, 'Tecnico': {'clave':'1234', 'rol': 'Tecnico'}, 'Tecnico 2': {'clave':'1234', 'rol': 'Tecnico'}, 'Tecnico 3 ': {'clave':'1234', 'rol': 'Tecnico'}, 'Tecnico 4': {'clave':'1234', 'rol': 'Tecnico'}, 'Tecnico 5 ': {'clave':'1234', 'rol': 'Tecnico'}} 



SECRET_KEY = 'supersecreto'  # Guarda esto en settings


def login_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        clave = request.POST.get('clave')

        if usuario in USUARIOS_SIMULADOS and USUARIOS_SIMULADOS[usuario]['clave'] == clave:
            payload = {
                'usuario': usuario,
                'rol': USUARIOS_SIMULADOS[usuario]['rol'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            response = redirect('home')
            response.set_cookie('jwt', token, httponly=True)
            print("✅ Login exitoso. Token emitido.")
            return response

        print("❌ Credenciales inválidas.")
        return render(request, 'Paciente/login.html', {'error': 'Credenciales inválidas'})

    return render(request, 'Paciente/login.html')


def rol_requerido(rol):
    def decorador(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if request.session.get('rol')==rol:
                return func(request, *args, **kwargs)
            messages.error(request, "No tienes la autorizacion para acceder a esta pagina.")
            return redirect('home')
        return wrapper
    return decorador
