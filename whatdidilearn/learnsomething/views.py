from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
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
    #search filter
    if request.method == 'POST':
        search_string = request.POST['search_article']
        articles = Article.objects.filter(title__icontains=search_string) | Article.objects.filter(authors__icontains=search_string)
    else:
        articles = Article.objects.all()

    return render(request, 'learnsomething/home.html', {'articles': articles })

@login_required
def home_library(request):
    #library filter
    user = request.user
    user_articles = Library.objects.filter(user=user).values_list('paper', flat=True)
    articles = Article.objects.filter(id__in=user_articles)

    #search filter
    if request.method == 'POST':
        search_string = request.POST['search_article']
        articles = articles.filter(paper_title__icontains=search_string) | Article.objects.filter(paper_authors__icontains=search_string)

    print(articles)

    return render(request, 'learnsomething/home.html', {'articles': articles, 'checkbox' : 'true' })

@login_required
def add_to_lib(request):
    if request.method == 'POST':
        pk = request.POST['pk']
        paper = get_object_or_404(Article, pk=pk)
        user = request.user

        #No duplicates
        if not Library.objects.filter(paper=paper).filter(user=user).exists():
            lib_item = Library(paper=paper, user=user)
            lib_item.save()

    return redirect('detail', pk=pk)

class ArticleDetailView(View):
    def get(self, request, *args, **kwargs):
        print(kwargs['pk'])
        article = get_object_or_404(Article, pk=kwargs['pk'])
        tags = Tag.objects.filter(paper_id=article)
        benchmarks = Benchmark.objects.filter(paper_id=article)
        comments = Comment.objects.filter(paper_id=article)
        context = {'article': article, 'tags' : tags, 'benchmarks' : benchmarks, 'comments' : comments}
        return render(request, 'learnsomething/detail.html', context)