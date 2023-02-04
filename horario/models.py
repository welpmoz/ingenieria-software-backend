from django.db import models

class Horario(models.Model):
  dia = models.CharField(max_length=10)
  hi = models.TimeField(null=True, blank=True)
  hf = models.TimeField(null=True, blank=True)
  aula = models.CharField(max_length=10)
  codigocurso = models.CharField(max_length=10)
  grupo = models.CharField(max_length=1)
  tipo = models.CharField(max_length=1)
  carrera = models.CharField(max_length=100)
  docente = models.CharField(max_length=100)

  def __str__(self) -> str:
    return f"{self.docente} -> {self.codigocurso} {self.grupo} {self.tipo}"