from django.db import models #coloquei um monte de null pq tava dando erro essa bosta
from django.core.serializers import serialize

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

    def __str__(self):
        return self.municipio

class Project(models.Model):
    nome_projeto = models.CharField(max_length=30)
    #familias = models.ManyToManyField('Family', on_delete=models.CASCADE)
    #tecnicos = models.CharField(max_length=40) #pretendo deixar isso aqui como um select e obviamente uma chave estrangeira do model de ténicos (cujo irei fzr)
    descricao = models.TextField()
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.nome_projeto
    
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
    (2, "Intermediario"),
    (3, "Avancado")
]

class Family(models.Model):
    nome_titular = models.CharField(max_length=30)
    nome_conjuge = models.CharField(max_length=30)
    data_nascimento = models.DateField()
    data_inicio = models.DateField()
    cpf = models.CharField(max_length=30)
    contato = models.CharField(max_length=30)
    bpc = models.CharField(max_length=50)
    nis = models.CharField(max_length=50)
    dap = models.CharField(max_length=50)
    aposentadoria = models.BooleanField(default=False)
    auxilio = models.BooleanField(default=False)
    escolaridade = models.IntegerField(choices=ESCOLAR_CHOICES, default=1)
    terra = models.OneToOneField('Terrain', on_delete=models.CASCADE)
    projeto = models.ForeignKey('Project', on_delete=models.CASCADE)
    subsistemas = models.ManyToManyField('Subsystem', through='FamilySubsystem', blank=True)

    def __str__(self):
        return self.nome_titular

    def get_pontuacao(self):
        pontuacao = self.subsistemas.count() * 5
        return pontuacao

    def get_nivel(self):
        pontos = self.get_pontuacao()
        if pontos <= 30:
            return dict(LEVEL_CHOICES).get(1)
        elif pontos <= 60:
            return dict(LEVEL_CHOICES).get(2)
        else:
            return dict(LEVEL_CHOICES).get(3)
    
    def get_nome_familia(self):
        try:
            sobrenome = self.nome_titular.split()[1]
            return "Família " + sobrenome
        except IndexError:
            return "Família " + self.nome_titular
        
    def get_escolaridade_display(self):
        return dict(ESCOLAR_CHOICES).get(self.escolaridade)

    def get_subsistemas_list(self):
        return ", ".join(
            f"{fs.subsystem.nome_subsistema} ({len(fs.produtos_saida)} produtos)"
            for fs in FamilySubsystem.objects.filter(family=self)
        )
    
    def add_subsystem_to_family(family, subsystem):
        family_subsystem, created = FamilySubsystem.objects.get_or_create(
            family=family,
            subsystem=subsystem,
        )
        if created:
            family_subsystem.produtos_saida = subsystem.produtos_base
            family_subsystem.save()
        return family_subsystem

class Subsystem(models.Model):
    nome_subsistema = models.CharField(max_length=50)
    produtos_base = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.nome_subsistema

class FamilySubsystem(models.Model):
    family = models.ForeignKey('Family', on_delete=models.CASCADE)
    subsystem = models.ForeignKey('Subsystem', on_delete=models.CASCADE)
    produtos_saida = models.JSONField(default=list, blank=True)

    class Meta:
        unique_together = ('family', 'subsystem')

    def __str__(self):
        return f"{self.family.get_nome_familia()} - {self.subsystem.nome_subsistema}"
    
class Evento(models.Model): #nao mexa ainda aninha esse aqui é o das visitas #tá bom
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