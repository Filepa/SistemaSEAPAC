from django.shortcuts import render
from .models import Family, Subsystem

# Create your views here.
def index(request):
    families = Family.objects.all()
    context = {
        "families": families
    }
    return render(request, "flow/index.html", context)

def register(request):
    return render(request, "flow/register.html")

def flow(request, nome_familia):
    subsystems = Subsystem.objects.all()
    context = {
        "nome_familia": nome_familia,
        "subsystems": subsystems
    }
    return render(request, "flow/flow.html", context)

def timeline(request, nome_familia):
    context = {
        "nome_familia": nome_familia
    }
    return render(request, "flow/timeline.html", context)