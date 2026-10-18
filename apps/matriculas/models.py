from django.db import models
from django.utils import timezone


class AnioAcademico(models.Model):
    anio = models.IntegerField(unique=True)
    activo = models.BooleanField(default=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Año Académico'
        verbose_name_plural = 'Años Académicos'
        ordering = ['-anio']

    def __str__(self):
        return str(self.anio)


class Grado(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    orden = models.IntegerField()

    class Meta:
        verbose_name = 'Grado'
        verbose_name_plural = 'Grados'
        ordering = ['orden']

    def __str__(self):
        return self.nombre


class Seccion(models.Model):
    TURNOS = [
        ('Mañana', 'Mañana'),
        ('Tarde', 'Tarde'),
    ]

    grado = models.ForeignKey(Grado, on_delete=models.CASCADE, related_name='secciones')
    letra = models.CharField(max_length=1)
    turno = models.CharField(max_length=10, choices=TURNOS, default='Mañana')

    class Meta:
        verbose_name = 'Sección'
        verbose_name_plural = 'Secciones'
        unique_together = ('grado', 'letra', 'turno')
        ordering = ['grado__orden', 'letra']

    def __str__(self):
        return f"{self.grado.nombre} - {self.letra} ({self.turno})"


class Vacante(models.Model):
    anio = models.ForeignKey(AnioAcademico, on_delete=models.CASCADE, related_name='vacantes')
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name='vacantes')
    cupos_totales = models.IntegerField(default=30)
    cupos_ocupados = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Vacante'
        verbose_name_plural = 'Vacantes'
        unique_together = ('anio', 'seccion')

    def __str__(self):
        return f"{self.anio} - {self.seccion} ({self.cupos_disponibles} disponibles)"

    @property
    def cupos_disponibles(self):
        return self.cupos_totales - self.cupos_ocupados


class Estudiante(models.Model):
    SEXOS = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    dni = models.CharField(max_length=8, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXOS)
    direccion = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    colegio_procedencia = models.CharField(max_length=150, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return f"{self.apellidos}, {self.nombres} ({self.dni})"

    @property
    def nombre_completo(self):
        return f"{self.apellidos}, {self.nombres}"


class Apoderado(models.Model):
    PARENTESCOS = [
        ('Padre', 'Padre'),
        ('Madre', 'Madre'),
        ('Tutor', 'Tutor'),
        ('Hermano', 'Hermano'),
        ('Tío', 'Tío'),
        ('Otro', 'Otro'),
    ]

    dni = models.CharField(max_length=8, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    parentesco = models.CharField(max_length=20, choices=PARENTESCOS, default='Padre')
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Apoderado'
        verbose_name_plural = 'Apoderados'
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return f"{self.apellidos}, {self.nombres} ({self.parentesco})"


class EstudianteApoderado(models.Model):
    """Relación entre estudiante y apoderado(s)"""
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='apoderados')
    apoderado = models.ForeignKey(Apoderado, on_delete=models.CASCADE, related_name='estudiantes')
    es_principal = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Estudiante-Apoderado'
        verbose_name_plural = 'Estudiantes-Apoderados'
        unique_together = ('estudiante', 'apoderado')

    def __str__(self):
        return f"{self.estudiante} - {self.apoderado}"


class Matricula(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente de Pago'),
        ('Pagado', 'Pagado'),
        ('Matriculado', 'Matriculado'),
        ('Anulado', 'Anulado'),
    ]

    codigo = models.CharField(max_length=20, unique=True)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='matriculas')
    apoderado = models.ForeignKey(Apoderado, on_delete=models.CASCADE, related_name='matriculas')
    anio = models.ForeignKey(AnioAcademico, on_delete=models.CASCADE)
    grado_solicitado = models.ForeignKey(Grado, on_delete=models.CASCADE, related_name='matriculas_solicitadas')
    seccion = models.ForeignKey(Seccion, on_delete=models.SET_NULL, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_matricula = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True)
    registrado_por = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'
        ordering = ['-fecha_solicitud']

    def __str__(self):
        return f"{self.codigo} - {self.estudiante.nombre_completo} ({self.estado})"


class Pago(models.Model):
    METODOS = [
        ('Efectivo', 'Efectivo'),
        ('Yape', 'Yape'),
        ('Plin', 'Plin'),
        ('Transferencia', 'Transferencia'),
        ('Tarjeta', 'Tarjeta'),
    ]

    ESTADOS = [
        ('Confirmado', 'Confirmado'),
        ('Anulado', 'Anulado'),
    ]

    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE, related_name='pagos')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo = models.CharField(max_length=20, choices=METODOS, default='Efectivo')
    numero_operacion = models.CharField(max_length=50, blank=True)
    fecha_pago = models.DateTimeField(default=timezone.now)
    registrado_por = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Confirmado')
    observacion = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['-fecha_pago']

    def __str__(self):
        return f"Pago S/ {self.monto} - {self.matricula.codigo}"