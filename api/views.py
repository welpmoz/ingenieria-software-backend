from .serializers import UserSerializer
from django.contrib.auth import models, authenticate

from rest_framework import decorators, response

from validator.models import NombresDisponible
from asistencia.models import Asistencia

from asistencia.serializers import AsistenciaSerializer

DIRECTORES = ['NILA ZONIA ACURIO USCA']

# POST /api/login/ 'Content-Type':'application/json'
@decorators.api_view(['POST'])
def login(request):
  username = request.data['username']
  password = request.data['password']
  user = authenticate(username=username, password=password)
  if user is not None:
    return response.Response({
      'username':user.username, 'password':password,
      'is_staff':user.is_staff
    })
  else:
    return response.Response({'detail':'Necesita registrarse.'})

@decorators.api_view(['POST'])
def signup(request):
  nombre = request.data['first_name']
  existe = NombresDisponible.objects.filter(nombre=nombre)
  if existe:
    if nombre in DIRECTORES:
      is_staff = True
    if models.User.objects.filter(first_name=nombre).exists():
      return response.Response({'detail':'El usuario con ese nombre ya existe.'})
    new_user = models.User(is_staff=is_staff, **request.data)
    password = request.data['password']
    new_user.set_password(password)
    new_user.save()
    return response.Response({
      'username':new_user.username, 'password':password,
      'is_staff':new_user.is_staff
    })
  else:
    return response.Response({'detail':'Lo sentimos, no puede registrarse.'})

@decorators.api_view(['GET'])
def get_anteriores_asistencias(request):
  # asistencias = Asistencia.objects.order_by().values_list('fecha').distinct()
  asistencias = Asistencia.objects.values_list('fecha')
  serializer = AsistenciaSerializer(asistencias, many=True)
  return response.Response(serializer.data)