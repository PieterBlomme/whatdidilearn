# Generated by Django 3.0 on 2019-12-08 19:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=1000, unique=True)),
                ('title', models.CharField(max_length=1000)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=500)),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learnsomething.Article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learnsomething.Article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_url', models.URLField(max_length=1000)),
                ('title', models.CharField(max_length=1000)),
                ('text', models.TextField()),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learnsomething.Article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Benchmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_url', models.URLField(max_length=1000)),
                ('dataset', models.CharField(max_length=1000)),
                ('score', models.DecimalField(decimal_places=5, max_digits=10)),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learnsomething.Article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
