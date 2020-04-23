from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from api.filters import AgendasFilter, ConsultasFilter, MedicosFilter
from api.models import Agendas, Consultas, Especialidades, Medicos
from api.serializers import (AgendaSerializer, ConsultaSerializer,
                             EspecialidadesSerializer, MedicosSerializer)


class EspecialidadesViewSet(viewsets.ModelViewSet):
    queryset = Especialidades.objects.all()
    serializer_class = EspecialidadesSerializer
    filter_backends = [SearchFilter]
    search_fields = ['nome']


class MedicosViewSet(viewsets.ModelViewSet):
    queryset = Medicos.objects.all()
    serializer_class = MedicosSerializer
    filter_backends = [SearchFilter, MedicosFilter]
    search_fields = ['nome']


class AgendasViewSet(viewsets.ModelViewSet):
    queryset = Agendas.disponivel.prefetch_horarios_disponiveis()
    serializer_class = AgendaSerializer
    ordering_fields = ['dia']
    filter_backends = [AgendasFilter]


class ConsultasViewSet(viewsets.ModelViewSet):
    queryset = Consultas.objects.all()
    serializer_class = ConsultaSerializer
    filter_backends = [ConsultasFilter]

    def destroy(self, request, *args, **kwargs):

        consulta = ConsultasFilter().disponivel_para_deletar(request.user.pk, kwargs['pk'])
        if not consulta:
            return Response('Não foi possível desmarcar esta consulta', status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_destroy(consulta)
        
        return Response(status=status.HTTP_200_OK)
