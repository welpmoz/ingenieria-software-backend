from .models import CargasAcademica, NombresDisponible, ArchivosAlumno
from .serializers import CargaSerializer, NombresSerializer, ArchivoAlumnosSerializer
from asistencia.models import Matricula

from rest_framework import parsers, permissions, viewsets, decorators, response

from curso.models import Curso
from horario.models import Horario
from asistencia.models import Asistencia, Matricula

import openpyxl as xl
import pandas as pd
import sqlalchemy as sqal
import datetime as time

url = 'postgresql+psycopg2://postgres:postgres@localhost:5432/backend3'
engine = sqal.create_engine(url=url, echo=False)

split_data = lambda doble_curso : doble_curso.split(' / ')

def divide_atributo(atributo):
  return pd.Series(map(split_data, atributo))

def transformar_hora(entero):
  if (entero == None):
    return time.time(hour=0)
  return time.time(hour=entero)

# no interactua con el frontend
class CargaViewset(viewsets.ModelViewSet):
  queryset = CargasAcademica.objects.all()
  parser_classes = (parsers.MultiPartParser, parsers.FormParser)
  serializer_class = CargaSerializer

  def perform_create(self, serializer):
    CargasAcademica.objects.all().delete()
    NombresDisponible.objects.all().delete()
    Horario.objects.all().delete()
    Curso.objects.all().delete()
    Matricula.objects.all().delete()
    Asistencia.objects.all().delete()
    serializer.save()
    archivos = CargasAcademica.objects.all()
    archivo = archivos[0]
    ruta = archivo.archivo_url
    # load workbook
    data_excel = xl.load_workbook(ruta, data_only=True)
    hoja_distribucion = data_excel['DISTR. SEM 2022-2-INF']
    data = hoja_distribucion.tables['CARGA_ACAD']
    data = hoja_distribucion[data.ref]
    lista_filas = []
    for fila in data:
      atributos = []
      for atributo in fila:
        atributos.append(atributo.value)
      lista_filas.append(atributos)
    dataframe = pd.DataFrame(data=lista_filas[1:], index=None, columns=lista_filas[0])
    dataframe.drop(['N°', 'Columna1', 'HP', 'HT', 'AFORO LÍMITE'], axis=1, inplace=True)
    dataframe['CARRERA'] = divide_atributo(dataframe['CARRERA'])
    dataframe['CODIGO'] = divide_atributo(dataframe['CODIGO'])
    dataframe = dataframe.explode(['CODIGO', 'CARRERA'])
    # borrar cursos inactivos
    index_inactivos = dataframe[
      (dataframe.DOCENTES == 'CURSO DESACTIVADO') |
      (dataframe.DOCENTES == 'GRUPO DESACTIVADO') |
      (dataframe.DOCENTES == 'CURSO O GRUPO POR DESACTIVAR')
    ].index
    dataframe.drop(index=index_inactivos, inplace=True)
    # agregar datos a nombres disponibles
    columnas_nombre = ['DOCENTES']
    nombres_disponibles = dataframe[columnas_nombre].drop_duplicates()
    nombres_disponibles.columns = ['nombre']
    # agregar datos a cursos
    columnas_curso = ['CURSO', 'CRED.', 'CODIGO', 'GPO', 'MATRICULADOS', 'CARRERA', 'DOCENTES']
    cursos = dataframe[columnas_curso].drop_duplicates()
    cursos.columns = ['denominacion', 'creditos', 'codigo', 'grupo', 'matriculados', 'carrera', 'docente']
    # agregar datos a horarios
    columnas_horario = ['DIA', 'HR/\nINICIO', 'HR/\nFIN', 'AULA', 'CODIGO', 'DOCENTES', 'TIPO', 'CARRERA', 'GPO']
    horarios = dataframe[columnas_horario].drop_duplicates()
    horarios.columns = ['dia', 'hi', 'hf', 'aula', 'codigocurso', 'docente', 'tipo', 'carrera', 'grupo']
    horarios['hi'] = pd.Series(map(transformar_hora, horarios['hi']))
    horarios['hf'] = pd.Series(map(transformar_hora, horarios['hf']))
    # abrir la conexion e insertar datos
    nombres_disponibles.to_sql(NombresDisponible._meta.db_table, engine, index=False, if_exists='append')
    cursos.to_sql(Curso._meta.db_table, engine, index=False, if_exists='append')
    horarios.to_sql(Horario._meta.db_table, engine, index=False, if_exists='append')

# GET /api/docentes/ - 'application/json'
@decorators.api_view(['GET'])
@decorators.permission_classes([permissions.IsAuthenticated,])
def get_docentes(request):
  docentes = NombresDisponible.objects.all()
  serializer = NombresSerializer(docentes, many=True)
  return response.Response(serializer.data)

class ArchivosAlumnoViewset(viewsets.ModelViewSet):
  queryset = ArchivosAlumno.objects.all()
  parser_classes = (parsers.MultiPartParser, parsers.FormParser,)
  permission_classes = (permissions.IsAuthenticated,)
  serializer_class = ArchivoAlumnosSerializer

  # Aqui se debe procesar el excel subido
  # POST /api/carga_alumnos/?codigocurso=1&grupo=2
  def perform_create(self, serializer):
    serializer.save(docente=self.request.user)
    lectura = pd.read_excel(serializer.data.get('archivo_url'), header=None)
    lectura.columns = ['id', 'codigoalumno', 'nombre']
    lectura.drop(['id'], axis=1, inplace=True)
    parametros = self.request.query_params.dict()
    codigocurso = parametros.get('codigocurso')
    grupo = parametros.get('grupo')
    lectura['codigocurso'] = codigocurso
    lectura['grupo'] = grupo
    lectura.to_sql(Matricula._meta.db_table, engine, index=False, if_exists='append')

  # PUT
  def perform_update(self, serializer):
    print('llamando a put')
    return super().perform_update(serializer)