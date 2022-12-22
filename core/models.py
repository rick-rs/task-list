from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


# Create your models here.
class Tarefa(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_expiracao = models.DateTimeField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

    class Meta:
        db_table = 'tarefa'
    
    def get_data_expiracao(self):
        return self.data_expiracao.strftime('%Y-%m-%dT%H:%M')
    
    def get_tarefa_atrasada(self):
        if self.data_expiracao < datetime.now():
            return True
        else:
            return False
