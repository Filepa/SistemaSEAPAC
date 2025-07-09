from django.db import models

# Create your models here.
class User(models.Model):
    nome = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    senha = models.CharField(max_length=200) #tem que deixar privado depois
    contato = models.CharField(max_length=30)
    foto_perfil = models.ImageField(upload_to='fotos_de_perfil/', blank=True, null=True) #favor não utilizar ainda

    def __str__(self):
        return self.nome
    
class Family(models.Model):
    nome_titular = models.CharField(max_length=30)
    

    def __str__(self):
        return self.nome_titular