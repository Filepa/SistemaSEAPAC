from django.db import models
from django.contrib.auth.models import AbstractUser
from seapac.models import Municipality
import os
from PIL import Image
from django.conf import settings

#Model base para usuários (sejam eles de qualquer grupo)
class Usuario(AbstractUser):
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(blank=False)
    cpf = models.CharField(max_length=18, unique=True,null=True, blank=True, verbose_name="CPF")
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

    def has_valid_photo(self):
        if self.foto_perfil and self.foto_perfil.name:
            caminho = os.path.join(settings.MEDIA_ROOT, self.foto_perfil.name)
            return os.path.exists(caminho)
        return False

    def get_photo_url(self):
        if self.has_valid_photo():
            return self.foto_perfil.url
        return None

    #redimensionamento de imagem
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  #salva a imagem normalmente

        if self.foto_perfil:
            caminho = os.path.join(settings.MEDIA_ROOT, self.foto_perfil.name)

            img = Image.open(caminho)
            tamanho_max = (400, 400)
            img.thumbnail(tamanho_max) #Redimensiona mantendo proporção
            img.save(caminho)

   