from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Estudiante
from .forms import EstudianteForm


@login_required(login_url='login')
def lista_estudiantes(request):
    busqueda = request.GET.get('buscar', '')
    if busqueda:
        estudiantes = Estudiante.objects.filter(
            dni__icontains=busqueda
        ) | Estudiante.objects.filter(
            nombres__icontains=busqueda
        ) | Estudiante.objects.filter(
            apellidos__icontains=busqueda
        )
    else:
        estudiantes = Estudiante.objects.all()

    return render(request, 'matriculas/lista_estudiantes.html', {
        'estudiantes': estudiantes,
        'busqueda': busqueda,
    })


@login_required(login_url='login')
def crear_estudiante(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            estudiante = form.save()
            messages.success(request, f'✅ Estudiante {estudiante.nombre_completo} registrado correctamente.')
            return redirect('lista_estudiantes')
    else:
        form = EstudianteForm()

    return render(request, 'matriculas/form_estudiante.html', {
        'form': form,
        'titulo': 'Registrar Nuevo Estudiante',
    })


@login_required(login_url='login')
def editar_estudiante(request, id):
    estudiante = get_object_or_404(Estudiante, id=id)
    if request.method == 'POST':
        form = EstudianteForm(request.POST, instance=estudiante)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ Estudiante actualizado correctamente.')
            return redirect('lista_estudiantes')
    else:
        form = EstudianteForm(instance=estudiante)

    return render(request, 'matriculas/form_estudiante.html', {
        'form': form,
        'titulo': f'Editar Estudiante: {estudiante.nombre_completo}',
    })


@login_required(login_url='login')
def eliminar_estudiante(request, id):
    estudiante = get_object_or_404(Estudiante, id=id)
    if request.method == 'POST':
        nombre = estudiante.nombre_completo
        estudiante.delete()
        messages.success(request, f'🗑️ Estudiante {nombre} eliminado.')
        return redirect('lista_estudiantes')

    return render(request, 'matriculas/eliminar_estudiante.html', {
        'estudiante': estudiante,
    })

from .models import Apoderado
from .forms import ApoderadoForm

@login_required(login_url='login')
def lista_apoderados(request):
    busqueda = request.GET.get('buscar', '')
    if busqueda:
        apoderados = Apoderado.objects.filter(
            dni__icontains=busqueda
        ) | Apoderado.objects.filter(
            nombres__icontains=busqueda
        ) | Apoderado.objects.filter(
            apellidos__icontains=busqueda
        )
    else:
        apoderados = Apoderado.objects.all()

    return render(request, 'matriculas/lista_apoderados.html', {
        'apoderados': apoderados,
        'busqueda': busqueda,
    })

@login_required(login_url='login')
def crear_apoderado(request):
    if request.method == 'POST':
        form = ApoderadoForm(request.POST)
        if form.is_valid():
            apoderado = form.save()
            messages.success(request, f'✅ Apoderado {apoderado.apellidos}, {apoderado.nombres} registrado correctamente.')
            return redirect('lista_apoderados')
    else:
        form = ApoderadoForm()

    return render(request, 'matriculas/form_apoderado.html', {
        'form': form,
        'titulo': 'Registrar Nuevo Apoderado',
    })

@login_required(login_url='login')
def editar_apoderado(request, id):
    apoderado = get_object_or_404(Apoderado, id=id)
    if request.method == 'POST':
        form = ApoderadoForm(request.POST, instance=apoderado)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Apoderado actualizado correctamente.')
            return redirect('lista_apoderados')
    else:
        form = ApoderadoForm(instance=apoderado)

    return render(request, 'matriculas/form_apoderado.html', {
        'form': form,
        'titulo': f'Editar Apoderado: {apoderado.apellidos}, {apoderado.nombres}',
    })

@login_required(login_url='login')
def eliminar_apoderado(request, id):
    apoderado = get_object_or_404(Apoderado, id=id)
    if request.method == 'POST':
        nombre = f'{apoderado.apellidos}, {apoderado.nombres}'
        apoderado.delete()
        messages.success(request, f'🗑️ Apoderado {nombre} eliminado.')
        return redirect('lista_apoderados')

    return render(request, 'matriculas/eliminar_apoderado.html', {
        'apoderado': apoderado,
    })

from .models import Matricula, AnioAcademico, Grado
from .forms import MatriculaForm
from django.utils import timezone

@login_required(login_url='login')
def lista_matriculas(request):
    matriculas = Matricula.objects.all().order_by('-fecha_solicitud')
    return render(request, 'matriculas/lista_matriculas.html', {
        'matriculas': matriculas,
    })

@login_required(login_url='login')
def crear_matricula(request):
    if request.method == 'POST':
        form = MatriculaForm(request.POST)
        if form.is_valid():
            matricula = form.save(commit=False)
            
            # Generar código automático (ej. MAT-2026-0001)
            anio_actual = matricula.anio.anio
            ultima_matricula = Matricula.objects.filter(codigo__startswith=f'MAT-{anio_actual}-').order_by('-id').first()
            
            if ultima_matricula:
                # Extraer el número y sumarle 1
                ultimo_num = int(ultima_matricula.codigo.split('-')[-1])
                nuevo_num = ultimo_num + 1
            else:
                nuevo_num = 1
                
            matricula.codigo = f'MAT-{anio_actual}-{nuevo_num:04d}'
            matricula.registrado_por = request.user
            matricula.estado = 'Pendiente'
            matricula.save()
            
            messages.success(request, f'✅ Matrícula {matricula.codigo} generada. Estado: Pendiente de Pago.')
            return redirect('lista_matriculas')
    else:
        form = MatriculaForm()

    return render(request, 'matriculas/form_matricula.html', {
        'form': form,
        'titulo': 'Registrar Nueva Matrícula',
    })

from .models import Pago
from .forms import PagoForm

@login_required(login_url='login')
def lista_pagos(request):
    pagos = Pago.objects.all().order_by('-fecha_pago')
    return render(request, 'matriculas/lista_pagos.html', {
        'pagos': pagos,
    })

@login_required(login_url='login')
def registrar_pago(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.registrado_por = request.user
            pago.save()

            # Cambiar el estado de la matrícula a 'Pagado'
            matricula = pago.matricula
            matricula.estado = 'Pagado'
            matricula.save()

            messages.success(request, f'✅ Pago registrado. La matrícula {matricula.codigo} ahora está Pagada.')
            return redirect('lista_pagos')
    else:
        form = PagoForm()
        
    # Solo mostrar en el select las matrículas que están pendientes de pago
    form.fields['matricula'].queryset = Matricula.objects.filter(estado='Pendiente')

    return render(request, 'matriculas/form_pago.html', {
        'form': form,
        'titulo': 'Registrar Pago de Matrícula',
    })

from .models import Pago
from .forms import PagoForm

@login_required(login_url='login')
def lista_pagos(request):
    pagos = Pago.objects.all().order_by('-fecha_pago')
    return render(request, 'matriculas/lista_pagos.html', {
        'pagos': pagos,
    })

@login_required(login_url='login')
def registrar_pago(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.registrado_por = request.user
            pago.save()

            # Cambiar el estado de la matrícula a 'Pagado'
            matricula = pago.matricula
            matricula.estado = 'Pagado'
            matricula.save()

            messages.success(request, f'✅ Pago registrado. La matrícula {matricula.codigo} ahora está Pagada.')
            return redirect('lista_pagos')
    else:
        form = PagoForm()
        
    # Solo mostrar en el select las matrículas que están pendientes de pago
    form.fields['matricula'].queryset = Matricula.objects.filter(estado='Pendiente')

    return render(request, 'matriculas/form_pago.html', {
        'form': form,
        'titulo': 'Registrar Pago de Matrícula',
    })


from django.db import models, transaction
from .models import Vacante

@login_required(login_url='login')
def confirmar_matricula(request, id):
    matricula = get_object_or_404(Matricula, id=id)
    
    if matricula.estado != 'Pagado':
        messages.error(request, '❌ Solo se pueden confirmar matrículas que estén en estado "Pagado".')
        return redirect('lista_matriculas')

    # Buscar vacantes disponibles para el grado solicitado y el año
    vacantes_disponibles = Vacante.objects.filter(
        anio=matricula.anio,
        seccion__grado=matricula.grado_solicitado,
        cupos_ocupados__lt=models.F('cupos_totales') # Que haya cupo
    ).order_by('id')

    if request.method == 'POST':
        vacante_id = request.POST.get('vacante')
        if not vacante_id:
            messages.error(request, '❌ Debes seleccionar una sección.')
            return redirect('confirmar_matricula', id=id)

        vacante = get_object_or_404(Vacante, id=vacante_id)

        if vacante.cupos_ocupados >= vacante.cupos_totales:
            messages.error(request, '❌ La sección seleccionada ya no tiene cupos disponibles.')
            return redirect('confirmar_matricula', id=id)

        # Usar transacción para que se guarde todo o no se guarde nada si hay error
        with transaction.atomic():
            # 1. Asignar sección a la matrícula y cambiar estado
            matricula.seccion = vacante.seccion
            matricula.estado = 'Matriculado'
            matricula.fecha_matricula = timezone.now()
            matricula.save()

            # 2. Ocupar la vacante
            vacante.cupos_ocupados += 1
            vacante.save()

        messages.success(request, f'✅ ¡Matrícula confirmada! Alumno asignado a {vacante.seccion}.')
        return redirect('lista_matriculas')

    return render(request, 'matriculas/confirmar_matricula.html', {
        'matricula': matricula,
        'vacantes': vacantes_disponibles,
    })

from django.http import FileResponse
from .pdf_utils import generar_ficha_matricula

@login_required(login_url='login')
def descargar_ficha_pdf(request, id):
    matricula = get_object_or_404(Matricula, id=id)
    
    if matricula.estado != 'Matriculado':
        messages.error(request, '❌ Solo puedes descargar la ficha si la matrícula ya está confirmada.')
        return redirect('lista_matriculas')

    # Generar el PDF
    pdf_buffer = generar_ficha_matricula(matricula)
    
    # Retornar el archivo como descarga
    return FileResponse(
        pdf_buffer, 
        as_attachment=True, 
        filename=f'Ficha_Matricula_{matricula.codigo}.pdf'
    )

from .models import EstudianteApoderado

@login_required(login_url='login')
def mi_matricula(request):
    # Buscamos si el usuario logueado tiene un perfil de apoderado
    try:
        apoderado = request.user.perfil.apoderado
    except:
        apoderado = None
        
    # Si no tiene un apoderado vinculado, le mostramos la lista vacía
    matriculas = []
    if apoderado:
        matriculas = Matricula.objects.filter(apoderado=apoderado).order_by('-fecha_solicitud')

    return render(request, 'matriculas/mi_matricula.html', {
        'matriculas': matriculas,
    })

from django.db.models import Count, Sum

@login_required(login_url='login')
def reportes(request):
    # Solo el administrador puede ver los reportes
    if request.user.perfil.rol != 'Administrador':
        return redirect('dashboard')

    # Estadísticas básicas
    total_estudiantes = Estudiante.objects.count()
    total_matriculados = Matricula.objects.filter(estado='Matriculado').count()
    total_pendientes = Matricula.objects.filter(estado='Pendiente').count()
    total_pagado = Pago.objects.aggregate(total=Sum('monto'))['total'] or 0

    # Matriculados por grado
    por_grado = Matricula.objects.filter(estado='Matriculado').values('grado_solicitado__nombre').annotate(total=Count('id')).order_by('grado_solicitado__orden')

    # Matriculados por sección
    por_seccion = Matricula.objects.filter(estado='Matriculado').values('seccion__grado__nombre', 'seccion__letra').annotate(total=Count('id')).order_by('seccion__grado__orden')

    return render(request, 'matriculas/reportes.html', {
        'total_estudiantes': total_estudiantes,
        'total_matriculados': total_matriculados,
        'total_pendientes': total_pendientes,
        'total_pagado': total_pagado,
        'por_grado': por_grado,
        'por_seccion': por_seccion,
    })