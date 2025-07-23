from django.shortcuts import render, get_object_or_404, redirect
from .models import Family, Subsystem
from .forms import FamilyForm

# Create your views here.
def index(request):
    total_families = Family.objects.count()
    families = Family.objects.all()
    total_avancado = Family.objects.filter(nivel=3).count()
    context = {
        "families": families,
        "total_families": total_families,
        "total_avancado": total_avancado,
        "title": "Página Inicial - Dashboard"
    }
    return render(request, "seapac/index.html", context)

def register(request):
    if request.method == 'POST':
        form = FamilyForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            form = FamilyForm()
    else:
        form = FamilyForm()

    return render(request, "seapac/form.html", {'form': form, 'title': 'Cadastrar Família'})

def edit_family(request,id):
    family = get_object_or_404(Family,id=id)
    if request.method == 'POST':
        form = FamilyForm(request.POST, request.FILES, instance=family)

        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = FamilyForm(instance=family)

    return render(request,'seapac/form.html', {'form':form, 'title': 'Editar Família'})

def list_families(request):
    families = Family.objects.all()
    context ={
        'families': families, 
        'title': 'Lista de Famílias'
    }
    return render(request, "seapac/list_families.html", context)

def flow(request, nome_familia):
    subsystems = Subsystem.objects.all()
    context = {
        "nome_familia": nome_familia,
        "subsystems": subsystems,
        "title": "Fluxo"
    }
    return render(request, "seapac/flow.html", context)

def timeline(request, nome_familia):
    context = {
        "nome_familia": nome_familia,
        "title": "Timeline"
    }
    return render(request, "seapac/timeline.html", context)