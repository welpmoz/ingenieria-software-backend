from .models import Matricula, Asistencia

from rest_framework import serializers

class MatriculaSerializer(serializers.ModelSerializer):
  class Meta:
    model = Matricula
    fields = ['id', 'codigoalumno', 'nombre']

class AsistenciaSerializer(serializers.ModelSerializer):
  class Meta:
    model = Asistencia
    fields = '__all__'