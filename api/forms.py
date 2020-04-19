from datetime import date

from django import forms

from api.models import Agendas


class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agendas
        fields = ["dia", "medico", "horario"]

    def clean(self):

        dia = self.cleaned_data["dia"]
        medico = self.cleaned_data["medico"]

        if dia < date.today():
            raise forms.ValidationError(
                "Não deve ser possível criar uma agenda para um médico em um dia passado"
            )

        db_agenda = Agendas.objects.filter(dia=dia, medico=medico).exists()

        if db_agenda:
            raise forms.ValidationError(
                "Não deve ser possível criar mais de uma agenda para um médico em um mesmo dia"
            )

        return self.cleaned_data
