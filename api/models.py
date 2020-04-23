from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone

from api.managers import AgendaDisponivelManager, AgendaQuerySet


class Especialidades(models.Model):

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Especialidades"

    def __str__(self):
        return self.nome


class Medicos(models.Model):

    id = models.AutoField(primary_key=True)
    crm = models.IntegerField(unique=True)
    nome = models.CharField(max_length=25, unique=True)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=255, unique=True)
    especialidade = models.ForeignKey(
        Especialidades, related_name="Especialidades", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "Medicos"

    def __str__(self):
        return str(self.nome)


class Agendas(models.Model):

    id = models.AutoField(primary_key=True)

    medico = models.ForeignKey(
        Medicos, related_name="Medicos", on_delete=models.CASCADE
    )

    dia = models.DateField()

    objects = models.Manager()

    disponivel = AgendaDisponivelManager.from_queryset(AgendaQuerySet)()

    class Meta:
        verbose_name_plural = "Agendas"
        unique_together = (
            "dia",
            "medico",
        )
        ordering = ["dia"]

    def __str__(self):
        return str(self.dia)


class AgendaHora(models.Model):

    agenda = models.ForeignKey(
        Agendas, related_name='horarios', on_delete=models.PROTECT)
    hora = models.TimeField()
    disponivel = models.BooleanField(
        'disponível', default=True, editable=False)

    class Meta:
        verbose_name = 'Horário'
        ordering = ['hora']
        unique_together = ['agenda', 'hora']

    def __str__(self):
        return str(self.hora)


class Consultas(models.Model):

    id = models.AutoField(primary_key=True)
    dia = models.DateField()
    agenda = models.ForeignKey(
        Agendas, related_name="Agendas", on_delete=models.CASCADE
    )
    horario = models.TimeField()

    data_agendamento = models.DateTimeField(
        default=timezone.now(), editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['dia', 'horario']
        verbose_name_plural = "Consultas"

    def __str__(self):
        return str(self.data_agendamento)


@receiver(post_save, sender=Consultas)
def marcar_horario_como_indisponivel(sender, instance, created, **kwargs):
    if created:
        (
            AgendaHora
            .objects
            .filter(agenda__dia=instance.dia, hora=instance.horario)
            .update(disponivel=False)
        )


@receiver(post_delete, sender=Consultas)
def marcar_horario_como_disponivel(sender, instance, **kwargs):
    (
        AgendaHora
        .objects
        .filter(agenda__dia=instance.dia, hora=instance.horario)
        .update(disponivel=True)
    )
