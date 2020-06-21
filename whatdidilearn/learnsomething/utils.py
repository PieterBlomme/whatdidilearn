from .models import *

def get_references(script_content):
    try:
        refs = []
        for ref in script_content['references']:
            d_ref = {
                'title' : ref['title'],
                'year' : ref['year'],
                'authors' : [a['name'] for a in ref['authors']],
            }
            refs.append(d_ref)

        return refs
    except:
        return None

def get_arxiv_sanity_array(script_content):
    capture = False
    text = ''
    for line in script_content.splitlines():
        if line.startswith('var papers'):
            line = line.replace('var papers = ', '')
            capture = True
        if line.startswith('var pid_to_users'):
            capture = False

        if capture:
            text += line
    return text

def search_helper(articles, POST):
    if 'search_article' in POST:
        search_string = POST['search_article']
        articles = articles.filter(title__icontains=search_string) | articles.filter(authors__icontains=search_string) | articles.filter(abstract__icontains=search_string)
    if 'search_tag' in POST:
        search_string = POST['search_tag']
        tags = Tag.objects.filter(tag__icontains=search_string).values_list('paper', flat=True)
        articles = articles.filter(id__in=tags)
    if 'search_benchmark' in POST:
        search_string = POST['search_benchmark']
        benchmarks = Benchmark.objects.filter(dataset__icontains=search_string).values_list('paper', flat=True)
        articles = articles.filter(id__in=benchmarks)

    return articles.order_by('-date')