from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_view(request):
    #if request.user.is_authenticated:
        #return redirect('dashboard')

    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = 'Usuario o contraseña incorrectos'

    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard_view(request):
    perfil = getattr(request.user, 'perfil', None)
    rol = perfil.rol if perfil else 'Apoderado'

    menus = {
        'Administrador': [
            {'icono': 'bi-people-fill', 'titulo': 'Estudiantes', 'descripcion': 'Registrar y gestionar estudiantes', 'url': '/estudiantes/'},
            {'icono': 'bi-person-badge-fill', 'titulo': 'Apoderados', 'descripcion': 'Registrar y gestionar apoderados', 'url': '/apoderados/'},
            {'icono': 'bi-journal-check', 'titulo': 'Matrículas', 'descripcion': 'Registrar y aprobar matrículas', 'url': '/matriculas/'},
            {'icono': 'bi-cash-coin', 'titulo': 'Pagos', 'descripcion': 'Ver todos los pagos registrados', 'url': '/pagos/'},
            {'icono': 'bi-file-earmark-text-fill', 'titulo': 'Reportes', 'descripcion': 'Reportes y estadísticas', 'url': '/reportes/'},
            {'icono': 'bi-people-fill', 'titulo': 'Usuarios', 'descripcion': 'Gestionar usuarios y roles', 'url': '/admin/'},
        ],
        'Cajero': [
            {'icono': 'bi-cash-coin', 'titulo': 'Registrar Pago', 'descripcion': 'Registrar el pago de una matrícula', 'url': '/pagos/registrar/'},
            {'icono': 'bi-clock-history', 'titulo': 'Matrículas Pendientes', 'descripcion': 'Ver matrículas por cobrar', 'url': '/matriculas/'},
            {'icono': 'bi-receipt', 'titulo': 'Historial de Pagos', 'descripcion': 'Consultar pagos realizados', 'url': '/pagos/'},
        ],
        'Apoderado': [
            {'icono': 'bi-journal-check', 'titulo': 'Mi Matrícula', 'descripcion': 'Ver estado de matrícula de mi hijo', 'url': '/mi-matricula/'},
            {'icono': 'bi-file-earmark-text-fill', 'titulo': 'Ficha de Matrícula', 'descripcion': 'Descargar ficha en PDF', 'url': '/mi-matricula/'},
        ],
    }

    opciones = menus.get(rol, [])

    return render(request, 'dashboard.html', {
        'usuario': request.user,
        'rol': rol,
        'opciones': opciones,
    })