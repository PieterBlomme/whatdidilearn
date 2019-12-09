from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    url = models.URLField(unique=True, max_length=1000)
    title = models.CharField(max_length=1000)
    authors = models.CharField(max_length=1000, default="")
    date = models.DateField()

class Tag(models.Model):
    paper = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=500)

class Library(models.Model):
    paper = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    paper = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code_url = models.URLField(max_length=1000)
    title = models.CharField(max_length=1000)
    text = models.TextField()

class Benchmark(models.Model):
    paper = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code_url = models.URLField(max_length=1000)
    dataset = models.CharField(max_length=1000)
    score = models.DecimalField(max_digits=10, decimal_places=5)