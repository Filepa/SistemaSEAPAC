from django.db import models
import os
from django.conf import settings

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

LEVEL_CHOICES = [
    (1, "Inicial"),
    (2, "Intermediario"),
    (3, "Avancado")
]

class Family(models.Model):
    nome_titular = models.CharField(max_length=30)
    data_inicio = models.DateField()
    contato = models.CharField(max_length=30)
    municipio = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    projetos = models.ManyToManyField('Project', blank=True)
    subsistemas = models.ManyToManyField('Subsystem', through='FamilySubsystem', blank=True)
    renda = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.nome_titular

    def get_pontuacao(self):
        pontuacao = self.subsistemas.count() * 3
        if pontuacao == 6:
            return 0
        else:
            return pontuacao - 6

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
    
    def calcular_renda(self):
        dados_produtos = []
        total_receita = 0
        total_custo = 0
        renda_total = 0

        total_receita_potencial = 0
        renda_total_potencial = 0

        for fs in FamilySubsystem.objects.filter(family=self):
            produtos_dict = {}

            # Agrupar fluxos por produto
            for produto in fs.produtos_saida:
                nome = produto.get("nome", "Produto sem nome")
                fluxos = produto.get("fluxos", [])

                if nome not in produtos_dict:
                    produtos_dict[nome] = {
                        "nome": nome,
                        "valor_potencial": 0,
                        "valor_unitario": 0,
                        "custo_unitario": 0,
                        "qtd_total": 0,
                        "qtd_vendida": 0,
                        "custo_total": 0,
                    }

                for fluxo in fluxos:
                    qtd = fluxo.get("qtd") or 0
                    valor = fluxo.get("valor") or 0
                    valor_potencial = fluxo.get("valor_potencial") or 0
                    custo = fluxo.get("custo") or 0

                    produtos_dict[nome]["qtd_total"] += qtd
                    produtos_dict[nome]["valor_potencial"] = valor_potencial or produtos_dict[nome]["valor_potencial"]
                    produtos_dict[nome]["custo_unitario"] = custo or produtos_dict[nome]["custo_unitario"]
                    produtos_dict[nome]["custo_total"] += qtd * custo

                    if valor > 0:  # fluxo vendido
                        produtos_dict[nome]["valor_unitario"] = valor
                        produtos_dict[nome]["qtd_vendida"] += qtd

            # Agora calcular as métricas finais por produto
            for nome, dados in produtos_dict.items():
                qtd_total = dados["qtd_total"]
                qtd_vendida = dados["qtd_vendida"]
                valor_unitario = dados["valor_unitario"]
                valor_potencial = dados["valor_potencial"]
                custo_unitario = dados["custo_unitario"]
                custo_total = dados["custo_total"]

                # Receita e lucro reais
                receita_real = valor_unitario * qtd_vendida
                lucro_real = receita_real - custo_total

                # Receita e lucro potenciais — caso vendesse tudo
                receita_potencial = valor_potencial * qtd_total
                lucro_potencial = receita_potencial - custo_total

                dados_produtos.append({
                    "subsistema": fs.subsystem.nome_subsistema,
                    "produto": nome,
                    "qtd": qtd_total,  # mostra a quantidade total do produto
                    "valor": valor_unitario,
                    "valor_potencial": valor_potencial,
                    "custo": custo_unitario,
                    "receita": receita_real,
                    "receita_potencial": receita_potencial,
                    "custo_total": custo_total,
                    "lucro": lucro_real,
                    "lucro_potencial": lucro_potencial,
                })

                total_receita += receita_real
                total_custo += custo_total
                renda_total += lucro_real
                total_receita_potencial += receita_potencial
                renda_total_potencial += lucro_potencial

        return {
            "produtos": dados_produtos,
            "total_receita": total_receita,
            "total_custo": total_custo,
            "renda_total": renda_total,
            "total_receita_potencial": total_receita_potencial,
            "renda_total_potencial": renda_total_potencial,
        }

class Subsystem(models.Model):
    TIPO_CHOICES = [
        ('TS', 'Tecnologia Social'),
        ('SS', 'Subsistema'),
        ('ME', 'Mundo Externo'),
    ]

    nome_subsistema = models.CharField(max_length=50)
    descricao = models.TextField()
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES, default='SS')
    produtos_base = models.JSONField(default=list, blank=True)
    foto_subsistema = models.ImageField(upload_to='subsistemas/', null=True, blank=True, verbose_name="Foto do Subsistema")

    def __str__(self):
        return self.nome_subsistema
    
    def has_valid_photo(self):
        if self.foto_subsistema and self.foto_subsistema.name:
            caminho = os.path.join(settings.MEDIA_ROOT, self.foto_subsistema.name)
            return os.path.exists(caminho)
        return False

    def get_photo_url(self):
        if self.has_valid_photo():
            return self.foto_subsistema.url
        return None

class FamilySubsystem(models.Model):
    family = models.ForeignKey('Family', on_delete=models.CASCADE)
    subsystem = models.ForeignKey('Subsystem', on_delete=models.CASCADE)
    produtos_saida = models.JSONField(default=list, blank=True)

    class Meta:
        unique_together = ('family', 'subsystem')

    def __str__(self):
        return f"{self.family.get_nome_familia()} - {self.subsystem.nome_subsistema}"

class Project(models.Model):
    STATUS_CHOICES = [
        ('', 'Em Execução'),
        ('concluido', 'Concluído'),
        ('planejamento', 'Em Planejamento'),
    ]

    nome_projeto = models.CharField(max_length=200)
    familias = models.ManyToManyField(Family)
    tecnicos = models.ManyToManyField(Technician)
    descricao = models.TextField()
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='planejamento')
    orcamento = models.CharField(max_length=30, blank=True, null=True) #nao tem no diagrama mas eu mantive

    def __str__(self):
        return self.nome_projeto
    
    def get_municipios_atuacao(self):
        municipios = self.familias.values_list('municipio__nome', flat=True).distinct()
        return ", ".join(municipios)

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