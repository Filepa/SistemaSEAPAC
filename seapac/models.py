from django.db import models
    
class Technician(models.Model):
    nome_tecnico = models.CharField(max_length=30)
    descricao = models.TextField()
    telefone = models.CharField(max_length=30)
    cpf = models.CharField(max_length=30)
    email = models.EmailField()
    data_nascimento = models.DateField(blank=True, null=True)
    #foto = models.ImageField(upload_to='tecnicos/fotos_perfil', blank=True) ---> está dando erros seríssimos

    def __str__(self):
        return self.nome_tecnico
    
class Municipality(models.Model):
    nome = models.CharField(max_length=30)

    def __str__(self):
        return self.nome

class Terrain(models.Model):
    municipio = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    comunidade = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.municipio

LEVEL_CHOICES = [
    (1, "Inicial"),
    (2, "Intermediario"),
    (3, "Avancado")
]

class Family(models.Model):
    nome_titular = models.CharField(max_length=30)
    data_inicio = models.DateField()
    contato = models.CharField(max_length=30)
    terra = models.OneToOneField('Terrain', on_delete=models.CASCADE)
    projeto = models.ForeignKey('Project', on_delete=models.CASCADE, blank=True)
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
    
    def get_visitas_confirmadas(self):
        return self.eventos.filter(confirmado=True).count()

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

class Project(models.Model):
    nome_projeto = models.CharField(max_length=30)
    familias = models.ManyToManyField(Family)
    tecnicos = models.ManyToManyField(Technician)
    descricao = models.TextField()
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)
    orcamento = models.CharField(max_length=30, blank=True, null=True) #nao tem no diagrama mas eu mantive

    def __str__(self):
        return self.nome_projeto

class TimelineEvent(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='timeline_events')
    secao = models.CharField(max_length=100, blank=True)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    data = models.DateField()

    def __str__(self):
        return f"{self.titulo} - {self.family.get_nome_familia()}"

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    inicio = models.DateTimeField()
    familia = models.ForeignKey(Family, on_delete=models.CASCADE, null=False, related_name='eventos')
    confirmado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.titulo} - {self.inicio}"