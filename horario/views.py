from .models import Horario
from .serializers import HorarioSerializer

from rest_framework import permissions, decorators, response

# GET /api/horarios/?grupo&codigo_curso
@decorators.api_view(['GET'])
@decorators.permission_classes([permissions.IsAuthenticated,])
def get_horarios(request):
  if request.query_params:
    user = request.user
    #horarios = Horario.objects.filter(**request.query_params.dict())
    horarios = Horario.objects.filter(docente=user.first_name, **request.query_params.dict())
    if horarios:
      serializer = HorarioSerializer(horarios, many=True)
      return response.Response(serializer.data)
    else:
      return response.Response({'detail':'Tu curso no tiene horario.'})
  else:
    return response.Response({'detail':'Prueba /api/horarios/?grupo=2&codigo_curso=3'})