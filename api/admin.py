from django.contrib import admin

from api.forms import AgendaForm
from api.models import Agendas, Consultas, Especialidades, Horas, Medicos


admin.site.site_header = "Medicar Admin"


class AgendasAdmin(admin.ModelAdmin):
    form = AgendaForm
    list_display = ["id", "medico", "dia"]


class EspecialidadesAdmin(admin.ModelAdmin):
    list_display = ["id", "nome"]


class MedicosAdmin(admin.ModelAdmin):
    list_display = ["id", "crm", "nome", "email", "telefone", "especialidade"]


class HorasAdmin(admin.ModelAdmin):
    list_display = ["id", "hora"]


class ConsultasAdmin(admin.ModelAdmin):
    list_display = ["id", "agenda", "horario", "data_agendamento", "user"]


admin.site.register(Agendas, AgendasAdmin)
admin.site.register(Medicos, MedicosAdmin)
admin.site.register(Consultas, ConsultasAdmin)
admin.site.register(Especialidades, EspecialidadesAdmin)
admin.site.register(Horas, HorasAdmin)
