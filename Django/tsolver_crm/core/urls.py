from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contacto', views.contacto, name="contacto"),
    path('personas/alta', views.alta_personas, name="alta_persona"),
    path('prospectos/alta', views.alta_prospectos, name="alta_prospecto"),
    path('prospectos/listado', views.prospectos_listado, name='prospectos_listado'),
    path('prospectos/detalle/<str:nombre_prospecto>', views.prospecto_detalle, name='prospecto_detalle'),
    path('prospectos/historico/2017/', views.prospectos_historico_2017, name='prospectos_historico'),
    re_path(r'prospectos/historico/(?P<year>[0-9]{4})/$', views.prospectos_historico, name='prospectos_historico'),
    path('prospectos/activos', views.prospectos_estado, {'estado': 'activo'}, name="prospectos_activos"),
    path('prospectos/inactivos', views.prospectos_estado, {'estado': 'inactivo'}, name="prospectos_inactivos"),
    
    path('gestion/stock', views.gestion_de_stock, name="gestion_de_stock"),

]
