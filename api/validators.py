from datetime import datetime

from api.models import Agendas, Consultas


class Validators:

    def check_agenda(self, agenda, hora):
        return Agendas.objects.filter(
            pk=agenda,
            horario__id=hora
        ).exists()

    def consulta_disponivel(self, horario, agenda):

        return Consultas.objects.filter(
            horario=horario,
            agenda__id=agenda
        ).exists()

    def data_expirada(self, dia, hora):

        data_verificada = datetime.strptime(
            f"{dia} {hora}", "%Y-%m-%d %H:%M:%S"
        )
        return data_verificada < datetime.today()

    def usuario_tem_mesma_datahora(self, user, horario, agenda):
        return Consultas.objects.filter(
            user=user,
            horario=horario,
            agenda__dia=agenda
        ).exists()
