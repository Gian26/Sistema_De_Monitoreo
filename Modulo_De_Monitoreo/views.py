# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from Modulo_De_Monitoreo.models import NodosDeRed, RedesDisponibles, DatosDeNodo
from django import forms
from django.core.urlresolvers import reverse
import json
from collections import *



#creamos el formulario para seleccionar los parametros que se desean ver

class Form(forms.Form):

    OPTIONS = (
        ("temperatura", "Temperatura"),
        ("ph", "pH"),
        ("conductividad", "Conductividad"),
         ("orp", "ORP"),
    )
#("D.O", "Disoulucion de Oxygeno"),

    parametros = forms.MultipleChoiceField(
        required=False,
        label=u'Parámetros',
        widget=forms.CheckboxSelectMultiple(),
        choices=OPTIONS, )

from django.views.decorators.csrf import csrf_exempt



def dashboard(request):
    return render_to_response('dashboard.html', {'activo': 'Centro_Redes',
                                                 'titulo': 'Redes Disponibles',
                                                 'redes': RedesDisponibles.objects.all(),
                                                })
@csrf_exempt
def get_nodes(request):

    redDisponible = RedesDisponibles.objects.get(direccion_Coordinador=request.POST.get('network'))
    nodos_de_red = NodosDeRed.objects.filter(red_asigando=redDisponible)
    final_data = []
    for red in nodos_de_red:
        response_data = { 'result':'CORRECT','postpk':red.pk,'direccion':red.direccion_de_nodo}
        final_data.append(dict(response_data))

    return HttpResponse(
            json.dumps(final_data),
            content_type="application/json"
        )

def date_filtering(request):


    final_data=[]
    return HttpResponse(
            json.dumps(final_data),
            content_type="application/json"
        )

def latest_networks(request):
    response_data = {}
    final_data = []
    for red in RedesDisponibles.objects.all():
        response_data = { 'result':'CORRECT','postpk':red.pk,'direccion':red.direccion_Coordinador,
                        'titulo':red.nombre_De_Red}
        final_data.append(dict(response_data))

    return HttpResponse(
            json.dumps(final_data),
            content_type="application/json"
        )

def mapas(request, coordinator_address):
    red_obtenida = RedesDisponibles.objects.get(direccion_Coordinador=coordinator_address)
    return render_to_response('google_maps_api.html', {'titulo': 'Mapa: ' + convert_name(red_obtenida.nombre_De_Red),
                                                       'activo': coordinator_address,
                                                       'redes': RedesDisponibles.objects.all(),
                                                       'dir': coordinator_address})

def convert_name(name):
    arreglo = name.split("_")
    nombre = ' '.join(arreglo)
    return nombre


@csrf_exempt
def mostrar_nodos_de_red(request, coordinador):
    #redes_registradas = RedesDisponibles.objects.all()
    redDisponible = RedesDisponibles.objects.get(direccion_Coordinador=coordinador)
    nodos_de_red = NodosDeRed.objects.filter(red_asigando=redDisponible)
    formulario = Form()

    if request.POST:
        nodos  = request.POST.getlist('nodos')
        parametros  = request.POST.getlist('parametros')
        coordinador = request.POST.get('coordinador')
        if not nodos or not parametros:
            return render(request, 'todos_los_nodos.html', {'titulo': 'Nodos: ' + convert_name( redDisponible.nombre_De_Red),
                                            'redes': RedesDisponibles.objects.all(),
                                            'activo': redDisponible.nombre_De_Red,
                                            'nodos': nodos_de_red,
                                            'coordinador':coordinador,
                                            'form': formulario,
                                            'error_message':"seleccione una opcion"})


        results = get_graph_data_json(nodos,parametros)

        return render_to_response('filtrado_de_parametros_y_nodos_graficas.html',
                    {'nodos':json.dumps(nodos),
                     'parametros':json.dumps(parametros),
                      'cord':json.dumps(coordinador),
                     'results':results})

    return render(request, 'todos_los_nodos.html', {'titulo': 'Nodos: ' + convert_name( redDisponible.nombre_De_Red),
                                            'redes': RedesDisponibles.objects.all(),
                                            'activo': redDisponible.nombre_De_Red,
                                            'nodos': nodos_de_red,
                                            'coordinador':coordinador,
                                            'form': formulario})

#def filtrado_de_parametros_y_nodos(request):

def grafica_de_nodo(request, nodo_direccion):
    #redes_registradas = RedesDisponibles.objects.all()
    graficas = ["temperatura", "conductividad","ph","orp"]
    nodo =  NodosDeRed.objects.get(direccion_de_nodo = nodo_direccion)
    coordinador = nodo.red_asigando

    return render_to_response('grafica_de_parametros.html', {'titulo': u'Gráfica del nodo ' + nodo_direccion,
                                                  'redes': RedesDisponibles.objects.all(),
                                                  'graficas': graficas,
                                                  'coordinador':coordinador.direccion_Coordinador,
                                                  'nodo': nodo_direccion})

def get_node_location(request, coordinator_address):
    cadena_json = []
    coordinador = RedesDisponibles.objects.get(direccion_Coordinador=coordinator_address)
    Nodos = NodosDeRed.objects.filter(red_asigando=coordinador)
    for nodo in Nodos:
        nodo_data = {'direccion': nodo.direccion_de_nodo,
                     'lat': nodo.latitude,
                     'lng': nodo.longitude}
        cadena_json.append(dict(nodo_data))

    return HttpResponse(json.dumps(cadena_json), content_type="application/json")


def get_graph_data(request, nodo_address):
    cadena = []
    string_concat = "id,temperatura, conductividad, ph, orp, fecha_hora"

    for nodo in DatosDeNodo.objects.raw('Select ' + string_concat
                                                + ' from Modulo_De_Monitoreo_datosdenodo  WHERE direccion_Del_Nodo_id = %s ORDER BY fecha_hora ASC',
                                        [NodosDeRed.objects.get(direccion_de_nodo=nodo_address).id]):
        data = {'fecha': str(nodo.fecha_hora),'ph':nodo.ph, 'temperatura': nodo.temperatura, 'conductividad': nodo.conductividad,
                 'orp': nodo.orp
                }
        cadena.append(dict(data))

    return HttpResponse(json.dumps(cadena), content_type="application/json")

def get_graph_data_json(node_address,parametros):
    cadena = []
    direcciones_list = node_address
    parametros_list = ','.join(parametros)
    data = defaultdict(list)
    for nodo_address in direcciones_list:
        nodos = DatosDeNodo.objects.raw('Select id,' + parametros_list
                                                    + ' from Modulo_De_Monitoreo_datosdenodo  WHERE direccion_Del_Nodo_id = %s ORDER BY fecha_hora ASC',
                                            [NodosDeRed.objects.get(direccion_de_nodo=nodo_address).id])
        for parametro in parametros:

            for nodo in nodos:
                temp={}
                temp['temperatura'] = nodo.temperatura
                temp['ph'] = nodo.ph
                temp['orp'] = nodo.orp
                temp['conductividad'] = nodo.conductividad
                resultados={'fecha': str(nodo.fecha_hora),"'"+parametro+"'":temp[parametro],'nodo':nodo_address}

                data[parametro].append(resultados)
            #cadena.append(dict(data))
    return json.dumps(data)
#','.join(mylist)

#
#METODOS PARA EL GUARDAD DE DATOS
#pk bread, 2 dollar de egg, sweet bread

def guardar_datos_de_nodo(request):
    coordinador_de_red = request.GET.get('coordinador', '')
    conductividad = request.GET.get('conductividad', '')
    orp = request.GET.get('orp','')
    temperatura = request.GET.get('temperature', '')
    address = request.GET.get('address', '')
    ph = request.GET.get('ph', '')
    lat = request.GET.get('lat', '')
    lon = request.GET.get('lon', '')
    Nombre_de_red=str(request.GET.get('nombre_de_red', ''))

    nodo = [coordinador_de_red, conductividad, temperatura, address, ph, lat, lon,orp]

    if (RedesDisponibles.objects.filter(direccion_Coordinador=nodo[0])):
        coordinador  = RedesDisponibles.objects.get(direccion_Coordinador=nodo[0])
        coordinador.nombre_De_Red = Nombre_de_red
        coordinador.save()
        return HttpResponse("existe red " + guardar_datos_del_nodo(nodo))
    else:
        guardar_red = RedesDisponibles(direccion_Coordinador = coordinador_de_red,nombre_De_Red=Nombre_de_red)
        guardar_red.save()
        guardar_datos_del_nodo(nodo)
        return HttpResponse("se dio de alta la red")

# Hacer el guardado y registro de los nodos de la red
def guardar_datos_del_nodo(nodo):
    conductividad = nodo[1]
    temperatura = nodo[2]
    direccion_Del_Nodo = nodo[3]
    dire_coordinador = nodo[0]
    ph = nodo[4]
    lat = nodo[5]
    lon = nodo[6]
    orp = nodo[7]

    if (NodosDeRed.objects.filter(direccion_de_nodo=direccion_Del_Nodo)):
        guardar_datos = DatosDeNodo(temperatura=temperatura,
                                    orp=orp,
                                    ph=ph,
                                    conductividad =conductividad,
                                    direccion_Del_Nodo=NodosDeRed.objects.get(direccion_de_nodo=direccion_Del_Nodo))
        guardar_datos.save()
        return ("existe nodo")
    else:
        #registrar el nodo y guardar datos
        nodo = NodosDeRed(direccion_de_nodo=direccion_Del_Nodo,
                          latitude=lat,
                          longitude=lon,
                          red_asigando=RedesDisponibles.objects.get(direccion_Coordinador=dire_coordinador))
        nodo.save()
        #direccion_Nodo =
        guardar_datos = DatosDeNodo(temperatura=temperatura,
                                    conductividad=conductividad,
                                    ph=ph,
                                    orp=orp,
                                    direccion_Del_Nodo=NodosDeRed.objects.get(direccion_de_nodo=direccion_Del_Nodo))
        guardar_datos.save()
        return ("no existe nodo " + direccion_Del_Nodo + " " + dire_coordinador)

@csrf_exempt
def rangepicker(request):

    cadena = []

    if request.POST:
        nodo_address = request.POST.get('nodo')
        fecha_inicio = request.POST.get('start_date')
        fecha_fin = request.POST.get('end_date')
    else:
        nodo_address = "1243332"
        fecha_inicio = "2015-04-02 00:00:00"
        fecha_fin = "2015-04-03 24:00:00"
        from datetime import datetime
        DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
        start_date = datetime.strptime(fecha_inicio, DATE_FORMAT)
        start_date_range = (
            # The start_date with the minimum possible time
            datetime.combine(start_date, datetime.min.time()),
            # The start_date with the maximum possible time
            datetime.combine(start_date, datetime.max.time())
        )
        qs = DatosDeNodo.objects.filter(fecha_hora__range=start_date_range, direccion_Del_Nodo=NodosDeRed.objects.get(direccion_de_nodo=nodo_address).id)


    datos_por_fecha = DatosDeNodo.objects.raw('Select * from Modulo_De_Monitoreo_datosdenodo  WHERE direccion_Del_Nodo_id = %s AND fecha_hora >= %s  AND fecha_hora <= %s  ORDER BY fecha_hora ASC',
                                            [NodosDeRed.objects.get(direccion_de_nodo=nodo_address).id,fecha_inicio,fecha_fin])

    for nodo in datos_por_fecha:
        data = {'fecha': str(nodo.fecha_hora),'ph':nodo.ph, 'temperatura': nodo.temperatura, 'conductividad': nodo.conductividad,'orp': nodo.orp}
        cadena.append(dict(data))

    return HttpResponse(json.dumps(cadena), content_type="application/json")