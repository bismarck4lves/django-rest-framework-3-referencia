from django.contrib import admin

from api.forms import AgendaForm
from api.models import Agendas, Consultas, Especialidades, Horas, Medicos


admin.site.site_header = 'Medicar Admin'


@admin.register(Agendas)
class AgendasAdmin (admin.ModelAdmin):
    form = AgendaForm
    list_display = ['id', 'medico', 'dia']


@admin.register(Especialidades)
class EspecialidadesAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']


@admin.register(Medicos)
class MedicosAdmin(admin.ModelAdmin):
    list_display = ['id', 'crm', 'nome', 'email', 'telefone', 'especialidade']


@admin.register(Horas)
class HorasAdmin (admin.ModelAdmin):
    list_display = ['id', 'hora', 'status']


@admin.register(Consultas)
class ConsultasAdmin (admin.ModelAdmin):
    list_display = ['id', 'agenda', 'horario', 'data_agendamento', 'user']
