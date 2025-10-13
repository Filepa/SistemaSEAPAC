from django.db import models
from django.contrib.auth.models import AbstractUser
from seapac.models import Municipality

#Model base para usuários (sejam eles de qualquer grupo)
class Usuario(AbstractUser):
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(blank=False)
    cpf = models.CharField(max_length=11, unique=True,null=True, blank=True, verbose_name="CPF")
    nome_cidade = models.ForeignKey(Municipality, on_delete=models.SET_NULL, null=True, blank=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    nome_bairro = models.CharField(max_length=100, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='perfil/', null=True, blank=True, verbose_name="Foto de Perfil")

    def __str__(self):
        return f"{self.username} - {self.cpf}"
    
    #Vê qual tipo de usuário que está logado no sistema (se é ADM ou Técnico)
    @property
    def is_administrador(self):
        return self.groups.filter(name="ADMINISTRADORES").exists()
    
    @property
    def is_tecnico(self):
        return self.groups.filter(name="TECNICOS").exists()

