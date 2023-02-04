from django.db import models

def upload_to(instance, filename):
  return 'silabos/{filename}'.format(filename=filename)

class Curso(models.Model):
  denominacion = models.CharField(max_length=100)
  creditos = models.PositiveSmallIntegerField()
  codigo = models.CharField(max_length=10)
  grupo = models.CharField(max_length=1)
  matriculados = models.PositiveSmallIntegerField()
  carrera = models.CharField(max_length=100)
  docente = models.CharField(max_length=100)
  silabo_url = models.FileField(upload_to=upload_to, null=True, blank=True, default=None)

  def __str__(self) -> str:
    return f"{self.docente}:{self.denominacion}:{self.codigo}:{self.grupo}"