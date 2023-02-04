from .models import NombresDisponible, CargasAcademica, ArchivosAlumno
from rest_framework import serializers

class NombresSerializer(serializers.ModelSerializer):
  class Meta:
    model = NombresDisponible
    fields = ['nombre']

class CargaSerializer(serializers.ModelSerializer):
  archivo_url = serializers.FileField(required=True)

  class Meta:
    model = CargasAcademica
    fields = ['archivo_url']

class ArchivoAlumnosSerializer(serializers.ModelSerializer):
  archivo_url = serializers.FileField(required=True)

  class Meta:
    model = ArchivosAlumno
    fields = ['archivo_url', 'codigocurso', 'grupo']