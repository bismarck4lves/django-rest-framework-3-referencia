from datetime import datetime

from django.db import models
from django.db.models import Count, OuterRef, Subquery, Value
from django.db.models.functions import Concat
from rest_framework.filters import BaseFilterBackend

from api.models import Agendas, Consultas


class MedicosFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        especialidades = request.query_params.getlist("especialidade")
        if especialidades:
            return queryset.filter(especialidade__id__in=especialidades)
        return queryset


class AgendasFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):

        medico = request.query_params.getlist("medico")
        especialides = request.query_params.getlist("especialidade")
        data_inicio = request.query_params.get("data_inicio", None)
        data_fim = request.query_params.get("data_final", None)

        agendas = queryset.annotate(n_horas=Count("horario")).filter(
            medico__in=medico, medico__especialidade__id__in=especialides,
        )

        if data_inicio and data_fim:
            agendas = agendas.filter(dia__range=[data_inicio, data_fim])

        for agenda in agendas:
            if self.n_consultas_marcadas(agenda.pk) >= agenda.n_horas:
                agendas = agendas.exclue(id=agenda.pk)
            
        return agendas

    def n_consultas_marcadas(self, agenda):
        return Consultas.objects.filter(agenda__id=agenda).count()


class ConsultasFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        base_queryset = queryset.annotate(
            data_hora=Concat(
                "agenda__dia",
                models.Value(" "),
                "horario__hora",
                output_field=models.CharField(),
            )
        )
        return base_queryset.filter(data_hora__gte=datetime.today(), user=request.user.pk)


class FilterToDestroy:
    def fetch(self, user, pk):

        base_queryset = Consultas.objects.annotate(
            data_hora=Concat(
                "agenda__dia",
                models.Value(" "),
                "horario__hora",
                output_field=models.DateTimeField(),
            )
        )
        return base_queryset.filter(user=user, data_hora__gte=datetime.now(), pk=pk)
