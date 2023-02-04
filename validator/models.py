from django.db import models
from django.contrib.auth.models import User

class NombresDisponible(models.Model):
  nombre = models.CharField(max_length=100, unique=True)

  def __str__(self) -> str:
    return self.nombre

def upload_to(instance, filename):
  return 'cargaacademica/{filename}'.format(filename=filename)

class CargasAcademica(models.Model):
  archivo_url = models.FileField(upload_to=upload_to)

  def __str__(self) -> str:
    return self.archivo_url.name

def upload_to2(instance, filename):
  return 'listaalumnos/{filename}'.format(filename=filename)

class ArchivosAlumno(models.Model):
  archivo_url = models.FileField(upload_to=upload_to2)
  codigocurso = models.CharField(max_length=10)
  grupo = models.CharField(max_length=1)
  docente = models.ForeignKey(User, on_delete=models.CASCADE)