from .models import Asistencia, Matricula
from .serializers import AsistenciaSerializer, MatriculaSerializer

from rest_framework import viewsets, permissions, response

# permitido todas las operaciones
# GET /api/matriculas/?codigocurso=1&grupo=2
class MatriculaViewset(viewsets.ModelViewSet):
  queryset = Matricula.objects.all()
  serializer_class = MatriculaSerializer
  permission_classes = (permissions.IsAuthenticated,)

  def list(self, request, *args, **kwargs):
    if request.query_params:
      matriculas = Matricula.objects.filter(**request.query_params.dict())
      serializer = MatriculaSerializer(matriculas, many=True)
      return response.Response(serializer.data)
    else:
      return response.Response({'detail':'Llamada incorrecta.'})

# POST /api/asistencias
class AsistenciaViewset(viewsets.ModelViewSet):
  queryset = Asistencia.objects.all()
  serializer_class = AsistenciaSerializer
  permission_classes = (permissions.IsAuthenticated,)