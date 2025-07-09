from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "flow/index.html")

def register(request):
    return render(request, "flow/register.html")