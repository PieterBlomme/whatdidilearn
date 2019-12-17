from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from .forms import RegisterForm
from .models import *
from datetime import datetime

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

    #sort date descending
    articles = articles.order_by('-date')
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
    
    #sort date descending
    articles = articles.order_by('-date')
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

@login_required
def add_tag(request):
    if request.method == 'POST':
        pk = request.POST['pk']
        tag = request.POST['tag']

        paper = get_object_or_404(Article, pk=pk)
        user = request.user

        #No duplicates
        if not Tag.objects.filter(paper=paper).filter(user=user).filter(tag=tag).exists():
            tag_item = Tag(paper=paper, user=user, tag=tag)
            tag_item.save()

        return redirect('detail', pk=pk)

    else:
        return redirect('home')

@login_required
def add_benchmark(request):
    if request.method == 'POST':
        pk = request.POST['pk']
        dataset = request.POST['dataset']
        score = request.POST['score']
        url = request.POST['url']

        paper = get_object_or_404(Article, pk=pk)
        user = request.user

        #No duplicates
        if not Benchmark.objects.filter(paper=paper).filter(user=user).filter(dataset=dataset).exists():
            benchmark_item = Benchmark(paper=paper, user=user, dataset=dataset, score=score, code_url=url)
            benchmark_item.save()
        return redirect('detail', pk=pk)

    else:
        return redirect('home')


@login_required
def add_comment(request):
    if request.method == 'POST':
        pk = request.POST['pk']
        title = request.POST['title']
        text = request.POST['text']
        url = request.POST['url']

        paper = get_object_or_404(Article, pk=pk)
        user = request.user

        comment_item = Comment(paper=paper, user=user, title=title, text=text, code_url=url)
        comment_item.save()

        return redirect('detail', pk=pk)

    else:
        return redirect('home')

@login_required
def add_paper(request):
    if request.method == 'POST':
        title = request.POST['title']
        authors = request.POST['authors']
        if request.POST['date']:
            date = request.POST['date']
        else:
            date = datetime.today().strftime('%Y-%m-%d')
        url = request.POST['url']

        #Create paper
        #No duplicates
        if not Article.objects.filter(url=url).exists():
            paper = Article(title=title, authors=authors, date=date, url=url)
            paper.save()
        else:
            paper = Article.objects.get(url=url)

        #Add to user library
        #No duplicates
        user = request.user
        if not Library.objects.filter(paper=paper).filter(user=user).exists():
            lib_item = Library(paper=paper, user=user)
            lib_item.save()

        return redirect('detail', pk=paper.id)

    else:
         return render(request, 'learnsomething/new.html')

@login_required
def delete_tag(request, pk_paper, pk):
    tag = get_object_or_404(Tag, pk=pk)

    if (tag.user == request.user): # Safety check: only for given user
        tag.delete()

    return redirect('detail', pk=pk_paper)

@login_required
def delete_benchmark(request, pk_paper, pk):
    benchmark = get_object_or_404(Benchmark, pk=pk)

    if (benchmark.user == request.user): # Safety check: only for given user
        benchmark.delete()

    return redirect('detail', pk=pk_paper)

@login_required
def delete_comment(request, pk_paper, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if (comment.user == request.user): # Safety check: only for given user
        comment.delete()

    return redirect('detail', pk=pk_paper)

class ArticleDetailView(View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['pk'])
        tags = Tag.objects.filter(paper_id=article)
        benchmarks = Benchmark.objects.filter(paper_id=article)
        comments = Comment.objects.filter(paper_id=article)
        context = {'article': article, 'tags' : tags, 'benchmarks' : benchmarks, 'comments' : comments}
        return render(request, 'learnsomething/detail.html', context)