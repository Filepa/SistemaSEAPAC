from django.shortcuts import render, get_object_or_404, redirect
from .models import Family, Subsystem, Evento, Terrain, Project
from .forms import FamilyForm, TerrainForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
import json

# Create your views here.
def index(request):
    level = request.GET.get('nivel')
    query = request.GET.get('q')
    families = Family.objects.all()
    if level:
        families = families.filter(nivel=level)
    if query:
        families = families.filter(nome_titular__icontains=query)
    total_municipios = Terrain.objects.values('municipio').distinct().count()
    total_families = Family.objects.count()
    total_avancado = Family.objects.filter(nivel=3).count()
    total_intermediario = Family.objects.filter(nivel=2).count()
    total_inicial = Family.objects.filter(nivel=1).count()
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
        familyform = FamilyForm(request.POST, request.FILES)
        terrainform = TerrainForm(request.POST)
        if familyform.is_valid() and terrainform.is_valid():
            family = familyform.save()
            terrain = terrainform.save(commit=False)
            terrain.family = family 
            terrain.save()
            return redirect('index')
    else:
        familyform = FamilyForm()
        terrainform = TerrainForm()
    return render(request, "seapac/form.html", {
        'familyform': familyform,
        'terrainform': terrainform,
        'title': 'Cadastrar Família'
    })

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
        families = families.filter(nivel=level)
    if query:
        families = families.filter(nome_titular__icontains=query)
    context ={
        'families': families, 
        'title': 'Lista de Famílias',
        "nivel_selecionado": level,
        "query": query
    }
    return render(request, "seapac/list_families.html", context)

def flow(request, id):
    family = get_object_or_404(Family, id=id)
    subsystems = Subsystem.objects.all()
    context = {
        "id": id,
        "family": family,
        "subsystems": subsystems,
        "title": "Fluxo"
    }
    return render(request, "seapac/flow.html", context)

def timeline(request, id):
    family = get_object_or_404(Family, id=id)
    context = {
        "id": id,
        "family": family,
        "title": "Linha do Tempo"
    }
    return render(request, "seapac/timeline.html", context)

def family_profile(request, id):
    family = get_object_or_404(Family, id=id)
    context = {
        "id": id,
        "family": family,
        "title": "Perfil"
    }
    return render(request, "seapac/family_profile.html", context)

def calendar(request):
    level = request.GET.get('nivel')
    query = request.GET.get('q')
    families = Family.objects.all()
    if level:
        families = families.filter(nivel=level)
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