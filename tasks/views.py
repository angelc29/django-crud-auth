from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

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

@login_required
def tasks(request):
    # Se coloca un filtro para mostrar solo las tareas del usuario actual
    # datecompleted es la fecha en que se completó la tarea por lo que si esta null, no esta terminada
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request,'tasks.html', {
        'tasks': tasks,
        'type': 'Pending'
    })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'tasks.html', {
        'tasks': tasks,
        'type': 'Completed'
    })

@login_required
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

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        #task = Task.objects.get(pk=task_id)
        # Se utiliza otra funcion para poder mandar un 404
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        # Se le pasa como parametro el objeto tarea al template para posteriormete ser usado para renderizar
        form = TaskForm(instance=task)
        return render(request,'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            render(request,'task_detail.html', {'task': task, 'form': form, 'error': 'Error updating task'})

@login_required
def complete_task(request,task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
    return redirect('tasks')

@login_required
def delete_task(request,task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
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