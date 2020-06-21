from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from .forms import RegisterForm
from .models import *
from datetime import datetime
from django.db.models import Exists, OuterRef, BooleanField, Value, Q
from lxml import html
from lxml.etree import ParserError
import requests

from .utils import get_arxiv_sanity_array, search_helper

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
    if request.user.is_authenticated:
        user = request.user
        mylib = Library.objects.filter(paper=OuterRef('id'), user=user)
        articles = Article.objects.all().annotate(user_article=Exists(mylib))
    else:
        articles = Article.objects.all().annotate(user_article=Value(False, output_field=BooleanField()))
    
    if request.method == 'POST':
        articles = search_helper(articles, request.POST)
    else: #return last 50
        articles = articles.order_by('-date')[:50]

    #search dropdowns
    if request.user.is_authenticated:
        benchmarks = Benchmark.objects.filter(Q(user=user) | Q(private=False))
    else:
        benchmarks = Benchmark.objects.filter(private=False)
    benchmarks = benchmarks.values('dataset').distinct()
    tags = Tag.objects.values('tag').distinct()

    return render(request, 'learnsomething/home.html', {'articles': articles, 
                                                        'benchmarks' : benchmarks,
                                                        'tags' : tags })

def user_library(request, user):
    #library filter
    user = get_object_or_404(User, username=user)
    mylib = Library.objects.filter(paper=OuterRef('id'), user=user)
    articles = Article.objects.all().filter(Exists(mylib)).annotate(user_article=Exists(mylib))

    #search filter
    if request.method == 'POST':
        articles = search_helper(articles, request.POST)
    else: #return last 50
        articles = articles.order_by('-date')[:50]
        
    #search dropdowns
    if request.user.is_authenticated:
        benchmarks = Benchmark.objects.filter(Q(user=user) | Q(private=False))
    else:
        benchmarks = Benchmark.objects.filter(private=False)
    benchmarks = benchmarks.values('dataset').distinct()
    tags = Tag.objects.filter(user=user).values('tag').distinct()

    return render(request, 'learnsomething/home.html', {'articles': articles, 
                                                        'benchmarks' : benchmarks,
                                                        'tags' : tags,
                                                        'checkbox' : 'true' })
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
        if ('private' not in request.POST.keys()):
            private = False
        elif (request.POST['private'] == "on"):
            private = True
        else:
            private = False

        paper = get_object_or_404(Article, pk=pk)
        user = request.user

        #No duplicates
        if not Benchmark.objects.filter(paper=paper).filter(user=user).filter(dataset=dataset).exists():
            benchmark_item = Benchmark(paper=paper, user=user, dataset=dataset, score=score, code_url=url, private=private)
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
        if ('private' not in request.POST.keys()):
            private = False
        elif (request.POST['private'] == "on"):
            private = True
        else:
            private = False

        paper = get_object_or_404(Article, pk=pk)
        user = request.user

        comment_item = Comment(paper=paper, user=user, title=title, text=text, code_url=url, private=private)
        comment_item.save()

        return redirect('detail', pk=pk)

    else:
        return redirect('home')

@login_required
def add_paper(request):
    if request.method == 'POST':
        title = request.POST['title']
        authors = request.POST['authors']
        abstract = request.POST['abstract']
        if request.POST['date']:
            date = request.POST['date']
        else:
            date = datetime.today().strftime('%Y-%m-%d')
        url = request.POST['url']

        #Create paper
        #No duplicates
        if not Article.objects.filter(url=url).exists():
            paper = Article(title=title, authors=authors, date=date, url=url, abstract=abstract)
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
        user = request.user
        article = get_object_or_404(Article, pk=kwargs['pk'])

        if request.user.is_authenticated:
            if Library.objects.filter(user=user, paper=kwargs['pk']).count():
                article.user_article = True
        else:
            article.user_article = False

        show_all = self.request.GET.get('show_all', 0)

        tags = Tag.objects.filter(paper_id=article)

        #Get all comments/benchmarks that are non private or from user
        if request.user.is_authenticated:
            benchmarks = Benchmark.objects.filter(paper_id=article).filter(Q(user=user) | Q(private=False))
            comments = Comment.objects.filter(paper_id=article).filter(Q(user=user) | Q(private=False))
        else:
            benchmarks = Benchmark.objects.filter(paper_id=article).filter(private=False)
            comments = Comment.objects.filter(paper_id=article).filter(private=False)

        #filter if needed
        #show_all = 0: filter both
        #show_all = 1: filter benchmarks
        #show_all = 2: filter comments
        #show_all = 3: show all
        if show_all == 2 or show_all == 0:
            if request.user.is_authenticated:
                comments = comments.filter(user=user)
            else:
                comments = Comment.objects.none()
        if show_all == 1 or show_all == 0:
            if request.user.is_authenticated:
                benchmarks = benchmarks.filter(user=user)
            else:
                benchmarks = Benchmark.objects.none()

        if 'arxiv' in article.url:
            arxiv_id = article.url.split('/')[-1].replace('.pdf', '').replace('.PDF', '')
        else:
            arxiv_id = None

        #arxiv sanity most similar
        try:
            page = requests.get(f"http://www.arxiv-sanity.com/{arxiv_id}")
            tree = html.fromstring(page.content)
            scripts = tree.xpath('//*/script')
            for script in scripts:
                if '// passed in from flask as json' in script.text_content():
                    arxiv_sanity = get_arxiv_sanity_array(script.text_content())
        except ParserError:
            arxiv_sanity = ""

        context = {'article': article, 'tags' : tags, 'benchmarks' : benchmarks, 'comments' : comments, 
                            'show_all' : show_all, 'arxiv_id' : arxiv_id, 'arxiv_sanity' : arxiv_sanity}
        return render(request, 'learnsomething/detail.html', context)