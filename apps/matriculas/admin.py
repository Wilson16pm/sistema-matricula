from django.contrib import admin
from .models import (
    AnioAcademico, Grado, Seccion, Vacante,
    Estudiante, Apoderado, EstudianteApoderado,
    Matricula, Pago
)


@admin.register(AnioAcademico)
class AnioAcademicoAdmin(admin.ModelAdmin):
    list_display = ('anio', 'activo', 'fecha_inicio', 'fecha_fin')
    list_filter = ('activo',)


@admin.register(Grado)
class GradoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'orden')
    ordering = ('orden',)


@admin.register(Seccion)
class SeccionAdmin(admin.ModelAdmin):
    list_display = ('grado', 'letra', 'turno')
    list_filter = ('grado', 'turno')


@admin.register(Vacante)
class VacanteAdmin(admin.ModelAdmin):
    list_display = ('anio', 'seccion', 'cupos_totales', 'cupos_ocupados', 'cupos_disponibles')
    list_filter = ('anio', 'seccion__grado')


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('dni', 'apellidos', 'nombres', 'sexo', 'fecha_nacimiento')
    search_fields = ('dni', 'nombres', 'apellidos')
    list_filter = ('sexo',)


@admin.register(Apoderado)
class ApoderadoAdmin(admin.ModelAdmin):
    list_display = ('dni', 'apellidos', 'nombres', 'parentesco', 'telefono')
    search_fields = ('dni', 'nombres', 'apellidos')
    list_filter = ('parentesco',)


@admin.register(EstudianteApoderado)
class EstudianteApoderadoAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'apoderado', 'es_principal')
    list_filter = ('es_principal',)


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'estudiante', 'anio', 'grado_solicitado', 'seccion', 'estado', 'fecha_solicitud')
    list_filter = ('estado', 'anio', 'grado_solicitado')
    search_fields = ('codigo', 'estudiante__dni', 'estudiante__nombres', 'estudiante__apellidos')


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'monto', 'metodo', 'fecha_pago', 'estado', 'registrado_por')
    list_filter = ('metodo', 'estado')
    search_fields = ('matricula__codigo', 'numero_operacion')