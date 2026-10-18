from django.core.management.base import BaseCommand
from apps.matriculas.models import (
    AnioAcademico, Grado, Seccion, Vacante
)


class Command(BaseCommand):
    help = 'Carga datos iniciales: año académico, grados, secciones y vacantes'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('🚀 Iniciando carga de datos...\n'))

        # 1. Año Académico
        anio, creado = AnioAcademico.objects.get_or_create(
            anio=2026,
            defaults={
                'activo': True,
                'fecha_inicio': '2026-03-01',
                'fecha_fin': '2026-12-15',
            }
        )
        if creado:
            self.stdout.write(self.style.SUCCESS(f'✅ Año académico creado: {anio.anio}'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠️  Año académico ya existía: {anio.anio}'))

        # 2. Grados
        grados_data = [
            ('1° Secundaria', 1),
            ('2° Secundaria', 2),
            ('3° Secundaria', 3),
            ('4° Secundaria', 4),
            ('5° Secundaria', 5),
        ]

        grados = []
        for nombre, orden in grados_data:
            grado, creado = Grado.objects.get_or_create(
                nombre=nombre,
                defaults={'orden': orden}
            )
            grados.append(grado)
            if creado:
                self.stdout.write(self.style.SUCCESS(f'✅ Grado creado: {grado.nombre}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️  Grado ya existía: {grado.nombre}'))

        # 3. Secciones (A y B, turno Mañana)
        secciones = []
        for grado in grados:
            for letra in ['A', 'B']:
                seccion, creado = Seccion.objects.get_or_create(
                    grado=grado,
                    letra=letra,
                    turno='Mañana'
                )
                secciones.append(seccion)
                if creado:
                    self.stdout.write(self.style.SUCCESS(f'✅ Sección creada: {seccion}'))
                else:
                    self.stdout.write(self.style.WARNING(f'⚠️  Sección ya existía: {seccion}'))

        # 4. Vacantes para cada sección
        for seccion in secciones:
            vacante, creado = Vacante.objects.get_or_create(
                anio=anio,
                seccion=seccion,
                defaults={'cupos_totales': 30, 'cupos_ocupados': 0}
            )
            if creado:
                self.stdout.write(self.style.SUCCESS(f'✅ Vacante creada: {vacante}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️  Vacante ya existía: {vacante}'))

        self.stdout.write(self.style.SUCCESS('\n🎉 ¡Carga de datos completada con éxito!'))