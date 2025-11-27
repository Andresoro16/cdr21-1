from django.shortcuts import render

def principal (request):
    return render(request, 'dashboard/principal.html')

def login(request):
    return render(request, 'invitado/login.html')

def home(request):
    return render(request, 'dashboard/home.html')

# Create your views here.
