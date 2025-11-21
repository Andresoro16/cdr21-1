from django.shortcuts import render

def principal (request):
    return render(request, 'dashboard/principal.html')

def login(request):
    return render(request, 'invitado/login.html')

# Create your views here.
