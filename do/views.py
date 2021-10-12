from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import TodoForm
from .models import todo
from django.utils import timezone


def home(request):
    return render(request, 'do/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'do/signupuser.html', {'Form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'do/signupuser.html',
                              {'Form': UserCreationForm(), 'error': 'this user name already used'})
        else:
            return render(request, 'do/signupuser.html',
                          {'Form': UserCreationForm(), 'error': 'password did not match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'do/login.html', {'Form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'do/login.html',
                          {'Form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    else:
        logout(request)
        return redirect('home')


@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'do/createtodo.html', {'Form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'do/createtodo.html', {'Form': TodoForm(), 'error': 'Bad data passed in'})


@login_required
def currenttodos(request):
    todos = todo.objects.filter(user=request.user, datecomplited__isnull=True)
    return render(request, 'do/currenttodos.html', {'todos': todos})


@login_required
def completedtodos(request):
    todos = todo.objects.filter(user=request.user, datecomplited__isnull=False).order_by('-datecomplited')
    return render(request, 'do/completedtodos.html', {'todos': todos})


@login_required
def viewtodo(request, todo_pk):
    one_todo = get_object_or_404(todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=one_todo)
        return render(request, 'do/viewtodo.html', {'todo': one_todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=one_todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'do/viewtodo.html', {'todo': one_todo, 'form': form, 'error': 'Bad info'})


@login_required
def completetodo(request, todo_pk):
    one_todo = get_object_or_404(todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        one_todo.datecomplited = timezone.now()
        one_todo.save()
        return redirect('currenttodos')


@login_required
def deletetodo(request, todo_pk):
    one_todo = get_object_or_404(todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        one_todo.datecomplited = timezone.now()
        one_todo.delete()
        return redirect('currenttodos')
