# Generated by Django 2.2 on 2019-04-15 23:18

import datetime
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
            name='Dog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image_filename', models.CharField(max_length=255)),
                ('breed', models.CharField(blank=True, default='', max_length=255)),
                ('age', models.IntegerField(default=None, null=True)),
                ('gender', models.CharField(max_length=1)),
                ('size', models.CharField(max_length=255)),
                ('date_added', models.DateField(default=datetime.date.today)),
                ('temperment', models.CharField(blank=True, default='', max_length=255)),
                ('vaccinated', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserPref',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.CharField(default='', max_length=255)),
                ('gender', models.CharField(default='', max_length=255)),
                ('size', models.CharField(default='', max_length=255)),
                ('temperment', models.CharField(default='', max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='preferences', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserDog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=1)),
                ('rating', models.IntegerField(default=5)),
                ('dog', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pugorugh.Dog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]