from rest_framework.filters import BaseFilterBackend
from api.models import Consultas
from api.validators import Validators
from datetime import date, datetime
from django.db.models import Case, Q, Value, When


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

        agendas = queryset.filter(
            medico__in=medico,
            medico__especialidade__id__in=especialides,
        )

        if data_inicio and data_fim:
            agendas = agendas.filter(dia__range=[data_inicio, data_fim])

        return agendas


class ConsultasFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):

        hoje = date.today()
        hora = datetime.now().strftime('%H:%M')

        return queryset.filter(
            user=request.user,
            dia__gte=date.today(),
            horario__gte=Case(
                When(
                    Q(agenda__dia=hoje), then=Value(hora)
                ),
                default=Value('00:00')
            )
        )

    def disponivel_para_deletar(self, user, consulta):

        consulta = Consultas.objects.filter(
            pk=consulta,
            user=user
        )

        if not consulta.exists():
            return False

        data = consulta.first()

        if Validators().data_expirada(data.dia, data.horario):

            return False

        return consulta
