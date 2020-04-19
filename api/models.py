from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


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


class Horas(models.Model):

    id = models.AutoField(primary_key=True)
    hora = models.TimeField()
  
    class Meta:
        verbose_name_plural = "Horas"

    def __str__(self):
        return str(self.hora)


class Agendas(models.Model):

    id = models.AutoField(primary_key=True)
    medico = models.ForeignKey(
        Medicos, related_name="Medicos", on_delete=models.CASCADE
    )
    dia = models.DateField()
    horario = models.ManyToManyField("Horas")

    class Meta:
        verbose_name_plural = "Agendas"
        unique_together = (
            "dia",
            "medico",
        )
        ordering = ["dia"]

    def __str__(self):
        return str(self.dia)


class Consultas(models.Model):

    id = models.AutoField(primary_key=True)
    agenda = models.ForeignKey(
        Agendas, related_name="Agendas", on_delete=models.CASCADE
    )
    horario = models.ForeignKey(Horas, on_delete=models.CASCADE)

    data_agendamento = models.DateTimeField(default=timezone.now(), editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Consultas"

    def __str__(self):
        return str(self.data_agendamento)
