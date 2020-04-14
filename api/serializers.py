from rest_framework import serializers

from api.models import Agendas, Consultas, Especialidades, Horas, Medicos
from api.validators import Validators


class EspecialidadesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Especialidades
        fields = ['id', 'nome']


class MedicosSerializer(serializers.ModelSerializer):

    especialidade = EspecialidadesSerializer(many=False)

    class Meta:
        model = Medicos
        fields = ['id', 'crm', 'nome', 'especialidade']


class AgendasSerializer(serializers.ModelSerializer):

    medico = MedicosSerializer(many=False, read_only=True)
    horario = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='hora',
    )

    def to_representation(self, instance):

        data = super(AgendasSerializer, self).to_representation(instance)

        def valida_datas(dia, hora, agenda_id):

            horario = Horas.objects.get(hora=hora)

            expirado = Validators().data_expirada(dia, hora)
            if expirado:
                return False

            em_uso = Validators().consulta_disponivel(horario.pk, agenda_id)
            if em_uso:
                return False

            return True

        data['horario'] = list(
            filter(lambda hora: valida_datas(data['dia'], hora, data['id']),
                   data['horario'])
        )
        if not data['horario']:
            return None
        return data

    class Meta:
        model = Agendas
        fields = ['id', 'medico', 'dia', 'horario']


class ConsultaSerializer(serializers.ModelSerializer):

    agenda_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Agendas.objects.all()
    )
    dia = serializers.DateField(source='agenda.dia', read_only=True)
    horario = serializers.TimeField(source='horario.hora', format="%H:%M")
    medico = MedicosSerializer(source='agenda.medico', read_only=True)

    class Meta:
        model = Consultas
        fields = ['id', 'dia', 'horario',
                  'data_agendamento', 'medico', 'agenda_id']

    def create(self, validated_data):

        usuario = validated_data.get('user')
        agenda = validated_data.get('agenda_id')

        horario = validated_data.get('horario').get('hora')
        horario = Horas.objects.get(hora=horario)

        expirado = Validators().data_expirada(
            agenda,
            horario.hora
        )
        if expirado:
            raise (serializers.ValidationError(
                'Data e hora informados são menores do que a data atual'
            ))

        hora_agenda_existe = Validators().check_agenda(
            agenda.pk,
            horario.pk
        )
        if not hora_agenda_existe:
            raise (serializers.ValidationError(
                'Agenda e hora não coincidem'
            ))

        agenda_em_uso = Validators().consulta_disponivel(
            horario.pk,
            agenda.pk
        )
        if agenda_em_uso:
            raise (serializers.ValidationError(
                'A consulta não está disponível para data e hora solicitadas.'
            ))

        mesma_datahora = Validators().usuario_tem_mesma_datahora(
            usuario.pk,
            horario.pk,
            agenda.dia
        )

        if mesma_datahora:
            raise (serializers.ValidationError(
                'Você já tem uma consulta marcada para esta mesma data e hora'
            ))

        return Consultas.objects.create(user=usuario, horario=horario, agenda=agenda)
