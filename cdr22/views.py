from django.shortcuts import render

def principal (request):
    return render(request, 'dashboard/principal.html')

""" Auth Views """
def login(request):
    return render(request, 'invitado/login.html')

def olvidePassword(request):
    return render(request, 'invitado/olvide-password.html')

""" Dashboard Views """
def home(request):
    return render(request, 'dashboard/home.html')


# Create your views here.
