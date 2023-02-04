from django.db import models

class Matricula(models.Model):
  codigoalumno = models.CharField(max_length=10)
  nombre = models.CharField(max_length=100)
  codigocurso = models.CharField(max_length=10)
  grupo = models.CharField(max_length=1)

class Asistencia(models.Model):
  idmatricula = models.ForeignKey(Matricula, on_delete=models.CASCADE)
  fecha = models.DateTimeField(auto_now_add=True)
  presente = models.BooleanField(default=False)
  observacion = models.TextField(blank=True)