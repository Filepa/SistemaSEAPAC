from django.shortcuts import render, get_object_or_404, redirect
from .models import Family, Subsystem, Evento, Terrain, FamilySubsystem, Project
from .forms import FamilyForm, TerrainForm
from django.forms import formset_factory
from django import forms
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
import json

LEVEL_CHOICES = [
    (1, "Inicial"),
    (2, "Intermediario"),
    (3, "Avancado")
]

# Create your views here.
def index(request):
    level = request.GET.get('nivel')
    query = request.GET.get('q')
    families = Family.objects.all()
    if query:
        families = families.filter(nome_titular__icontains=query)
    if level:
        families = [f for f in families if str(f.get_nivel()) == str(dict(LEVEL_CHOICES).get(int(level)))]
    total_municipios = Terrain.objects.values('municipio').distinct().count()
    total_families = Family.objects.count()
    total_avancado = len([f for f in Family.objects.all() if f.get_nivel() == "Avancado"])
    total_intermediario = len([f for f in Family.objects.all() if f.get_nivel() == "Intermediario"])
    total_inicial = len([f for f in Family.objects.all() if f.get_nivel() == "Inicial"])
    context = {
        "families": families,
        "total_families": total_families,
        "total_avancado": total_avancado,
        "total_intermediario": total_intermediario,
        "total_inicial": total_inicial,
        "title": "Página Inicial - Dashboard",
        "nivel_selecionado": level,
        "query": query,
        "total_municipios": total_municipios
    }
    return render(request, "seapac/index.html", context)

def register(request):
    if request.method == 'POST':
        terrainform = TerrainForm(request.POST)
        familyform = FamilyForm(request.POST, request.FILES)
        if terrainform.is_valid() and familyform.is_valid():
            terrain = terrainform.save()
            family = familyform.save(commit=False)
            family.terra = terrain
            family.save()
            familyform.save_m2m()
            return redirect('edit_flow', id=family.id)
        else:
            print(terrainform.errors, familyform.errors)
    else:
        terrainform = TerrainForm()
        familyform = FamilyForm()
    return render(request, "seapac/form.html", {
        'familyform': familyform,
        'terrainform': terrainform,
        'title': 'Cadastrar Família'
    })

def edit_flow(request, id):
    family = get_object_or_404(Family, id=id)
    subsystems = Subsystem.objects.all()
    selected_ids = list(family.subsistemas.values_list('id', flat=True))
    if request.method == 'POST':
        selected = request.POST.getlist('subsistemas')
        family.subsistemas.set(selected)
        family.save()
        return redirect('index')
    return render(request, "seapac/formflow.html", {
        'family': family,
        'subsystems': subsystems,
        'selected_ids': selected_ids,
        'title': 'Fluxo'
    })

#crud projetos: fazendo

#def list_projects(request):
   # projects = Project.objects.all()
    #return render(request, 'seapac/projetos/projects.html', {'projects': projects})

#def create_projects(request, id): 
   # if request.method == 'POST':
     #   form = ProjectForm(request.POST)
       # if form.is_valid():
         #   projetos = form.save()
          #  return redirect('list_projects')

    #else: 
     #   form = ProjectForm()

    #return render(request, 'seapac/projetos/projects_form.html', {'form': form, 'projetos': None})

#def edit_projects(request, pk): 
    #projetos = get_object_or_404(Project, pk=pk)
    
    #if request.method == 'POST':
      #  form = ProjectForm(request.POST, instance=projetos)
       # if form.is_valid():
        #    form.save()
         #   return redirect('detail_projects', pk=projetos.pk)
   # else:
        #form = ProjetcForm(instance=projetos)
    #
   # return render(request, 'seapac/projetos/projects_detail.html', {
      # 'form': form,
       # 'projeto': projetos
    #})

#def detail_projects(request, pk):
   # projetos = get_object_or_404(Project, pk=pk)
   # context= {
       # 'projetos': projetos
   # }
   # return render(request, 'seapac/projetos/projects_detail.html', context) 


def edit_family(request, id):
    family = get_object_or_404(Family, id=id)
    try:
        terrain = Terrain.objects.get(family=family)
    except Terrain.DoesNotExist:
        terrain = None

    if request.method == 'POST':
        familyform = FamilyForm(request.POST, request.FILES, instance=family)
        terrainform = TerrainForm(request.POST, instance=terrain)
        if familyform.is_valid() and terrainform.is_valid():
            family = familyform.save()
            terrain = terrainform.save(commit=False)
            terrain.family = family
            terrain.save()
            return redirect('index')
    else:
        familyform = FamilyForm(instance=family)
        terrainform = TerrainForm(instance=terrain)
    return render(request, "seapac/form.html", {
        'familyform': familyform,
        'terrainform': terrainform,
        'title': 'Editar Família'
    })

def list_families(request):
    level = request.GET.get('nivel')
    query = request.GET.get('q')
    families = Family.objects.all()
    if level:
        families = [f for f in families if str(f.get_nivel()) == str(dict(LEVEL_CHOICES).get(int(level)))]
    if query:
        families = families.filter(nome_titular__icontains=query)
    context ={
        'families': families, 
        'title': 'Lista de Famílias',
        "nivel_selecionado": level,
        "query": query
    }
    return render(request, "seapac/list_families.html", context)

def family_profile(request, id):
    family = get_object_or_404(Family, id=id)
    context = {
        "family": family,
        "title": "Perfil da Família"
    }
    return render(request, "seapac/family_profile.html", context)

def flow(request, id):
    family = get_object_or_404(Family, id=id)
    family_subsystems = FamilySubsystem.objects.filter(family=family).select_related('subsystem')
    
    subsystems_data = []
    for family_subsystem in family_subsystems:
        subsystems_data.append({
            'nome_subsistema': family_subsystem.subsystem.nome_subsistema,
            'produtos_saida': family_subsystem.produtos_saida,
        })

    json_subsystems = json.dumps(subsystems_data, separators=(',', ':'))

    context = {
        "id": id,
        "family": family,
        "family_subsystems": family_subsystems,
        "total_subsystems": family_subsystems.count(),
        "title": "Fluxo",
        "json_subsystems": json_subsystems
    }
    return render(request, "seapac/flow.html", context)

def subsystem_panel(request, family_id, subsystem_id):
    family = get_object_or_404(Family, id=family_id)
    family_subsystem = get_object_or_404(FamilySubsystem, family=family, subsystem_id=subsystem_id)

    if not family_subsystem.produtos_saida:
        family_subsystem.produtos_saida = family_subsystem.subsystem.produtos_base
        family_subsystem.save()


    return render(request, "seapac/subsystem_panel.html", {
        'subsystem': family_subsystem.subsystem,
        'family': family,
        'family_subsystem': family_subsystem,
        'title': 'Painel do Subsistema',
        'type': 'readonly'
    })

def edit_subsystem_panel(request, family_id, subsystem_id):
    family = get_object_or_404(Family, id=family_id)
    family_subsystem = get_object_or_404(FamilySubsystem, family=family, subsystem_id=subsystem_id)

    subsystems_destino = family.subsistemas.all()
    destino_choices = [(s.nome_subsistema, s.nome_subsistema) for s in subsystems_destino]
    destino_choices.insert(0, ('', '---------'))

    produto_choices = [(p['nome'], p['nome']) for p in family_subsystem.produtos_saida]

    class FluxoForm(forms.Form):
        nome_produto = forms.ChoiceField(choices=(), required=True, label="Produto")
        porcentagem = forms.DecimalField(required=False, max_digits=6, decimal_places=2, label="Porcentagem")
        destino = forms.ChoiceField(choices=(), required=False, label="Destino")

    FluxoFormSet = formset_factory(FluxoForm, extra=1, can_delete=True)

    if request.method == 'POST':
        formset = FluxoFormSet(request.POST, prefix='fluxo')
        for form in formset:
            form.fields['nome_produto'].choices = produto_choices
            form.fields['destino'].choices = destino_choices

        if formset.is_valid():
            produtos_saida_atualizados = list(family_subsystem.produtos_saida)
            novos_fluxos = {p['nome']: [] for p in produtos_saida_atualizados}

            for form in formset:
                if not form.cleaned_data:
                    continue
                nome_produto = form.cleaned_data['nome_produto']
                porcentagem = form.cleaned_data.get('porcentagem') or 0
                destino = form.cleaned_data.get('destino') or ''

                novos_fluxos[nome_produto].append({
                    'porcentagem': float(porcentagem),
                    'destino': destino,
                })

            for produto in produtos_saida_atualizados:
                nome = produto['nome']
                produto['fluxos'] = novos_fluxos.get(nome, [])

            family_subsystem.produtos_saida = produtos_saida_atualizados
            family_subsystem.save()

            return redirect('subsystem_panel', family_id=family.id, subsystem_id=family_subsystem.subsystem.id)

    else:
        initial_data = []
        for produto in family_subsystem.produtos_saida:
            if produto['fluxos']:
                for fluxo in produto['fluxos']:
                    initial_data.append({
                        'nome_produto': produto['nome'],
                        'porcentagem': fluxo['porcentagem'],
                        'destino': fluxo['destino'],
                    })

        formset = FluxoFormSet(initial=initial_data, prefix='fluxo')
        for form in formset:
            form.fields['nome_produto'].choices = produto_choices
            form.fields['destino'].choices = destino_choices

    return render(request, "seapac/subsystem_panel.html", {
        'subsystem': family_subsystem.subsystem,
        'family': family,
        'family_subsystem': family_subsystem,
        'title': 'Editar Painel do Subsistema',
        'type': 'edit',
        'formset': formset,
    })

def timeline(request, id):
    family = get_object_or_404(Family, id=id)
    context = {
        "id": id,
        "family": family,
        "title": "Linha do Tempo"
    }
    return render(request, "seapac/timeline.html", context)

def calendar(request):
    level = request.GET.get('nivel')
    query = request.GET.get('q')
    families = Family.objects.all()
    if level:
        families = [f for f in families if str(f.get_nivel()) == str(dict(LEVEL_CHOICES).get(int(level)))]
    if query:
        families = families.filter(nome_titular__icontains=query)
    context = {
        "title": "Calendário de Visitas",
        "families": families,
        "nivel_selecionado": level,
        "query": query,
    }
    return render(request, "seapac/calendar.html", context)

def eventos_json(request):
    eventos = Evento.objects.all()
    data = [{
        'id': e.id,
        'title': e.titulo,
        'start': e.inicio.isoformat()
    } for e in eventos]
    return JsonResponse(data, safe=False)

@csrf_exempt
def criar_evento(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        start_datetime = parse_datetime(data['start'])
        
        evento = Evento.objects.create(
            titulo=data['title'],
            inicio=start_datetime
        )
        Evento.save_as_fixture()
        return JsonResponse({'status': 'ok', 'id': evento.id})
    
@csrf_exempt
def deletar_evento(request, event_id):
    if request.method == 'DELETE':
        try:
            evento = Evento.objects.get(id=event_id)
            evento.delete()
            Evento.save_as_fixture()
            return JsonResponse({'status': 'ok'})
        except Evento.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Evento não encontrado'}, status=404)