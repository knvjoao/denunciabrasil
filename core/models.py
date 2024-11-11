from django.db import models
from django.contrib.auth.models import User
import random

#Para simplificar, o token será um inteiro de 1 a 1000, definido pela biblioteca random. Para algo mais seguro, poderia ser usada a biblioteca uuid.
def criar_token():
    return random.randint(1, 1000)

#Uma denúncia tem um usuário, um usuário pode fazer mais de uma denúncia.
#Em caso de implementação, status seria uma variável que mudaria quando a denúncia fosse visualizada. Para o Projeto, é definido como "Pendente".

class Denuncia(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    token = models.IntegerField(default=criar_token)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    status = "Pendente"
    senha = models.CharField(max_length=50)

def __str__(self):
    return f"Denúncia: {self.titulo} | (Token: {self.token})"