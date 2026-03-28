from django.contrib.auth.models import User
from django.db import models

class StatusOrdemDeServico(models.TextChoices):
    ABERTA = "ABT", "Aberta"
    EM_ANDAMENTO = "EAD", "Em Andamento"
    CONCLUIDA = "CNC", "Concluída"
    CANCELADA = "CCL", "Cancelada"

class OrdemDeServico(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data_de_criacao = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=50,
        choices=StatusOrdemDeServico,
        default=StatusOrdemDeServico.ABERTA.value
    )

    cliente = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ordens_cliente"
    )

    tecnico = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="ordens_tecnico"
    )

    def __str__(self):
        return f"{self.titulo} ({self.status})"
    
    def esta_finalizada(self):
        return self.status == StatusOrdemDeServico.CANCELADA.value or \
            self.status == StatusOrdemDeServico.CONCLUIDA.value
    
    class Meta:
        verbose_name = "Ordem de Serviço"
        verbose_name_plural = "Ordens de Serviço"
        ordering = ['-data_de_criacao']
        db_table = "ordens_de_servico"
        permissions = [
            ('pode_visualizar_todas_os', 'Pode visualizar todas as ordens de serviço'),
            ('pode_atribuir_tecnico', 'Pode atribuir uma Ordem de Serviço a um técnico'),
            ('pode_fechar_os', 'Pode fechar uma ordem de serviçox')
        ]