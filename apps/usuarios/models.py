from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Perfil(models.Model):
    ROLES = [
        ('Administrador', 'Administrador'),
        ('Cajero', 'Cajero'),
        ('Apoderado', 'Apoderado'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    apoderado = models.OneToOneField('matriculas.Apoderado', on_delete=models.SET_NULL, null=True, blank=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='Apoderado')
    dni = models.CharField(max_length=8, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.rol}"


# Señal: cuando se crea un User, se crea automáticamente su Perfil
@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance, rol='Apoderado')