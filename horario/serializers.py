from .models import Horario

from rest_framework import serializers

class HorarioSerializer(serializers.ModelSerializer):
  class Meta:
    model = Horario
    #fields = ['dia', 'hi', 'hf', 'aula', 'tipo', 'docente', 'carrera']
    fields = '__all__'