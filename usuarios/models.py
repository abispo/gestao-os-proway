from django.contrib.auth.models import User
from django.db import models

class Genero(models.TextChoices):
    NAO_INFORMADO = "NI", "Prefiro não informar"
    MASCULINO = "M", "Masculino"
    FEMININO = "F", "Feminino"

class Perfil(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    data_nascimento = models.DateField(
        verbose_name="Data de Nascimento",
        null=True
    )
    genero = models.CharField(max_length=20, choices=Genero, null=True)
    endereco = models.CharField(max_length=200, null=False)

    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name} ({self.usuario.username})"

    class Meta:
        db_table = "perfis_usuarios"