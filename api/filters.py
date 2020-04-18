from rest_framework.filters import BaseFilterBackend
from datetime import datetime, timedelta
from django.db import models
from django.db.models import OuterRef, Subquery, Q
from api.models import Consultas, Agendas
from api.validators import Validators


class MedicosFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        especialidades = request.query_params.getlist('especialidade')
        if especialidades:
            return queryset.filter(especialidade__id__in=especialidades)
        return queryset


class AgendasFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):

        hoje = datetime.today()
        mais_trinta_dias = hoje + timedelta(days=30)

        medico = request.query_params.getlist('medico')
        especialides = request.query_params.getlist('especialidade')
        data_inicio = request.query_params.get('data_inicio', hoje)
        data_fim = request.query_params.get('data_final', mais_trinta_dias)
        return queryset.filter(
            medico__in=medico,
            medico__especialidade__id__in=especialides,
            dia__range=[data_inicio, data_fim],
        )


class ConsultasFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        base_queryset = queryset.annotate(
            data_hora=models.functions.Concat(
                'agenda__dia',
                models.Value(' '),
                'horario__hora',
                output_field=models.DateTimeField()
            )
        )

        return base_queryset.filter(
            data_hora__gte=datetime.today(),
            user=request.user.pk
        )


class FilterToDestroy():

    def fetch(self, user, pk):
        return Consultas.objects.filter(
            user=user,
            pk=pk
        )
