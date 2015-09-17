__author__ = 'GNC26'
from django.conf.urls import patterns, include, url
from models import DatosDeNodo,RedesDisponibles,NodosDeRed
from views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = patterns('',
    # Examples:
    url(r'^$',dashboard,name="dashboard"),
    url(r'get_data/(?P<nodo_address>[a-zA-Z0-9]+)/$',get_graph_data,name="graph_data"),
    url(r'all_nodes/(?P<coordinador>[a-zA-Z0-9]+)/$',mostrar_nodos_de_red,name="ver_nodos"),
    url(r'node_graph/(?P<nodo_direccion>[a-zA-Z0-9]+)/$',grafica_de_nodo,name="graph"),
    url(r'get_markers/(?P<coordinator_address>[a-zA-Z0-9]+)/$',get_node_location,name="location"),
    url(r'guardar_datos/',guardar_datos_de_nodo),
    url(r'maps/(?P<coordinator_address>[a-zA-Z0-9]+)$',mapas,name="mapas"),
    url(r'get_networks/$',latest_networks,name="new_networks"),
    url(r'get_nodes/$',get_nodes,name="new_nodes"),
    url(r'rangepick/$',rangepicker),
)


#http://serdmanczyk.github.io/XBeeAPI-PythonArduino-Tutorial/
#https://github.com/msepcot/arduino_samples