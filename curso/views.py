from .models import Curso
from .serializers import CursoSerializer

from rest_framework import viewsets, permissions, parsers, response

class CursoViewset(viewsets.ModelViewSet):
  queryset = Curso.objects.all()
  serializer_class = CursoSerializer
  parser_classes = (parsers.MultiPartParser, parsers.FormParser,)
  permission_classes = (permissions.IsAuthenticated,)

  # PUT /api/cursos/id/ - ContentType:multipart/form-data
  # GET /api/cursos/ - ContentType:application/json?
  def list(self, request, *args, **kwargs):
    if request.query_params:
      cursos = Curso.objects.filter(**request.query_params.dict())
      serializer = CursoSerializer(cursos, many=True)
      return response.Response(serializer.data)
    user = request.user
    cursos = Curso.objects.filter(docente=user.first_name)
    serializer = CursoSerializer(cursos, many=True)
    return response.Response(serializer.data)
