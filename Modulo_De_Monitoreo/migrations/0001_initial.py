# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=75)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('tagline', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DatosDeNodo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_hora', models.DateTimeField(auto_now=True)),
                ('temperatura', models.FloatField(max_length=255, blank=True)),
                ('ph', models.FloatField(max_length=255, blank=True)),
                ('conductividad', models.FloatField(max_length=255, blank=True)),
                ('orp_sensor', models.FloatField(max_length=255, blank=True)),
            ],
            options={
                'ordering': ('fecha_hora',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('headline', models.CharField(max_length=255)),
                ('body_text', models.TextField()),
                ('pub_date', models.DateField()),
                ('mod_date', models.DateField()),
                ('n_comments', models.IntegerField()),
                ('n_pingbacks', models.IntegerField()),
                ('rating', models.IntegerField()),
                ('authors', models.ManyToManyField(to='Modulo_De_Monitoreo.Author')),
                ('blog', models.ForeignKey(to='Modulo_De_Monitoreo.Blog')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NodosDeRed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('direccion_de_nodo', models.CharField(max_length=25)),
                ('latitude', models.FloatField(max_length=233, blank=True)),
                ('longitude', models.FloatField(max_length=233, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RedesDisponibles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('direccion_Coordinador', models.CharField(max_length=15, blank=True)),
                ('nombre_De_Red', models.CharField(max_length=100, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='nodosdered',
            name='red_asigando',
            field=models.ForeignKey(to='Modulo_De_Monitoreo.RedesDisponibles'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datosdenodo',
            name='direccion_Del_Nodo',
            field=models.ForeignKey(to='Modulo_De_Monitoreo.NodosDeRed'),
            preserve_default=True,
        ),
    ]
