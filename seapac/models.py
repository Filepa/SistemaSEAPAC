from django.db import models #coloquei um monte de null pq tava dando erro essa bosta
from django.core.serializers import serialize
import json

# Create your models here.
class User(models.Model):
    nome = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    senha = models.CharField(max_length=200) #tem que deixar privado depois
    contato = models.CharField(max_length=30)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True)

    def __str__(self):
        return self.nome

class Terrain(models.Model):
    municipio = models.CharField(max_length=30)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    comunidade = models.CharField(max_length=30, null=True)
    tamanho_m2 = models.FloatField(max_length=30, null=True)

class Project(models.Model):
    nome_projeto = models.CharField(max_length=30)
    descricao = models.TextField()
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.nome_projeto

class Subsystem(models.Model):
    nome_subsistema = models.CharField(max_length=20)
    foto_subsistema = models.ImageField(upload_to='fotos_subsistemas/', blank=True)
    produtos_entrada = models.CharField(max_length=20, null=True)
    produtos_saida = models.CharField(max_length=20, null=True)
    destino_produtos_entrada = models.CharField(max_length=20, null=True)
    destino_produtos_saida = models.CharField(max_length=20, null=True)
    produtos_entrada_opcoes = models.JSONField(null=True, blank=True)
    produtos_saida_opcoes = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.nome_subsistema
    
ESCOLAR_CHOICES = [
    (1, "nenhum"),
    (2, "fundamental incompleto"),
    (3, "fundamental completo"),
    (4, "ensino médio incompleto"),
    (5, "ensino médio completo"),
    (6, "ensino superior incompleto"),
    (7, "ensino superior completo"),
    (8, "pós-graduação"),
]

LEVEL_CHOICES = [
    (1, "Inicial"),
    (2, "Intermediário"),
    (3, "Avançado")
]

class Family(models.Model):
    nome_titular = models.CharField(max_length=30)
    nome_conjuge = models.CharField(max_length=30)
    data_nascimento = models.DateField(blank=True)
    data_inicio = models.DateField()
    cpf = models.CharField(max_length=30)
    contato = models.CharField(max_length=30)
    bpc = models.CharField(max_length=50)
    nis = models.CharField(max_length=50)
    dap = models.CharField(max_length=50)
    aposentadoria = models.BooleanField(default=False)
    auxilio = models.BooleanField(default=False)
    escolaridade = models.IntegerField(choices=ESCOLAR_CHOICES, default=1)
    nivel = models.IntegerField(choices=LEVEL_CHOICES, default=1)
    terra = models.OneToOneField('Terrain', on_delete=models.CASCADE)
    projeto = models.ForeignKey('Project', on_delete=models.CASCADE)
    subsistemas = models.ManyToManyField('Subsystem', blank=True)

    def __str__(self):
        return self.nome_titular

    def get_nivel(self):
        return dict(LEVEL_CHOICES).get(self.nivel)
    
    def get_nome_familia(self):
        return "Família " + self.nome_titular.split()[1]

class Evento(models.Model): #nao mexa ainda aninha esse aqui é o das visitas
    titulo = models.CharField(max_length=200)
    inicio = models.DateTimeField()

    def __str__(self):
        return f"{self.titulo} - {self.inicio}"

    @classmethod
    def save_as_fixture(cls):
        eventos = cls.objects.all()
        fixture_data = serialize('json', eventos)
        
        fixture_path = 'seapac/fixtures/eventos.json'
        
        with open(fixture_path, 'w') as f:
            f.write(fixture_data)