from django.urls import path
from . import views

urlpatterns = [
    path('estudiantes/', views.lista_estudiantes, name='lista_estudiantes'),
    path('estudiantes/crear/', views.crear_estudiante, name='crear_estudiante'),
    path('estudiantes/<int:id>/editar/', views.editar_estudiante, name='editar_estudiante'),
    path('estudiantes/<int:id>/eliminar/', views.eliminar_estudiante, name='eliminar_estudiante'),
    path('apoderados/', views.lista_apoderados, name='lista_apoderados'),
    path('apoderados/crear/', views.crear_apoderado, name='crear_apoderado'),
    path('apoderados/<int:id>/editar/', views.editar_apoderado, name='editar_apoderado'),
    path('apoderados/<int:id>/eliminar/', views.eliminar_apoderado, name='eliminar_apoderado'),
    path('matriculas/', views.lista_matriculas, name='lista_matriculas'),
    path('matriculas/crear/', views.crear_matricula, name='crear_matricula'),
    path('pagos/', views.lista_pagos, name='lista_pagos'),
    path('pagos/registrar/', views.registrar_pago, name='registrar_pago'),
    path('matriculas/<int:id>/confirmar/', views.confirmar_matricula, name='confirmar_matricula'),
    path('matriculas/<int:id>/pdf/', views.descargar_ficha_pdf, name='descargar_ficha_pdf'),
    path('mi-matricula/', views.mi_matricula, name='mi_matricula'),
    path('reportes/', views.reportes, name='reportes'),
]