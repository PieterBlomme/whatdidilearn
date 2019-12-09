from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import *

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'learnsomething/signup.html', {'form': form})

def home(request):
    checkbox_val = "false"
    if request.method == 'POST':
        print(request.POST['mylibrary_post'])
        checkbox_val = request.POST['mylibrary_post']

        if 'search_article' in request.POST:
            search_string = request.POST['search_article']
            articles = Article.objects.filter(title__icontains=search_string) | Article.objects.filter(authors__icontains=search_string)
    else:
        articles = Article.objects.all()

    return render(request, 'learnsomething/home.html', {'articles': articles, 
                                                        'checkbox' : checkbox_val #send it back
                                                        })