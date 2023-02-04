from .models import Curso

from rest_framework import serializers

class CursoSerializer(serializers.ModelSerializer):
  silabo_url = serializers.FileField(required=False)

  class Meta:
    model = Curso
    fields = ['id', 'codigo', 'grupo', 'denominacion', 'carrera', 'matriculados', 'silabo_url', 'creditos']