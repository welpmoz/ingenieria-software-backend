from django.urls import path, include

from horario.views import get_horarios
from curso.views import CursoViewset
from validator.views import CargaViewset, get_docentes, ArchivosAlumnoViewset
from .views import signup, login, get_anteriores_asistencias
from asistencia.views import AsistenciaViewset, MatriculaViewset

from rest_framework import routers

cursoRouter = routers.DefaultRouter()
cursoRouter.register('', CursoViewset)

cargaRouter = routers.DefaultRouter()
cargaRouter.register('', CargaViewset)

archivoAlumnosRouter = routers.DefaultRouter()
archivoAlumnosRouter.register('', ArchivosAlumnoViewset)

asistenciaRouter = routers.DefaultRouter()
asistenciaRouter.register('', AsistenciaViewset)

matriculaRouter = routers.DefaultRouter()
matriculaRouter.register('', MatriculaViewset)

urlpatterns = [
  path('cursos/', include(cursoRouter.urls)),
  path('horarios/', get_horarios),
  path('docentes/', get_docentes),
  path('cargas_academicas/', include(cargaRouter.urls)),
  path('signup/', signup),
  path('login/', login),
  path('carga_alumnos/', include(archivoAlumnosRouter.urls)),
  path('asistencias/', include(asistenciaRouter.urls)),
  path('matriculas/', include(matriculaRouter.urls)),
  path('otraasistencia/', get_anteriores_asistencias),
]