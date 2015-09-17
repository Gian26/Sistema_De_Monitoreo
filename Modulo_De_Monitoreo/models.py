from django.db import models
from django.utils import timezone
from datetime import *
import json
class RedesDisponiblesManager(models.Manager):

    def with_counts(self):
        cadena = []
        name_map = {'first': 'first_name', 'last': 'last_name', 'bd': 'birth_date', 'pk': 'id'}
        test=DatosDeNodo.objects.raw('SELECT * FROM Modulo_De_Monitoreo_datosdenodo')
        for nodo in test:
            data = {'fecha': str(nodo.fecha_hora),'ph':nodo.ph, 'temperatura': nodo.temperatura, 'conductividad': nodo.conductividad,
                 'orp': nodo.orp
                }
            cadena.append(dict(data))
        return json.dumps(cadena)

class RedesDisponibles(models.Model):
    direccion_Coordinador = models.CharField(max_length=15, blank=True)
    nombre_De_Red = models.CharField(max_length=100, blank=True)
    objects =RedesDisponiblesManager()


class NodosDeRed(models.Model):
    red_asigando = models.ForeignKey(RedesDisponibles)
    direccion_de_nodo = models.CharField(max_length=25)
    latitude = models.FloatField(max_length=233,blank=True)
    longitude = models.FloatField(max_length=233,blank=True)

class DatosDeNodo(models.Model):
    fecha_hora = models.DateTimeField(auto_now=True)
    temperatura = models.FloatField(max_length=255,blank=True)
    ph = models.FloatField(max_length=255,blank=True)
    conductividad = models.FloatField(max_length=255,blank=True)
    orp = models.FloatField(max_length=255,blank=True)
    direccion_Del_Nodo = models.ForeignKey(NodosDeRed)

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):              # __unicode__ on Python 2
        return self.headline