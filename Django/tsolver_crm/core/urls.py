from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views
from .views import actualizar_stock  # Ajusta la importación según tu estructura de carpetas

router = DefaultRouter()
router.register(r'Persona', views.PersonaViewSet, basename='Persona')

urlpatterns = [
    path('', views.index, name='index'),
    path('api', include(router.urls)),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='core/login.html'),name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

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

    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('actualizar_stock/', actualizar_stock, name='actualizar_stock'),
    #----productos--------------------------------------------------------------------------------------------------
    path('crear_producto/',views.crear_producto, name='crear_producto'),
    path('editar_producto/<str:codigo_de_producto>/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<str:codigo_de_producto>/',views.eliminar_producto, name='eliminar_producto'),
    path('seleccionar_producto/',views.seleccionar_producto, name='seleccionar_producto'),
    path('ver_productos/', views.ver_productos, name='ver_productos'),



]
