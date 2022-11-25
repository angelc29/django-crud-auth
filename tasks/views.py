from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm

# Create your views here.
def home(request):
    # Es a traves del 3er parametro que se le pasan las propiedades
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        # Es a traves del 3er parametro que se le pasan las propiedades
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                #Register user
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect(tasks) #Redirije a otra vista con este metodo
            except IntegrityError:
                return render(request, 'signup.html',{
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })
        else:
            return render(request, 'signup.html',{
                'form': UserCreationForm,
                'error': 'Passwords dont match'
            })

def tasks(request):
    return render(request,'tasks.html')

def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST) # Crea un form con los datos que se le pasaron en el metodo POST
            new_task = form.save(commit=False) # Para evitar que se suba
            new_task.user = request.user # Se le asigna el usuario actual
            new_task.save()
            return redirect('tasks')
        except ValueError: 
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Please provide valide data'
            })


def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])

        if user is None:
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')