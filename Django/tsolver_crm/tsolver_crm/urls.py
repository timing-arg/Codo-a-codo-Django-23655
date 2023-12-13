"""
URL configuration for tsolver_crm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from core.admin import sitio_admin

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD:Django/tsolver_crm/tsolver_crm/urls.py
    path('tsolver_crm/', include('core.urls')),
=======
    #path('admin/', sitio_admin.urls),
    path('aula_virtual/', include('core.urls')),
>>>>>>> 307a084ba1eb3bb45212deb5743bb1cc04dbe4dd:Django/aulavirtual/aulavirtual/urls.py
]