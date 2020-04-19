from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from api.filters import AgendasFilter, MedicosFilter, ConsultasFilter, FilterToDestroy
from api.models import Agendas, Consultas, Especialidades, Medicos
from api.serializers import (AgendasSerializer, ConsultaSerializer,
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
    queryset = Agendas.objects.all()
    serializer_class = AgendasSerializer
    ordering_fields = ['dia']   
    filter_backends = [AgendasFilter]


class ConsultasViewSet(viewsets.ModelViewSet):
    queryset = Consultas.objects.all()
    serializer_class = ConsultaSerializer
    filter_backends = [ConsultasFilter]
    
    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        consulta = FilterToDestroy().fetch(request.user.pk, kwargs['pk'])
        if not consulta.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(consulta)
        return Response(status=status.HTTP_200_OK)
