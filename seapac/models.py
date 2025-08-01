from django.db import models #coloquei um monte de null pq tava dando erro essa bosta

# Create your models here.
class User(models.Model):
    nome = models.CharField(max_length=30, null=True)
    email = models.EmailField(max_length=30, null=True)
    senha = models.CharField(max_length=200, null=True) #tem que deixar privado depois
    contato = models.CharField(max_length=30, null=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True) #favor não utilizar ainda

    def __str__(self):
        return self.nome
    
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
    nome_familia = models.CharField(max_length=30, null=True)
    nome_titular = models.CharField(max_length=30, null=True)
    nome_conjuge = models.CharField(max_length=30, null=True)
    data_nasc = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    data_inic = models.DateField(auto_now_add=True, null=True)
    cpf = models.CharField(max_length=30, null=True)
    contato = models.CharField(max_length=30, null=True)
    bpc = models.CharField(max_length=50, null=True)
    nis = models.CharField(max_length=50, null=True)
    dap = models.CharField(max_length=50, null=True)
    aposentadoria = models.BooleanField(default=False, null=True)
    auxilio = models.BooleanField(default=False, null=True)
    escolaridade = models.IntegerField(choices=ESCOLAR_CHOICES, default=1, null=True)
    nivel = models.IntegerField(choices=LEVEL_CHOICES, default=1, null=True)
    #falta o link com a terra e o subsistema, mas é algo a ser decidido

    def __str__(self):
        return self.nome_familia
    
    def get_nivel(self):
        return dict(LEVEL_CHOICES).get(self.nivel)
    
class Subsystem(models.Model):
    nome_subsistema = models.CharField(max_length=20)
    #foto_subsistema = models.ImageField(upload_to='fotos_subsistemas/', blank=True, null=True) #favor nao utilizar ainda
    #produtos_entrada = models.CharField()
    #produtos_saida = models.CharField()
    #destino_produtos_entrada = models.CharField()
    #destino_produtos_saida = models.CharField()

    def __str__(self):
        return self.nome_subsistema
    
class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    inicio = models.DateTimeField()