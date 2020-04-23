from rest_framework import serializers

from api.models import Agendas, Consultas, Especialidades, Medicos
from api.validators import Validators
from datetime import date


class EspecialidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidades
        fields = ["id", "nome"]


class MedicosSerializer(serializers.ModelSerializer):

    especialidade = EspecialidadesSerializer(many=False)

    class Meta:
        model = Medicos
        fields = ["id", "crm", "nome", "especialidade"]


class AgendaSerializer(serializers.ModelSerializer):

    medico = MedicosSerializer()
    horarios = serializers.StringRelatedField(
        many=True, source='horarios_disponiveis')

    class Meta:
        model = Agendas
        fields = ['id', 'medico', 'dia', 'horarios']


class CurrentUserDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user


class ConsultaSerializer(serializers.ModelSerializer):

    agenda_id = serializers.PrimaryKeyRelatedField(
        queryset=Agendas.objects.filter(dia__gte=date.today()),
        write_only=True,
        label='agenda'
    )

    dia = serializers.DateField(source="agenda.dia", read_only=True)

    medico = MedicosSerializer(source="agenda.medico", read_only=True)

    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Consultas
        fields = ['id', 'dia', 'horario', 'data_agendamento',
                  'medico', 'user', 'agenda_id']

    def validate(self, data):

        agenda = data['agenda_id']
        horario = data['horario']

    
        if Validators().data_expirada(agenda.dia, horario):
            raise serializers.ValidationError(
                "Data e hora informados são menores do que a data atual"
            )

        if Validators().mesmo_dia_para_usuario(agenda.dia, horario, data['user']):
            raise serializers.ValidationError(
                'Paciente já possui uma consulta marcada para esse dia e horário'
            )

        if Validators().agenda_em_uso(agenda.pk, horario):

            raise serializers.ValidationError('Agenda em uso')

        if not agenda.horarios.filter(disponivel=True, hora=horario).exists():
            raise serializers.ValidationError('Horário indisponível')

        return data

    def create(self, data):

        agenda = data.pop('agenda_id')

        return Consultas.objects.create(
            dia=agenda.dia,
            agenda=agenda,
            user=data['user'],
            horario=data['horario']
        )
